# my-game-guides

Self-contained, offline-ready HTML game guides (one standalone file each, under `guides/`).

**`index.html`** is a browsable landing page. It lists every `guides/**/*.html` file with a
**View** (open in browser) and **Download** (save to device) option for each.

Because GitHub Pages serves static files only (no directory listing), the index discovers files
at runtime via the [GitHub git-trees API](https://docs.github.com/en/rest/git/trees)
(`?recursive=1`), filtered to `guides/**/*.html`. Add a guide, commit, and it shows up automatically.

If the API is ever unavailable (rate limit / offline / private), it falls back to the committed
`manifest.json`. Regenerate that fallback whenever guides change:

```bash
python3 -c "import json,glob; open('manifest.json','w').write(json.dumps(sorted(glob.glob('guides/**/*.html', recursive=True)), indent=2)+'\n')"
```
