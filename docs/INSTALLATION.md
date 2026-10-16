# Installation and compatibility

The mod fixes **visual glyphs**. It does not remap controller buttons, install an SFSE plugin, or depend on Starfield Advanced DualSense (SAD).

## Vortex / Mod Organizer 2 (recommended)

1. Build or obtain the compatible mod-manager ZIP.
2. Install that ZIP as a separate optional mod.
3. If another interface mod supplies `fonts_en.gfx` or `fonts_en.swf`, choose which mod's font files should win the conflict. Both files should come from the **same build**.
4. Restart Starfield completely before testing.

## Manual

1. Exit Starfield completely.
2. Back up any files already at `<Starfield install>/Data/Interface/fonts_en.gfx` and `fonts_en.swf`.
3. Place both files from the ZIP's `Interface` folder into `<Starfield install>/Data/Interface/`.
4. Relaunch Starfield and confirm Creations and the Data menu prompts.

To uninstall, disable the mod in your manager; or, if installed manually, remove only the two files you installed, then restore your backups.

## Compatibility

- **Supported/verified:** Directly connected DualSense, DSX off, on the tested Starfield build.
- **Not confirmed:** Xbox controller and Xbox-emulation display behavior; future updates or non-English font variants.
- **Global effect:** These font character replacements are used in other game menus. Xbox players can see PlayStation symbols.
- **Conflicts:** Other replacements for `Interface/fonts_en.gfx` or `Interface/fonts_en.swf`.
- **SAD:** Optional; the original issue exists in the unmodified game.
- **Troubleshooting:** If prompts are missing or incorrect, disable this fix and check for other active font replacements and whether the game was updated.
