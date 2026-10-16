# Starfield Creations – PS5 Glyph Fix

A standalone **Starfield (PC)** interface fix that replaces incorrect Xbox-style controller prompts in the **Creations Menu** with proper **PS5 / DualSense glyphs**.

This fix is also intended as an optional download on the **Starfield Advanced DualSense (SAD)** Nexus Mods page. **SAD is not required.** These incorrect prompts occur in the vanilla game; SAD does not cause them.

## Corrected buttons

| Creations action | PS5 symbol |
| --- | --- |
| Category List | L2 |
| Search | L1 |
| Load Order | Triangle |
| Options | PS5 Menu / Options (three lines) |
| Purchase Credits | Square |
| Select | Cross |
| Back | Circle |

**Visual changes only.** No input remapping, hooks, SFSE dependency, changes to `Starfield.exe`, or modifications to the game's BA2 archives.

## Status

The glyph mapping has been **verified in-game** with a directly connected DualSense, DSX disabled. The author also checked the **Data menu** and normal in-game menus, including the Options glyph that was missing in an earlier test.

The original tested release-candidate font files match the exact SHA-256 values in [docs/GLYPH-MAPPING.md](docs/GLYPH-MAPPING.md).

## Build your own installable ZIP

**No Bethesda game assets are included in this source repository.** A reproducible Python builder copies existing glyph shapes **from the user's own vanilla font files** and generates the tested mod using only Python's standard library.

1. Obtain `fonts_en.gfx` and `fonts_en.swf` from a **legitimate copy** of the supported Starfield build (`Starfield - Interface.ba2`). Use a compatible BA2 extraction utility. Do not use the output of another font mod.
2. Install Python 3.8 or newer.
3. From this repository, run:

   ```powershell
   py -3 tools/build.py --gfx "C:\path\to\vanilla\fonts_en.gfx" --swf "C:\path\to\vanilla\fonts_en.swf"
   ```

4. The validated mod-manager archive is generated at `dist/Starfield-Creations-PS5-Glyph-Fix-v1.0.0.zip`.

The builder **refuses to patch an unknown game build**, checks the resulting font hashes against the in-game-tested RC1, and does **not** change the originals. See [build instructions](docs/BUILD.md).

## Installation

Install the generated ZIP using **Vortex** or **Mod Organizer 2**, or manually place `Interface/fonts_en.gfx` and `Interface/fonts_en.swf` under your game's `Data` folder. Restart Starfield completely. Back up preexisting loose fonts before manual installation. See the [installation and compatibility guide](docs/INSTALLATION.md).

## Compatibility warning

**These are shared font assets.** The patched entries also affect other game menus, **not just Creations**. An Xbox controller or Xbox-emulation setup may display PlayStation symbols, and other mods that provide `fonts_en.gfx` or `fonts_en.swf` will conflict. Only the documented vanilla English fonts have been verified, so do not force the patch onto a later or different game version.

## Technical details

See [glyph-mapping notes](docs/GLYPH-MAPPING.md) for the seven mappings, unchanged menu behavior, font IDs, and source/output hashes.

## Credits and disclaimer

Created and tested by **VexenDeimos**. Starfield and the original font graphics are property of Bethesda Softworks / Bethesda Game Studios; PlayStation and DualSense are trademarks of their respective owners. This unofficial project is not sponsored, endorsed, or supported by Bethesda, Sony, or Microsoft.

The source repository does not grant permission to redistribute Bethesda's original or modified game binaries. Please verify the relevant permissions before posting standalone binaries elsewhere.
