# Practical AI Workflows: notes for editing

@VOICE.md

## How the site is built
- Edit the fragments in `src/` and the settings in `build.py`, then run `python3 build.py`. Never edit the built pages at the repo root, `core/`, `topics/`, or `examples/` directly.
- The Resident AI Elective repo imports `build.py` and reads `assets/site.css` and `assets/site.js` at build time. Keep `ICONS`, `icon()`, and the schedule CSS classes intact, and keep page URLs stable. To retire a page, add its path to `REDIRECTS` in `build.py`.
- Prompt blocks use `<div class="exchange">`. Add `<button class="copy-btn" type="button">Copy</button>` inside `.who` for any prompt a reader would reuse.
- The data rules in `src/core/start-here.html` are one person's reading of KU and health system policy. Do not change their substance without the author.
