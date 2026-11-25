# Galactic black holes (POSYDON) — interactive explainer

Browser explainer for [arXiv:2610.07152](https://arxiv.org/abs/2610.07152): natal kicks, binary channels, and seeding remnants into a Milky Way model.

Open `index.html` in a browser, or:

```bash
python3 -m http.server 8765
# → http://127.0.0.1:8765/
```

### Deploy (VPS `rack`)

Live: https://arxiv261007152.piersonl.com/

```bash
./deploy/setup-domain.sh   # once (nginx + TLS)
./deploy/deploy.sh         # after content changes
```

Files land in `/var/www/arxiv261007152` on `rack`.

### Edit copy in Obsidian

Open the `vault/` folder as an Obsidian vault. When prose is ready:

```bash
python3 scripts/apply_vault.py   # vault → index.html
```

To rebuild the vault from the current site (overwrites vault text):

```bash
python3 scripts/export_to_vault.py
```

See `vault/00 Workflow.md` and `MEMORY.md` for conventions.
