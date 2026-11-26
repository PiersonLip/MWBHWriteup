#!/usr/bin/env python3
"""Shared HTML ↔ Markdown helpers for the Obsidian content vault."""

from __future__ import annotations

import html as html_mod
import re
import sys
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
# Display alias stops at | or ]; stray trailing pipes in vault links are ignored
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]|]*))?\|*\]\]")

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
    deep = ""
    effect = ""
    image = ""
    viz = ""
    tip_fm = ""
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
                if line.strip().startswith("deep:"):
                    deep = line.split(":", 1)[1].strip().strip("'\"")
                    continue
                if line.strip().startswith("effect:"):
                    effect = line.split(":", 1)[1].strip().strip("'\"")
                    continue
                if line.strip().startswith("image:"):
                    image = line.split(":", 1)[1].strip().strip("'\"")
                    continue
                if line.strip().startswith("viz:"):
                    viz = line.split(":", 1)[1].strip().strip("'\"")
                    continue
                if line.strip().startswith("tip:"):
                    tip_fm = line.split(":", 1)[1].strip().strip("'\"")
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
    # [[Note|display]] / [[Note]] → plain words so nested tip linkify works
    def _wiki_plain(m: re.Match) -> str:
        return ((m.group(2) if m.group(2) is not None else m.group(1)) or "").strip().strip("|").strip()

    deep_md = ""
    if deep:
        # Short hover teaser: frontmatter tip: …, else first paragraph
        if tip_fm:
            tip = tip_fm
            deep_md = body.strip()
        else:
            parts = re.split(r"\n\s*\n", body.strip(), maxsplit=1)
            tip = WIKILINK_RE.sub(_wiki_plain, parts[0])
            tip = re.sub(r"\s+", " ", tip).strip()
            deep_md = parts[1].strip() if len(parts) > 1 else ""
    else:
        tip = tip_fm or WIKILINK_RE.sub(_wiki_plain, body)
        tip = re.sub(r"\s+", " ", tip).strip()
    return {
        "path": path,
        "title": title,
        "tip": tip,
        "aliases": aliases,
        "deep": deep,
        "deep_md": deep_md,
        "effect": effect,
        "image": image,
        "viz": viz,
    }


ORBIT_VIZ_HTML = """\
          <div class="deep-viz" data-orbit-viz>
            <canvas id="binary-orbit-canvas" width="640" height="640" aria-label="Two stars orbiting a shared center of mass"></canvas>
            <span class="deep-viz-caption">Unequal-mass binary · shared center of mass</span>
          </div>"""

ORION_VIZ_HTML = """\
          <figure class="deep-orion" data-orion-viz aria-label="Orion constellation — gold stars are known binaries or multiples; hover for details">
            <canvas id="orion-binary-canvas" width="800" height="800" aria-hidden="true"></canvas>
            <div class="deep-orion-tip" id="orion-tip" hidden></div>
          </figure>"""


def render_deep_note_html(md: str, deep_id: str = "note") -> str:
    """Render a deep-note markdown body into `.deep-copy` HTML.

    Supports paragraphs, ### headings, **bold**/*em*/wikilinks via md_inline_to_html,
    placeholders {{orbit-viz}} / {{orion-viz}}, and Obsidian footnotes.
    The first paragraph becomes <p class="deep-pull">.
    """
    text = (md or "").strip()
    if not text:
        return ""
    footnotes = {}
    for m in FN_DEF_MD_RE.finditer(text):
        footnotes[m.group(1)] = m.group(2).strip()
    text = FN_DEF_MD_RE.sub("", text).strip()
    begin_footnotes(deep_id, footnotes)
    try:
        blocks = re.split(r"\n\s*\n", text)
        out: List[str] = []
        first_para = True
        for raw_block in blocks:
            block = raw_block.strip()
            if not block:
                continue
            if block in ("{{orbit-viz}}", "{{orbit viz}}"):
                out.append(ORBIT_VIZ_HTML)
                first_para = False
                continue
            if block in ("{{orion-viz}}", "{{orion viz}}"):
                out.append(ORION_VIZ_HTML)
                first_para = False
                continue
            heading = re.match(r"^(#{2,3})\s+(.+)$", block, re.S)
            if heading and "\n" not in block.strip():
                level = len(heading.group(1))
                title = md_inline_to_html(heading.group(2).strip())
                out.append(f"          <h{level}>{title}</h{level}>")
                first_para = False
                continue
            # Multi-line block starting with heading then text → split
            hm = re.match(r"^(#{2,3})\s+(.+?)\n+([\s\S]+)$", block)
            if hm:
                level = len(hm.group(1))
                title = md_inline_to_html(hm.group(2).strip())
                out.append(f"          <h{level}>{title}</h{level}>")
                para = md_inline_to_html(re.sub(r"\s+", " ", hm.group(3).strip()))
                out.append(f"          <p>\n            {para}\n          </p>")
                first_para = False
                continue
            para = md_inline_to_html(re.sub(r"\s*\n\s*", " ", block).strip())
            cls = ' class="deep-pull"' if first_para else ""
            out.append(
                f"          <p{cls}>{para}</p>"
                if first_para
                else f"          <p>\n            {para}\n          </p>"
            )
            first_para = False
        body = "\n".join(out)
        state = end_footnotes()
        if state and state.order:
            # Slightly tighter indent so it sits cleanly inside .deep-copy
            fn = render_footnotes_html(state)
            fn = "\n".join(("          " + line if line.strip() else line) for line in fn.splitlines())
            body = f"{body}\n{fn}"
        return body
    except Exception:
        end_footnotes()
        raise


def apply_deep_notes(html: str) -> str:
    """Inject vault deep-note prose into each `.deep-body[data-deep-id]` copy block."""
    notes = []
    if GLOSSARY_DIR.is_dir():
        for path in sorted(GLOSSARY_DIR.glob("*.md")):
            if path.name.startswith("."):
                continue
            note = parse_glossary_note(path)
            if note.get("deep") and note.get("deep_md"):
                notes.append(note)
    if not notes:
        return html

    for note in notes:
        deep_id = note["deep"]
        copy_html = render_deep_note_html(note["deep_md"], deep_id=deep_id)
        if not copy_html:
            continue
        # Replace .deep-copy inside the matching deep-body
        pattern = re.compile(
            rf'(<div class="deep-body" data-deep-id="{re.escape(deep_id)}"\s*>\s*'
            rf'<div class="deep-copy">)([\s\S]*?)(</div>\s*</div>)',
            re.M,
        )

        def repl(m: re.Match, _copy=copy_html) -> str:
            return f"{m.group(1)}\n{_copy}\n        {m.group(3)}"

        new_html, n = pattern.subn(repl, html, count=1)
        if n:
            html = new_html
            title = note.get("title") or deep_id
            pretty = (title[:1].upper() + title[1:]) if title else "Note"
            html = re.sub(
                r'(<h2 id="deep-title">)[^<]*(</h2>)',
                rf"\g<1>{esc(pretty)}\g<2>",
                html,
                count=1,
            )
        else:
            print(f"warn: no deep-body for deep id {deep_id!r}", file=sys.stderr)
    return html


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
            # Allow image/viz/deep-only notes (empty tip body)
            if not (
                note["tip"]
                or note.get("image")
                or note.get("viz")
                or note.get("deep")
                or note.get("effect")
            ):
                continue
            entry = {
                "title": note["title"],
                "tip": note["tip"],
                "stem": path.stem,
                "deep": note.get("deep") or "",
                "effect": note.get("effect") or "",
                "image": note.get("image") or "",
                "viz": note.get("viz") or "",
            }
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
    s = FN_REF_HTML_RE.sub(lambda m: f"[^{m.group(1)}]", s)
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

    # Inline Obsidian footnotes ^[text] → numbered refs
    def inline_fn_sub(m: re.Match) -> str:
        if not _FN:
            return m.group(0)
        fid, num = _FN.add_inline(m.group(1))
        cid = fn_slug(_FN.chapter_id)
        sid = fn_slug(fid)
        return (
            f'<sup class="fn-ref" id="fnref-{cid}-{sid}" data-fn-id="{esc(fid)}">'
            f'<a href="#fn-{cid}-{sid}">{num}</a></sup>'
        )

    s = FN_INLINE_MD_RE.sub(inline_fn_sub, s)

    # Reference footnotes [^id]
    def ref_fn_sub(m: re.Match) -> str:
        if not _FN:
            return m.group(0)
        fid = m.group(1)
        num = _FN.mark_used(fid)
        cid = fn_slug(_FN.chapter_id)
        sid = fn_slug(fid)
        return (
            f'<sup class="fn-ref" id="fnref-{cid}-{sid}" data-fn-id="{esc(fid)}">'
            f'<a href="#fn-{cid}-{sid}">{num}</a></sup>'
        )

    s = FN_REF_MD_RE.sub(ref_fn_sub, s)

    # Markdown links on pure md BEFORE wikilinks become HTML (or link_sub
    # would rewrite [label](url) inside data-tip="..." attributes).
    def link_sub(m: re.Match) -> str:
        return f'<a href="{esc(m.group(2))}" target="_blank" rel="noopener">{m.group(1)}</a>'

    s = LINK_MD_RE.sub(link_sub, s)

    # Obsidian wikilinks → hover tips when the target is a glossary note
    def wiki_sub(m: re.Match) -> str:
        target = m.group(1).strip()
        # allow Glossary/Term or just Term
        if target.lower().startswith("glossary/"):
            target = target.split("/", 1)[1]
        display = (m.group(2) or target).strip()
        entry = gloss.get(target.lower()) or gloss.get(display.lower())
        if entry and (
            entry["tip"]
            or entry.get("image")
            or entry.get("viz")
            or entry.get("deep")
            or entry.get("effect")
        ):
            deep = entry.get("deep") or ""
            effect = entry.get("effect") or ""
            image = entry.get("image") or ""
            viz = entry.get("viz") or ""
            deep_attr = f' data-deep="{esc(deep)}"' if deep else ""
            effect_attr = f' data-effect="{esc(effect)}"' if effect else ""
            image_attr = f' data-image="{esc(image)}"' if image else ""
            viz_attr = f' data-viz="{esc(viz)}"' if viz else ""
            cls = "tip tip-deep" if deep else "tip"
            if image:
                cls += " tip-image"
            if viz:
                cls += " tip-viz"
            return (
                f'<span class="{cls}" tabindex="0" data-tip="{esc(entry["tip"])}"'
                f"{deep_attr}{effect_attr}{image_attr}{viz_attr}>{display}</span>"
            )
        # unresolved wikilink: leave readable plain text
        return display

    s = WIKILINK_RE.sub(wiki_sub, s)

    # Legacy inline tip syntax still supported
    def tip_sub(m: re.Match) -> str:
        term = m.group(1)
        tip = esc(m.group(2).strip())
        return f'<span class="tip" tabindex="0" data-tip="{tip}">{term}</span>'

    s = TIP_MD_RE.sub(tip_sub, s)

    # Bold/italic for prose only — keep **…** inside data-tip="…" for tip renderer
    tip_holders: List[str] = []

    def _stash_data_tip(m: re.Match) -> str:
        tip_holders.append(m.group(0))
        return f"\x00TIPHOLD{len(tip_holders) - 1}\x00"

    s = re.sub(r'data-tip="[^"]*"', _stash_data_tip, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    for i, held in enumerate(tip_holders):
        s = s.replace(f"\x00TIPHOLD{i}\x00", held)
    # nbsp for unit gaps like 10 Gyr stays as normal space unless user writes &nbsp;
    s = s.replace(" M☉", "&nbsp;M☉").replace(" km/s", "&nbsp;km/s")
    s = s.replace(" Z☉", "&nbsp;Z☉").replace(" Gyr", "&nbsp;Gyr")
    return s


def render_footnotes_html(state: FootnoteState) -> str:
    if not state.order:
        return ""
    global _FN
    saved = _FN
    _FN = None  # footnote bodies shouldn't spawn new footnotes
    cid = state.chapter_id
    lines = [
        f'      <section class="footnotes" id="footnotes-{fn_slug(cid)}">',
        "        <h3>Notes</h3>",
        "        <ol>",
    ]
    try:
        cid_s = fn_slug(cid)
        for i, fid in enumerate(state.order, start=1):
            text = state.defs.get(fid, "")
            body = md_inline_to_html(text) if text else ""
            sid = fn_slug(fid)
            lines.append(
                f'          <li id="fn-{cid_s}-{sid}" value="{i}" data-fn-id="{esc(fid)}">'
                f'<span class="fn-text">{body}</span> '
                f'<a href="#fnref-{cid_s}-{sid}" class="fn-back" title="Back to text">↩</a>'
                f"</li>"
            )
    finally:
        _FN = saved
    lines += ["        </ol>", "      </section>", ""]
    return "\n".join(lines)


def extract_footnotes_from_html(article_inner: str) -> dict:
    """Pull footnote id → text from a chapter footnotes section."""
    defs = {}
    sec = FN_SECTION_HTML_RE.search(article_inner)
    if not sec:
        return defs
    for m in re.finditer(
        r'<li[^>]*data-fn-id="([^"]+)"[^>]*>\s*<span class="fn-text">(.*?)</span>',
        sec.group(0),
        re.S,
    ):
        defs[unescape(m.group(1))] = html_inline_to_md(m.group(2))
    return defs


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
    footnotes: dict = field(default_factory=dict)  # id -> markdown text


class FootnoteState:
    """Per-chapter footnote render state (appearance order → numbers)."""

    def __init__(self, chapter_id: str, defs: Optional[dict] = None):
        self.chapter_id = chapter_id or "ch"
        self.defs = dict(defs or {})
        self.order: List[str] = []  # ids in first-appearance order
        self._inline_i = 0

    def ensure(self, fid: str, text: str = "") -> None:
        if text and fid not in self.defs:
            self.defs[fid] = text
        if fid not in self.order and fid in self.defs:
            self.order.append(fid)

    def mark_used(self, fid: str) -> int:
        if fid not in self.defs:
            self.defs[fid] = ""
        if fid not in self.order:
            self.order.append(fid)
        return self.order.index(fid) + 1

    def add_inline(self, text: str) -> Tuple[str, int]:
        self._inline_i += 1
        fid = f"inline-{self._inline_i}"
        self.defs[fid] = text.strip()
        self.order.append(fid)
        return fid, len(self.order)


_FN: Optional[FootnoteState] = None


def begin_footnotes(chapter_id: str, defs: Optional[dict] = None) -> FootnoteState:
    global _FN
    _FN = FootnoteState(chapter_id, defs)
    return _FN


def end_footnotes() -> Optional[FootnoteState]:
    global _FN
    state = _FN
    _FN = None
    return state


FN_REF_MD_RE = re.compile(r"\[\^([^\]]+)\]")
FN_INLINE_MD_RE = re.compile(r"\^\[([^\]]+)\]")
FN_DEF_MD_RE = re.compile(r"(?m)^\[\^([^\]]+)\]:\s*(.+)$")
FN_REF_HTML_RE = re.compile(
    r'<sup class="fn-ref"[^>]*data-fn-id="([^"]+)"[^>]*>.*?</sup>',
    re.S,
)
FN_SECTION_HTML_RE = re.compile(
    r'<section class="footnotes"[^>]*>.*?</section>',
    re.S,
)


def fn_slug(s: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", s).strip("-") or "note"


def extract_inner(tag_html: str, open_pat: str) -> Optional[str]:
    m = re.search(open_pat + r"(.*?)</", tag_html, re.S)
    return m.group(1).strip() if m else None


def parse_article_html(article_inner: str, chapter_id: str) -> Chapter:
    footnotes = extract_footnotes_from_html(article_inner)
    article_inner = FN_SECTION_HTML_RE.sub("", article_inner)

    label_m = re.search(r'<p class="ch-label">(.*?)</p>', article_inner, re.S)
    title_m = re.search(r"<h2>(.*?)</h2>", article_inner, re.S)
    ch = Chapter(
        id=chapter_id,
        label=html_inline_to_md(label_m.group(1)) if label_m else chapter_id,
        title=html_inline_to_md(title_m.group(1)) if title_m else "",
        footnotes=footnotes,
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
    if ch.footnotes:
        lines.append("")
        for fid, text in ch.footnotes.items():
            lines.append(f"[^{fid}]: {text}")
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

    # Collect Obsidian footnote definitions ([^id]: text)
    footnotes = {}
    for m in FN_DEF_MD_RE.finditer(body):
        footnotes[m.group(1)] = m.group(2).strip()
    body_wo_defs = FN_DEF_MD_RE.sub("", body)

    blocks: List[Block] = []
    # strip leading title noise until first :::
    fence_re = re.compile(r":::(\w+)\s*\n(.*?):::", re.S)
    for m in fence_re.finditer(body_wo_defs):
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
        footnotes=footnotes,
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
    old_inner = FN_SECTION_HTML_RE.sub("", old_inner)
    old_figs = extract_figures(old_inner)
    fig_i = 0
    begin_footnotes(ch.id, ch.footnotes)
    parts = [
        f'      <p class="ch-label">{md_inline_to_html(ch.label)}</p>',
        f"      <h2>{md_inline_to_html(ch.title)}</h2>",
        "",
    ]
    try:
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
        state = end_footnotes()
        if state:
            # keep used footnotes on the chapter for export round-trips
            ch.footnotes = {fid: state.defs.get(fid, "") for fid in state.order}
            fn_html = render_footnotes_html(state)
            if fn_html:
                parts.append(fn_html)
    except Exception:
        end_footnotes()
        raise
    return "\n".join(parts).rstrip() + "\n"


def parse_hero_footer_from_html(html: str) -> Tuple[dict, str]:
    hm = HERO_RE.search(html)
    hero = {}
    if hm:
        inner = hm.group(2)
        eye = re.search(r'<p class="eyebrow">(.*?)</p>', inner, re.S)
        h1 = re.search(r"<h1>(.*?)</h1>", inner, re.S)
        lede = re.search(r'<p class="lede">(.*?)</p>', inner, re.S)
        byline = re.search(r'<p class="byline(?![-\w])[^"]*">(.*?)</p>', inner, re.S)
        written = re.search(r'<p class="byline byline-author">(.*?)</p>', inner, re.S)
        metas = re.findall(r'<div class="meta-row">\s*(.*?)\s*</div>', inner, re.S)
        meta_spans = re.findall(r"<span>(.*?)</span>", metas[0], re.S) if metas else []
        hero = {
            "eyebrow": html_inline_to_md(eye.group(1)) if eye else "",
            "title": html_inline_to_md(h1.group(1)) if h1 else "",
            "lede": html_inline_to_md(lede.group(1)) if lede else "",
            "byline": html_inline_to_md(byline.group(1)) if byline else "",
            "written": html_inline_to_md(written.group(1)) if written else "",
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
    ]
    if hero.get("written"):
        lines.append(f"written: {hero['written']}")
    lines.append("meta:")
    for m in hero.get("meta", []):
        lines.append(f"  - {m}")
    lines += [":::", "", ":::footer", footer, ":::", ""]
    return "\n".join(lines)


def parse_home_markdown(text: str) -> Tuple[dict, str]:
    hero = {"eyebrow": "", "title": "", "lede": "", "byline": "", "written": "", "meta": []}
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
        # Preserve theme picker + toc; only rebuild eyebrow/title/lede/byline/meta
        toc_m = re.search(r'<nav class="toc">.*?</nav>', m.group(2), re.S)
        toc = toc_m.group(0) if toc_m else '<nav class="toc"></nav>'
        theme_m = re.search(
            r'<div class="theme-picker"[^>]*>.*?</div>',
            m.group(2),
            re.S,
        )
        theme = theme_m.group(0) if theme_m else ""
        meta_block = ""
        if hero.get("meta"):
            meta = "\n".join(f"        <span>{md_inline_to_html(x)}</span>" for x in hero["meta"])
            meta_block = f'      <div class="meta-row">\n{meta}\n      </div>\n'
        theme_block = f"      {theme}\n" if theme else ""
        written = (hero.get("written") or "").strip()
        written_block = (
            f'      <p class="byline byline-author">\n        {md_inline_to_html(written)}\n      </p>\n'
            if written
            else ""
        )
        inner = f"""
      <p class="eyebrow">{md_inline_to_html(hero['eyebrow'])}</p>
      <h1>{md_inline_to_html(hero['title'])}</h1>
      <p class="lede">
        {md_inline_to_html(hero['lede'])}
      </p>
      <p class="byline">
        {md_inline_to_html(hero['byline'])}
      </p>
{written_block}{meta_block}{theme_block}      {toc}
    """
        return m.group(1) + inner + m.group(3)

    html = HERO_RE.sub(hero_repl, html, count=1)
    html = FOOTER_RE.sub(
        lambda m: m.group(1) + "\n      " + md_inline_to_html(footer) + "\n    " + m.group(3),
        html,
        count=1,
    )
    return html


FIGURES_DIR = VAULT / "figures"
FLOW_PATHS_NOTE = FIGURES_DIR / "flow-paths.md"

# Channel ids used by the #flow flowchart detail panel
FLOW_PATH_IDS = (
    "merger",
    "disrupt",
    "single",
    "bhstar-m",
    "dco-m",
    "bhbh",
    "otherbin",
)

FLOW_PATH_TITLES = {
    "merger": "Stellar mergers",
    "disrupt": "Disrupted binaries",
    "single": "Initially single",
    "bhstar-m": "BH+star mergers",
    "dco-m": "DCO mergers",
    "bhbh": "Detached BH-BH",
    "otherbin": "BH + other",
}

CHANNEL_DETAIL_RE = re.compile(
    r'id:\s*"(?P<id>[^"]+)"[\s\S]*?detail:\s*"(?P<detail>(?:\\.|[^"\\])*)"',
    re.M,
)


def _js_unescape(s: str) -> str:
    return (
        s.replace("\\n", "\n")
        .replace('\\"', '"')
        .replace("\\\\", "\\")
    )


def _js_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def _channels_array_span(html: str):
    """Return (start, end) indices of the `const channels = [ ... ];` block, or None."""
    m = re.search(r"const channels\s*=\s*\[", html)
    if not m:
        return None
    start = m.start()
    i = m.end() - 1  # at '['
    depth = 0
    for j in range(i, len(html)):
        ch = html[j]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                # include trailing ];
                end = j + 1
                if end < len(html) and html[end] == ";":
                    end += 1
                return start, end
    return None


def extract_flow_path_details(html: str) -> dict:
    """Pull channel id → detail blurb from the JS `channels` array."""
    span = _channels_array_span(html)
    if not span:
        return {}
    chunk = html[span[0] : span[1]]
    out = {}
    for m in CHANNEL_DETAIL_RE.finditer(chunk):
        cid = m.group("id")
        if cid in FLOW_PATH_IDS:
            out[cid] = _js_unescape(m.group("detail")).strip()
    return out


def parse_flow_paths_markdown(text: str) -> dict:
    """Parse vault/figures/flow-paths.md → {channel_id: detail}."""
    details = {}
    # Headings: "## single" or "## single · Initially single"
    parts = re.split(r"^##\s+(\S+)(?:\s*[·—-]\s*.+)?\s*$", text, flags=re.M)
    for i in range(1, len(parts), 2):
        cid = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if not body:
            continue
        paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
        # Skip a sole italic title line (*Stellar mergers*)
        while paras and re.fullmatch(r"\*[^*]+\*", paras[0]):
            paras = paras[1:]
        if not paras:
            continue
        para = paras[0]
        para = WIKILINK_RE.sub(
            lambda m: ((m.group(2) if m.group(2) is not None else m.group(1)) or "").strip(),
            para,
        )
        para = re.sub(r"\*\*(.+?)\*\*", r"\1", para)
        para = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\1", para)
        para = re.sub(r"\s+", " ", para).strip()
        if para:
            details[cid] = para
    return details


def flow_paths_to_markdown(details: dict) -> str:
    lines = [
        "---",
        "figure: flow",
        "---",
        "",
        "# Flowchart path blurbs",
        "",
        "These show in the **How do Galactic black holes form?** detail panel when you click a path.",
        "Edit the paragraph under each heading, then run `python3 scripts/apply_vault.py`.",
        "",
    ]
    for cid in FLOW_PATH_IDS:
        title = FLOW_PATH_TITLES.get(cid, cid)
        lines.append(f"## {cid} · {title}")
        lines.append("")
        lines.append(details.get(cid, "").strip() or "_TODO: path blurb_")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def apply_flow_path_details(html: str, details: dict) -> str:
    """Patch `detail: "..."` strings in the JS channels array."""
    if not details:
        return html
    span = _channels_array_span(html)
    if not span:
        return html
    a, b = span
    chunk = html[a:b]
    out = []
    last = 0
    n = 0
    for m in CHANNEL_DETAIL_RE.finditer(chunk):
        cid = m.group("id")
        out.append(chunk[last : m.start("detail")])
        if cid in details:
            out.append(_js_escape(details[cid]))
            n += 1
        else:
            out.append(m.group("detail"))
        out.append('"')
        last = m.end()
    out.append(chunk[last:])
    if not n:
        return html
    return html[:a] + "".join(out) + html[b:]


VAULT_GLOSSARY_RE = re.compile(
    r"(const VAULT_GLOSSARY\s*=\s*)/\*VAULT_GLOSSARY\*/[\s\S]*?/\*END_VAULT_GLOSSARY\*/(\s*;)",
    re.M,
)


def build_vault_glossary_payload() -> dict:
    """All glossary notes keyed for nested tip seeding (tip/effect/image/viz/deep)."""
    gloss = load_glossary(force=True)
    payload: dict = {}
    for key, entry in gloss.items():
        item = {"tip": entry.get("tip") or ""}
        if entry.get("effect"):
            item["effect"] = entry["effect"]
        if entry.get("image"):
            item["image"] = entry["image"]
        if entry.get("viz"):
            item["viz"] = entry["viz"]
        if entry.get("deep"):
            item["deep"] = entry["deep"]
        payload[key] = item
    return payload


def apply_vault_glossary_json(html: str) -> str:
    """Inject vault glossary tip text into the VAULT_GLOSSARY JS object."""
    import json

    payload = build_vault_glossary_payload()
    body = json.dumps(payload, ensure_ascii=False, indent=2)

    def repl(m: re.Match) -> str:
        return f"{m.group(1)}/*VAULT_GLOSSARY*/{body}/*END_VAULT_GLOSSARY*/{m.group(2)}"

    new_html, n = VAULT_GLOSSARY_RE.subn(repl, html, count=1)
    if n == 0:
        raise ValueError(
            "VAULT_GLOSSARY marker not found in index.html — expected "
            "const VAULT_GLOSSARY = /*VAULT_GLOSSARY*/{...}/*END_VAULT_GLOSSARY*/;"
        )
    return new_html
