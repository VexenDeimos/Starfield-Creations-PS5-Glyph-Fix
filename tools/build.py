#!/usr/bin/env python3
"""Build the validated Starfield Creations PS5 font mod from user-owned vanilla files.

Requires Python 3.8+ (standard library only).
Does not download, bundle, overwrite, or modify Starfield game assets.
Supported input is the exact tested original English font pair.
"""

from __future__ import annotations

import argparse
import hashlib
import io
from pathlib import Path
import struct
import sys
import zipfile
import zlib

VERSION = "1.0.0"
VANILLA_SHA256 = {
    "fonts_en.gfx": "f8afad5c8e54ad762200e658a2b7953864a12a04d6e20b9f7e19207836e9e1ce",
    "fonts_en.swf": "76cbfe7dfdaf84fb2019fd7e50f880e1301d0d20cd6dd9b87886e577371356e1",
}
TESTED_SHA256 = {
    "fonts_en.gfx": "3a2eff307bc24a19b63647dbaa2e1c9572d96a97e37289332e42ed562c89e0a1",
    "fonts_en.swf": "609e5ea45d57565f2f9a6d7d63156129a4513a5fdeb46dddb7deea98e4e8c1d1",
}
# All source glyphs already exist in the player's genuine vanilla font.
# Only the glyph SHAPES are copied; their code points and layout metrics stay intact.
GLYPH_MAP = {ord(target): ord(source) for target, source in (
    ("A", "a"),  # Select -> Cross
    ("B", "b"),  # Load Order -> Triangle
    ("C", "c"),  # Purchase Credits -> Square
    ("D", "d"),  # Back -> Circle
    ("G", "g"),  # Search -> L1
    ("J", "j"),  # Category List -> L2
    ("P", "O"),  # Options -> PlayStation menu/Options lines
)}
CONTROLLER_FONT_IDS = (6, 7, 9)


def sha256(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def read_verified(path: Path, filename: str) -> bytes:
    raw = path.read_bytes()
    got = sha256(raw)
    expected = VANILLA_SHA256[filename]
    if got != expected:
        raise ValueError(
            f"{path}: unsupported source file (SHA-256 {got}).\n"
            f"Only the tested vanilla file (SHA-256 {expected}) is supported. "
            "Do not force this patch onto a different game build or another mod's fonts."
        )
    return raw


def replace_glyph_shapes(payload: bytes) -> bytes:
    """Rewrite DefineFont3 glyph shape data/offsets, preserving codes and metrics."""
    if len(payload) < 9:
        raise ValueError("Truncated DefineFont3")
    font_id, flags, _lang, name_len = struct.unpack_from("<HBBB", payload)
    if font_id not in CONTROLLER_FONT_IDS:
        return payload
    if flags != 0x84:
        raise ValueError(f"Unexpected DefineFont3 flags: {font_id}: 0x{flags:02x}")

    offsets_start = 5 + name_len + 2
    glyph_count = struct.unpack_from("<H", payload, offsets_start - 2)[0]
    if glyph_count != 68:
        raise ValueError(f"Unexpected glyph count in font {font_id}: {glyph_count}")
    old_offsets = [
        struct.unpack_from("<H", payload, offsets_start + 2 * i)[0]
        for i in range(glyph_count)
    ]
    old_code_offset = struct.unpack_from("<H", payload, offsets_start + 2 * glyph_count)[0]
    code_start = offsets_start + old_code_offset
    codes = [
        struct.unpack_from("<H", payload, code_start + 2 * i)[0]
        for i in range(glyph_count)
    ]
    if len(set(codes)) != len(codes) or not set(GLYPH_MAP).union(GLYPH_MAP.values()).issubset(codes):
        raise ValueError(f"Font {font_id} has unexpected character codes")
    shapes = [
        payload[offsets_start + old_offsets[i]:offsets_start + (
            old_offsets[i + 1] if i + 1 < glyph_count else old_code_offset
        )]
        for i in range(glyph_count)
    ]
    if any(len(shape) < 2 for shape in shapes):
        raise ValueError(f"Unexpected glyph shape in font {font_id}")

    original_by_code = dict(zip(codes, shapes))
    new_shapes = [original_by_code[GLYPH_MAP[code]] if code in GLYPH_MAP else shape
                  for code, shape in zip(codes, shapes)]

    # Original font uses 16-bit offsets. Offset zero is relative to the offset table.
    offset = 2 * (glyph_count + 1)
    new_offsets = []
    for shape in new_shapes:
        new_offsets.append(offset)
        offset += len(shape)
    if offset > 0xFFFF:
        raise ValueError(f"Font {font_id} requires unsupported wide offsets")

    return (payload[:offsets_start]
            + b"".join(struct.pack("<H", entry) for entry in new_offsets)
            + struct.pack("<H", offset)
            + b"".join(new_shapes)
            + payload[code_start:])


def patch_font_file(raw: bytes) -> bytes:
    compressed = raw[:3] == b"CWS"
    if not compressed and raw[:3] != b"GFX":
        raise ValueError("Expected vanilla compressed SWF (CWS) or GFX font file")

    uncompressed = raw[:8] + zlib.decompress(raw[8:]) if compressed else raw
    if len(uncompressed) != struct.unpack_from("<I", uncompressed, 4)[0]:
        raise ValueError("Font file header length does not match contents")
    # SWF RECT: first five bits encode the bit-width of four coordinates.
    rect_bytes = (5 + 4 * (uncompressed[8] >> 3) + 7) // 8
    tag_start = 8 + rect_bytes + 4  # + frame rate and frame count
    result = bytearray(uncompressed[:tag_start])
    pos = tag_start
    modified_font_ids = []

    while pos < len(uncompressed):
        if pos + 2 > len(uncompressed):
            raise ValueError("Truncated SWF tag header")
        hdr = struct.unpack_from("<H", uncompressed, pos)[0]
        tag_id, payload_len = hdr >> 6, hdr & 63
        header_len = 2
        if payload_len == 63:
            if pos + 6 > len(uncompressed):
                raise ValueError("Truncated long SWF tag header")
            payload_len = struct.unpack_from("<I", uncompressed, pos + 2)[0]
            header_len = 6
        tag_end = pos + header_len + payload_len
        if tag_end > len(uncompressed):
            raise ValueError("SWF tag exceeds input length")
        payload = uncompressed[pos + header_len:tag_end]
        font_id = struct.unpack_from("<H", payload)[0] if len(payload) >= 2 else None

        if tag_id == 75 and font_id in CONTROLLER_FONT_IDS:
            updated = replace_glyph_shapes(payload)
            result.extend(struct.pack("<HI", (tag_id << 6) | 63, len(updated)))
            result.extend(updated)
            modified_font_ids.append(font_id)
        else:
            result.extend(uncompressed[pos:tag_end])
        pos = tag_end

    if sorted(modified_font_ids) != list(CONTROLLER_FONT_IDS):
        raise ValueError(f"Wrong controller font IDs found: {modified_font_ids}")
    result[4:8] = struct.pack("<I", len(result))
    if compressed:
        return bytes(result[:8]) + zlib.compress(result[8:], level=9)
    return bytes(result)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gfx", type=Path, required=True,
                        help="Path to the original vanilla fonts_en.gfx")
    parser.add_argument("--swf", type=Path, required=True,
                        help="Path to the original vanilla fonts_en.swf")
    parser.add_argument("--out", type=Path,
                        default=Path(f"dist/Starfield-Creations-PS5-Glyph-Fix-v{VERSION}.zip"),
                        help="Destination mod-manager ZIP")
    args = parser.parse_args()

    builds = {}
    for filename, source in (("fonts_en.gfx", args.gfx), ("fonts_en.swf", args.swf)):
        raw = read_verified(source, filename)
        built = patch_font_file(raw)
        got, expected = sha256(built), TESTED_SHA256[filename]
        if got != expected:
            raise ValueError(f"Built {filename} failed the validated RC1 hash check: {got} != {expected}")
        print(f"PASS  {filename}  {got}")
        builds[filename] = built

    repo_dir = Path(__file__).resolve().parent.parent
    install_readme = (repo_dir / "release" / "README.txt").read_bytes()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    if args.out.exists():
        raise FileExistsError(f"Refusing to overwrite existing output archive: {args.out}")
    with zipfile.ZipFile(args.out, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as package:
        for filename in ("fonts_en.gfx", "fonts_en.swf"):
            package.writestr(f"Interface/{filename}", builds[filename])
        package.writestr("README.txt", install_readme)

    with zipfile.ZipFile(args.out) as check:
        if check.testzip() is not None:
            raise ValueError("Built ZIP failed its CRC check")
        for filename in builds:
            if sha256(check.read(f"Interface/{filename}")) != TESTED_SHA256[filename]:
                raise ValueError(f"Built ZIP contains incorrect {filename}")
    print(f"SUCCESS  Created {args.out}")
    print("Only use these fonts with a legitimate compatible Starfield installation.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, struct.error, zlib.error, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
