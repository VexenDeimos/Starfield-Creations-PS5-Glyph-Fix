# Glyph mapping and verification

The current vanilla English font assets already have PlayStation button outlines. Starfield's Creations Menu requests character slots that, in the vanilla controller fonts, display Xbox symbols.

The fix copies glyph **shapes** within each original DefineFont3 tag while preserving the original mapped character codes and trailing font metrics.

| Requested font character | Reuse glyph from | In-game Creations result |
| --- | --- | --- |
| `A` | `a` | Select – Cross |
| `B` | `b` | Load Order – Triangle |
| `C` | `c` | Purchase Credits – Square |
| `D` | `d` | Back – Circle |
| `G` | `g` | Search – L1 |
| `J` | `j` | Category List – L2 (not L2/R2) |
| `P` | `O` | Options – three-line PS5 Menu/Options symbol |

Each replacement applies to the three controller-font variants, font IDs **6, 7, and 9**, in both files.

All unmentioned glyphs, codepoint positions, and other UI font tags remain unchanged. The fix is global to the shared font symbols; it is **not specific to the Creations Menu at load time**.

## SHA-256 (verified Starfield build)

| File | Vanilla input | Validated patched output |
| --- | --- | --- |
| `fonts_en.gfx` | `f8afad5c8e54ad762200e658a2b7953864a12a04d6e20b9f7e19207836e9e1ce` | `3a2eff307bc24a19b63647dbaa2e1c9572d96a97e37289332e42ed562c89e0a1` |
| `fonts_en.swf` | `76cbfe7dfdaf84fb2019fd7e50f880e1301d0d20cd6dd9b87886e577371356e1` | `609e5ea45d57565f2f9a6d7d63156129a4513a5fdeb46dddb7deea98e4e8c1d1` |

The builder verifies its inputs and outputs against these hashes and refuses other builds instead of producing potentially corrupted font files.

## Validation history

- v0.12 confirmed the correct native DualSense **Circle / Triangle** mapping while preserving the Data menu.
- v0.14 corrected **Cross**, **Square**, and **L1**, and identified the correct combined trigger character slot.
- v0.15 corrected **L2** and the **Options** glyph, with the Data menu's Options prompt still visible. The author confirmed the Creations button bar and ordinary gameplay menus looked correct.

These are observed test results, not a claim of exhaustive controller-mode compatibility. Xbox and Xbox-emulation compatibility still need separate validation.
