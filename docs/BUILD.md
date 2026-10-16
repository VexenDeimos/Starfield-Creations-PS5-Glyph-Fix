# Building from the original game fonts

The build tool uses **only the Python standard library** and original Starfield font files extracted from a legitimate game installation. It does not contact the internet or write to the game installation.

## Prerequisites

- Windows PC with Python 3.8+ (`py -3 --version`)
- Original `fonts_en.gfx` and `fonts_en.swf` from the supported English Starfield `Starfield - Interface.ba2` archive
- A separate BA2 extraction utility; no third-party extraction binaries are included here

Unpack the original files into a temporary folder. Do **not** substitute files supplied by older interface mods. Their hashes and glyph tables can differ significantly.

## Build

From the repository root:

```powershell
py -3 tools/build.py --gfx "C:\Temp\StarfieldOriginal\fonts_en.gfx" --swf "C:\Temp\StarfieldOriginal\fonts_en.swf"
```

Optionally use `--out "C:\Temp\My-Glyph-Fix.zip"` to select the output path.

The builder refuses an existing output ZIP; remove/rename it before rebuilding. It refuses unexpected font hashes, tag layouts, and any output not matching the exact tested binary hashes.

## Output

```
dist/
  Starfield-Creations-PS5-Glyph-Fix-v1.0.0.zip
    Interface/fonts_en.gfx
    Interface/fonts_en.swf
    README.txt
```

The generated archive can be installed with Vortex/MO2, or manually extracted into the game's `Data` directory. The two font files are **byte-for-byte identical** to the author-tested RC1 when built from the supported vanilla originals.

The builder does not modify the original files or extract from BA2 automatically. It does not create an SFSE plugin or rewrite controller bindings.

See [glyph mappings and reference hashes](GLYPH-MAPPING.md) for technical detail.
