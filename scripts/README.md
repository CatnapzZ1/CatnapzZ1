# scripts

Generators for the hand-built SVGs used by the profile README. Run `./build.sh` to rebuild all of them.

| Script | Output | Notes |
| --- | --- | --- |
| `title.py` | `assets/title.svg`, `assets/title-dark.svg` | Pixel-font name plus the sleeping cat. Glyphs come from [Ark Pixel Font](https://github.com/TakWolf/ark-pixel-font) (SIL OFL 1.1), which `build.sh` downloads on first run. |
| `cover.py` | `assets/cover.svg` | Embeds `assets/railing.jpg` and adds sakura branches and falling petals. Re-run after replacing the illustration. |
| `sky.py` | `assets/sky.svg` | Pixel clouds, paper plane (`plane.py`) and petals for the left column. |
| `interlude.py` | `assets/interlude.svg` | Wavy staff, pixel notes, divider and the eraser (`eraser.py`). |

Requirements: `python3` with Pillow, and `curl` for the one-time font download.

Palette (sampled from the illustration): `#2f64a6`, `#4b8bd4`, `#88d9ec`, `#c7acbb`.
