#!/usr/bin/env python3
"""Shared HTML ↔ Markdown helpers for the Obsidian content vault."""

from __future__ import annotations

import html as html_mod
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
VAULT = ROOT / "vault"
CHAPTERS_DIR = VAULT / "chapters"
GLOSSARY_DIR = VAULT / "Glossary"

TIP_HTML_RE = re.compile(
    r'<span class="tip" tabindex="0" data-tip="([^"]*)">(.*?)</span>',
    re.S,
)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]")

# Optional short Obsidian aliases → note stem
GLOSSARY_ALIASES = {
    "xrb": "X-ray binaries",
    "xrbs": "X-ray binaries",
    "ce": "common envelope",
    "rlo": "Roche-lobe overflow",
    "rlof": "Roche-lobe overflow",
    "smt": "stable mass transfer",
    "wr": "Wolf-Rayet",
}


def glossary_note_stem(term: str) -> str:
    """Safe note filename stem (no path separators)."""
    stem = term.strip().replace("/", "-").replace(":", " -")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem


def parse_glossary_note(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    aliases: List[str] = []
    body = raw
    title = path.stem
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            fm = raw[3:end]
            body = raw[end + 4 :]
            in_aliases = False
            for line in fm.splitlines():
                if line.strip().startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip("'\"") or title
                    continue
                if line.strip().startswith("aliases:"):
                    in_aliases = True
                    inline = line.split(":", 1)[1].strip()
                    if inline.startswith("["):
                        aliases = [a.strip().strip("'\"") for a in inline.strip("[]").split(",") if a.strip()]
                        in_aliases = False
                    continue
                if in_aliases:
                    if line.strip().startswith("- "):
                        aliases.append(line.strip()[2:].strip().strip("'\""))
                    elif line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                        in_aliases = False

    # strip leading heading
    body = re.sub(r"^\s*#\s+.+\n+", "", body.lstrip())
    tip = re.sub(r"\s+", " ", body).strip()
    return {"path": path, "title": title, "tip": tip, "aliases": aliases}


_GLOSSARY_CACHE: Optional[dict] = None


def load_glossary(force: bool = False) -> dict:
    """Map lookup key (lower) → {title, tip, stem}."""
    global _GLOSSARY_CACHE
    if _GLOSSARY_CACHE is not None and not force:
        return _GLOSSARY_CACHE
    by_key: dict = {}
    if GLOSSARY_DIR.is_dir():
        for path in sorted(GLOSSARY_DIR.glob("*.md")):
            if path.name.startswith("."):
                continue
            note = parse_glossary_note(path)
            if not note["tip"]:
                continue
            entry = {"title": note["title"], "tip": note["tip"], "stem": path.stem}
            keys = {path.stem.lower(), note["title"].lower()}
            for a in note["aliases"]:
                keys.add(a.lower())
            # built-in short aliases pointing at this stem
            for short, target in GLOSSARY_ALIASES.items():
                if target.lower() == path.stem.lower() or target.lower() == note["title"].lower():
                    keys.add(short)
            for k in keys:
                by_key[k] = entry
    _GLOSSARY_CACHE = by_key
    return by_key


def write_glossary_note(term: str, tip: str, aliases: Optional[List[str]] = None) -> Path:
    GLOSSARY_DIR.mkdir(parents=True, exist_ok=True)
    stem = glossary_note_stem(term)
    path = GLOSSARY_DIR / f"{stem}.md"
    alias_list = list(aliases or [])
    # ensure built-in reverse aliases
    for short, target in GLOSSARY_ALIASES.items():
        if target.lower() == term.lower() and short not in [a.lower() for a in alias_list]:
            # prefer canonical casing for known shorts
            pretty = {"xrb": "XrB", "xrbs": "XRBs", "ce": "CE", "rlo": "RLO", "rlof": "RLOF", "smt": "SMT", "wr": "WR"}.get(short, short)
            if pretty not in alias_list:
                alias_list.append(pretty)
    lines = ["---", f'title: "{term}"']
    if alias_list:
        lines.append("aliases:")
        for a in alias_list:
            lines.append(f"  - {a}")
    lines += ["---", "", f"# {term}", "", tip.strip(), ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def tip_wikilink(display: str, tip_text: str = "") -> str:
    """Prefer [[Note]] / [[Note|display]] using glossary notes when possible."""
    gloss = load_glossary()
    entry = gloss.get(display.lower())
    if entry:
        stem = entry["stem"]
        if display == stem or display.lower() == stem.lower():
            return f"[[{stem}]]"
        return f"[[{stem}|{display}]]"
    # fall back to old inline tip syntax if no note yet
    if tip_text:
        return f"[{display}]{{tip: {tip_text}}}"
    return f"[[{display}]]"
ARTICLE_RE = re.compile(
    r'(<article class="chapter" id=")([^"]+)(">)(.*?)(</article>)',
    re.S,
)
HERO_RE = re.compile(
    r'(<header class="hero">)(.*?)(</header>)',
    re.S,
)
FOOTER_RE = re.compile(
    r'(<footer class="site">)(.*?)(</footer>)',
    re.S,
)


def esc(s: str) -> str:
    return html_mod.escape(s, quote=True)


def unescape(s: str) -> str:
    return html_mod.unescape(s)


def html_inline_to_md(s: str) -> str:
    """Convert a fragment with tips/strong/em/sub to vault markdown inline."""
    def tip_to_wiki(m: re.Match) -> str:
        tip = unescape(m.group(1))
        display = _flatten_inline(m.group(2))
        return tip_wikilink(display, tip)

    s = TIP_HTML_RE.sub(tip_to_wiki, s)
    s = re.sub(r"<strong>(.*?)</strong>", r"**\1**", s, flags=re.S)
    s = re.sub(r"<em>(.*?)</em>", r"*\1*", s, flags=re.S)
    s = re.sub(r"<a href=\"([^\"]+)\"[^>]*>(.*?)</a>", r"[\2](\1)", s, flags=re.S)
    s = s.replace("&nbsp;", " ")
    s = s.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    # keep sub/sup as HTML — Obsidian tolerates them
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _flatten_inline(s: str) -> str:
    s = re.sub(r"<[^>]+>", "", s)
    return unescape(re.sub(r"\s+", " ", s)).strip()


TIP_MD_RE = re.compile(r"\[([^\]]+)\]\{tip:\s*([^}]*)\}")
LINK_MD_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def md_inline_to_html(s: str) -> str:
    """Convert vault inline markdown back to site HTML fragment."""
    gloss = load_glossary()

    # Obsidian wikilinks → hover tips when the target is a glossary note
    def wiki_sub(m: re.Match) -> str:
        target = m.group(1).strip()
        # allow Glossary/Term or just Term
        if target.lower().startswith("glossary/"):
            target = target.split("/", 1)[1]
        display = (m.group(2) or target).strip()
        entry = gloss.get(target.lower()) or gloss.get(display.lower())
        if entry and entry["tip"]:
            return f'<span class="tip" tabindex="0" data-tip="{esc(entry["tip"])}">{display}</span>'
        # unresolved wikilink: leave readable plain text
        return display

    s = WIKILINK_RE.sub(wiki_sub, s)

    # Legacy inline tip syntax still supported
    def tip_sub(m: re.Match) -> str:
        term = m.group(1)
        tip = esc(m.group(2).strip())
        return f'<span class="tip" tabindex="0" data-tip="{tip}">{term}</span>'

    s = TIP_MD_RE.sub(tip_sub, s)

    def link_sub(m: re.Match) -> str:
        return f'<a href="{esc(m.group(2))}" target="_blank" rel="noopener">{m.group(1)}</a>'

    s = LINK_MD_RE.sub(link_sub, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    # nbsp for unit gaps like 10 Gyr stays as normal space unless user writes &nbsp;
    s = s.replace(" M☉", "&nbsp;M☉").replace(" km/s", "&nbsp;km/s")
    s = s.replace(" Z☉", "&nbsp;Z☉").replace(" Gyr", "&nbsp;Gyr")
    return s


def wrap_prose_paragraphs(paragraphs: List[str]) -> str:
    parts = ['      <div class="prose">']
    for p in paragraphs:
        inner = md_inline_to_html(p)
        parts.append(f"        <p>\n          {inner}\n        </p>")
    parts.append("      </div>")
    return "\n".join(parts)


@dataclass
class Block:
    kind: str  # prose | callout | timeline | stats | eq | figure
    paragraphs: List[str] = field(default_factory=list)
    title: str = ""
    items: List[Tuple[str, str]] = field(default_factory=list)  # (strong, body) or (n, l)
    text: str = ""
    # figure fields
    figure_id: str = ""
    cap: str = ""
    heading: str = ""
    hint: str = ""


@dataclass
class Chapter:
    id: str
    label: str
    title: str
    blocks: List[Block] = field(default_factory=list)


def extract_inner(tag_html: str, open_pat: str) -> Optional[str]:
    m = re.search(open_pat + r"(.*?)</", tag_html, re.S)
    return m.group(1).strip() if m else None


def parse_article_html(article_inner: str, chapter_id: str) -> Chapter:
    label_m = re.search(r'<p class="ch-label">(.*?)</p>', article_inner, re.S)
    title_m = re.search(r"<h2>(.*?)</h2>", article_inner, re.S)
    ch = Chapter(
        id=chapter_id,
        label=html_inline_to_md(label_m.group(1)) if label_m else chapter_id,
        title=html_inline_to_md(title_m.group(1)) if title_m else "",
    )

    # Walk top-level-ish chunks by splitting on major block opens
    pos = 0
    # skip label + h2
    for m in re.finditer(
        r'<div class="prose">|<div class="callout">|<div class="timeline">|<div class="stat-row">|<p class="eq"[^>]*>|<div class="figure"[^>]*>',
        article_inner,
    ):
        start = m.start()
        if m.group(0).startswith('<div class="prose">'):
            end = article_inner.find("</div>", start) + len("</div>")
            chunk = article_inner[start:end]
            paras = [
                html_inline_to_md(p)
                for p in re.findall(r"<p>(.*?)</p>", chunk, re.S)
            ]
            ch.blocks.append(Block(kind="prose", paragraphs=paras))
        elif m.group(0).startswith('<div class="callout">'):
            end = article_inner.find("</div>", start) + len("</div>")
            chunk = article_inner[start:end]
            inner = re.sub(r'^<div class="callout">|</div>$', "", chunk, flags=re.S).strip()
            # turn <strong>X</strong> into **X**
            text = html_inline_to_md(re.sub(r"\s+", " ", inner))
            ch.blocks.append(Block(kind="callout", text=text))
        elif m.group(0).startswith('<div class="timeline">'):
            end = _find_closing_div(article_inner, start)
            chunk = article_inner[start:end]
            items = []
            for sm in re.finditer(
                r'<div class="step">\s*<strong>(.*?)</strong>\s*<span>(.*?)</span>\s*</div>',
                chunk,
                re.S,
            ):
                items.append((html_inline_to_md(sm.group(1)), html_inline_to_md(sm.group(2))))
            ch.blocks.append(Block(kind="timeline", items=items))
        elif m.group(0).startswith('<div class="stat-row">'):
            end = _find_closing_div(article_inner, start)
            chunk = article_inner[start:end]
            items = []
            for sm in re.finditer(
                r'<div class="stat"><div class="n">(.*?)</div><div class="l">(.*?)</div></div>',
                chunk,
                re.S,
            ):
                items.append((html_inline_to_md(sm.group(1)), html_inline_to_md(sm.group(2))))
            ch.blocks.append(Block(kind="stats", items=items))
        elif m.group(0).startswith('<p class="eq"'):
            end = article_inner.find("</p>", start) + len("</p>")
            chunk = article_inner[start:end]
            inner = re.search(r"<p class=\"eq\"[^>]*>(.*?)</p>", chunk, re.S).group(1)
            ch.blocks.append(Block(kind="eq", text=html_inline_to_md(inner)))
        elif m.group(0).startswith('<div class="figure"'):
            end = _find_closing_div(article_inner, start)
            chunk = article_inner[start:end]
            id_m = re.search(r'id="([^"]+)"', chunk)
            cap = re.search(r'<p class="figure-cap">(.*?)</p>', chunk, re.S)
            heading = re.search(r"<h3>(.*?)</h3>", chunk, re.S)
            hint = re.search(r'<p class="hint">(.*?)</p>', chunk, re.S)
            ch.blocks.append(
                Block(
                    kind="figure",
                    figure_id=id_m.group(1) if id_m else "",
                    cap=html_inline_to_md(cap.group(1)) if cap else "",
                    heading=html_inline_to_md(heading.group(1)) if heading else "",
                    hint=html_inline_to_md(hint.group(1)) if hint else "",
                )
            )
        pos = start
    return ch


def _find_closing_div(s: str, start: int) -> int:
    """Return index just after the matching closing </div> for the div that starts at start."""
    i = s.find("<div", start)
    if i != start:
        # start should point at <div
        pass
    depth = 0
    for m in re.finditer(r"<div\b[^>]*>|</div>", s[start:]):
        token = m.group(0)
        if token.startswith("<div"):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return start + m.end()
    raise ValueError("unbalanced div")


def chapter_to_markdown(ch: Chapter) -> str:
    lines = [
        "---",
        f"id: {ch.id}",
        f'label: "{ch.label}"',
        f'title: "{ch.title}"',
        "---",
        "",
        f"# {ch.title}",
        "",
        f"*{ch.label}*",
        "",
        "> Edit the blocks below. Interactive figure guts stay on the site; only captions / titles / hints sync.",
        "",
    ]
    for b in ch.blocks:
        if b.kind == "prose":
            lines.append(":::prose")
            for i, p in enumerate(b.paragraphs):
                if i:
                    lines.append("")
                lines.append(p)
            lines.append(":::")
            lines.append("")
        elif b.kind == "callout":
            lines.append(":::callout")
            lines.append(b.text)
            lines.append(":::")
            lines.append("")
        elif b.kind == "timeline":
            lines.append(":::timeline")
            for strong, body in b.items:
                lines.append(f"- **{strong}**: {body}")
            lines.append(":::")
            lines.append("")
        elif b.kind == "stats":
            lines.append(":::stats")
            for n, lab in b.items:
                lines.append(f"- {n} | {lab}")
            lines.append(":::")
            lines.append("")
        elif b.kind == "eq":
            lines.append(":::eq")
            lines.append(b.text)
            lines.append(":::")
            lines.append("")
        elif b.kind == "figure":
            lines.append(":::figure")
            if b.figure_id:
                lines.append(f"id: {b.figure_id}")
            lines.append(f"cap: {b.cap}")
            lines.append(f"title: {b.heading}")
            lines.append(f"hint: {b.hint}")
            lines.append(":::")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_chapter_markdown(text: str) -> Chapter:
    fm = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip().strip('"').strip("'")
            body = text[end + 4 :]

    blocks: List[Block] = []
    # strip leading title noise until first :::
    fence_re = re.compile(r":::(\w+)\s*\n(.*?):::", re.S)
    for m in fence_re.finditer(body):
        kind = m.group(1)
        content = m.group(2).strip()
        if kind == "prose":
            paras = [p.strip() for p in re.split(r"\n\s*\n", content) if p.strip()]
            blocks.append(Block(kind="prose", paragraphs=paras))
        elif kind == "callout":
            blocks.append(Block(kind="callout", text=re.sub(r"\s+", " ", content).strip()))
        elif kind == "timeline":
            items = []
            for line in content.splitlines():
                line = line.strip()
                if not line.startswith("-"):
                    continue
                line = line[1:].strip()
                mm = re.match(r"\*\*(.+?)\*\*:\s*(.*)", line)
                if mm:
                    items.append((mm.group(1), mm.group(2)))
            blocks.append(Block(kind="timeline", items=items))
        elif kind == "stats":
            items = []
            for line in content.splitlines():
                line = line.strip()
                if not line.startswith("-"):
                    continue
                line = line[1:].strip()
                if "|" in line:
                    n, lab = line.split("|", 1)
                    items.append((n.strip(), lab.strip()))
            blocks.append(Block(kind="stats", items=items))
        elif kind == "eq":
            blocks.append(Block(kind="eq", text=content.strip()))
        elif kind == "figure":
            meta = {"id": "", "cap": "", "title": "", "hint": ""}
            for line in content.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip().lower()
                    if k in meta:
                        meta[k] = v.strip()
            blocks.append(
                Block(
                    kind="figure",
                    figure_id=meta["id"],
                    cap=meta["cap"],
                    heading=meta["title"],
                    hint=meta["hint"],
                )
            )
    return Chapter(
        id=fm.get("id", "unknown"),
        label=fm.get("label", ""),
        title=fm.get("title", ""),
        blocks=blocks,
    )


def render_block_html(block: Block) -> str:
    if block.kind == "prose":
        return wrap_prose_paragraphs(block.paragraphs)
    if block.kind == "callout":
        return f'      <div class="callout">\n        {md_inline_to_html(block.text)}\n      </div>'
    if block.kind == "timeline":
        lines = ['      <div class="timeline">']
        for strong, body in block.items:
            lines.append("        <div class=\"step\">")
            lines.append(f"          <strong>{md_inline_to_html(strong)}</strong>")
            lines.append(f"          <span>{md_inline_to_html(body)}</span>")
            lines.append("        </div>")
        lines.append("      </div>")
        return "\n".join(lines)
    if block.kind == "stats":
        lines = ['      <div class="stat-row">']
        for n, lab in block.items:
            lines.append(
                f'        <div class="stat"><div class="n">{md_inline_to_html(n)}</div>'
                f'<div class="l">{md_inline_to_html(lab)}</div></div>'
            )
        lines.append("      </div>")
        return "\n".join(lines)
    if block.kind == "eq":
        return (
            '      <p class="eq">\n'
            f"        {md_inline_to_html(block.text)}\n"
            "      </p>"
        )
    raise ValueError(f"cannot render block kind {block.kind}")


def extract_figures(article_inner: str) -> List[str]:
    figs = []
    for m in re.finditer(r'<div class="figure"[^>]*>', article_inner):
        end = _find_closing_div(article_inner, m.start())
        figs.append(article_inner[m.start() : end])
    return figs


def patch_figure_html(fig_html: str, block: Block) -> str:
    out = fig_html
    if block.cap:
        out = re.sub(
            r'(<p class="figure-cap">)(.*?)(</p>)',
            lambda m: m.group(1) + md_inline_to_html(block.cap) + m.group(3),
            out,
            count=1,
            flags=re.S,
        )
    if block.heading:
        out = re.sub(
            r"(<h3>)(.*?)(</h3>)",
            lambda m: m.group(1) + md_inline_to_html(block.heading) + m.group(3),
            out,
            count=1,
            flags=re.S,
        )
    if block.hint:
        out = re.sub(
            r'(<p class="hint">)(.*?)(</p>)',
            lambda m: m.group(1) + md_inline_to_html(block.hint) + m.group(3),
            out,
            count=1,
            flags=re.S,
        )
    return out


def rebuild_article_inner(ch: Chapter, old_inner: str) -> str:
    old_figs = extract_figures(old_inner)
    fig_i = 0
    parts = [
        f'      <p class="ch-label">{md_inline_to_html(ch.label)}</p>',
        f"      <h2>{md_inline_to_html(ch.title)}</h2>",
        "",
    ]
    for b in ch.blocks:
        if b.kind == "figure":
            if fig_i >= len(old_figs):
                raise ValueError(
                    f"Chapter {ch.id}: vault has more :::figure blocks than the site. "
                    "Don't add/remove figures in the vault; only edit cap/title/hint."
                )
            parts.append(patch_figure_html(old_figs[fig_i], b))
            parts.append("")
            fig_i += 1
        else:
            parts.append(render_block_html(b))
            parts.append("")
    if fig_i != len(old_figs):
        raise ValueError(
            f"Chapter {ch.id}: vault has {fig_i} figures but site has {len(old_figs)}. "
            "Keep the same number/order of :::figure blocks."
        )
    return "\n".join(parts).rstrip() + "\n"


def parse_hero_footer_from_html(html: str) -> Tuple[dict, str]:
    hm = HERO_RE.search(html)
    hero = {}
    if hm:
        inner = hm.group(2)
        eye = re.search(r'<p class="eyebrow">(.*?)</p>', inner, re.S)
        h1 = re.search(r"<h1>(.*?)</h1>", inner, re.S)
        lede = re.search(r'<p class="lede">(.*?)</p>', inner, re.S)
        byline = re.search(r'<p class="byline">(.*?)</p>', inner, re.S)
        metas = re.findall(r'<div class="meta-row">\s*(.*?)\s*</div>', inner, re.S)
        meta_spans = re.findall(r"<span>(.*?)</span>", metas[0], re.S) if metas else []
        hero = {
            "eyebrow": html_inline_to_md(eye.group(1)) if eye else "",
            "title": html_inline_to_md(h1.group(1)) if h1 else "",
            "lede": html_inline_to_md(lede.group(1)) if lede else "",
            "byline": html_inline_to_md(byline.group(1)) if byline else "",
            "meta": [html_inline_to_md(x) for x in meta_spans],
        }
    fm = FOOTER_RE.search(html)
    footer = html_inline_to_md(fm.group(2)) if fm else ""
    footer = re.sub(r"\s+", " ", footer).strip()
    return hero, footer


def hero_to_markdown(hero: dict, footer: str) -> str:
    lines = [
        "---",
        "type: home",
        "---",
        "",
        "# Site home / hero",
        "",
        ":::hero",
        f"eyebrow: {hero.get('eyebrow', '')}",
        f"title: {hero.get('title', '')}",
        f"lede: {hero.get('lede', '')}",
        f"byline: {hero.get('byline', '')}",
        "meta:",
    ]
    for m in hero.get("meta", []):
        lines.append(f"  - {m}")
    lines += [":::", "", ":::footer", footer, ":::", ""]
    return "\n".join(lines)


def parse_home_markdown(text: str) -> Tuple[dict, str]:
    hero = {"eyebrow": "", "title": "", "lede": "", "byline": "", "meta": []}
    footer = ""
    hm = re.search(r":::hero\s*\n(.*?):::", text, re.S)
    if hm:
        meta_mode = False
        for line in hm.group(1).splitlines():
            if line.strip() == "meta:":
                meta_mode = True
                continue
            if meta_mode:
                if line.strip().startswith("- "):
                    hero["meta"].append(line.strip()[2:].strip())
                elif line.strip() and not line.startswith(" "):
                    meta_mode = False
            if not meta_mode and ":" in line:
                k, v = line.split(":", 1)
                k = k.strip()
                if k in hero and k != "meta":
                    hero[k] = v.strip()
    fm = re.search(r":::footer\s*\n(.*?):::", text, re.S)
    if fm:
        footer = re.sub(r"\s+", " ", fm.group(1)).strip()
    return hero, footer


def apply_hero_footer(html: str, hero: dict, footer: str) -> str:
    def hero_repl(m: re.Match) -> str:
        meta = "\n".join(f"        <span>{md_inline_to_html(x)}</span>" for x in hero["meta"])
        # rebuild toc from chapters on disk order? keep existing toc links
        toc_m = re.search(r'<nav class="toc">.*?</nav>', m.group(2), re.S)
        toc = toc_m.group(0) if toc_m else '<nav class="toc"></nav>'
        inner = f"""
      <p class="eyebrow">{md_inline_to_html(hero['eyebrow'])}</p>
      <h1>{md_inline_to_html(hero['title'])}</h1>
      <p class="lede">
        {md_inline_to_html(hero['lede'])}
      </p>
      <p class="byline">
        {md_inline_to_html(hero['byline'])}
      </p>
      <div class="meta-row">
{meta}
      </div>
      {toc}
    """
        return m.group(1) + inner + m.group(3)

    html = HERO_RE.sub(hero_repl, html, count=1)
    html = FOOTER_RE.sub(
        lambda m: m.group(1) + "\n      " + md_inline_to_html(footer) + "\n    " + m.group(3),
        html,
        count=1,
    )
    return html
