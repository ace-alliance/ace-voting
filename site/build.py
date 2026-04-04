#!/usr/bin/env python3
"""Build static site from CIP-136 governance action rationale JSON files."""

import json
import os
import re
import shutil
from pathlib import Path

try:
    from markdown import markdown
except ImportError:
    print("Warning: 'markdown' package not installed. Using plain text.")
    def markdown(text, **kwargs):
        text = re.sub(r'&', '&amp;', text)
        text = re.sub(r'<', '&lt;', text)
        text = re.sub(r'>', '&gt;', text)
        return f'<p>{text}</p>'

REPO_ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SITE_DIR / "templates"
STATIC_DIR = SITE_DIR / "static"
OUTPUT_DIR = REPO_ROOT / "_site"

# For GitHub Pages project sites, the base URL includes the repo name.
# Set to "" for custom domains or org-level sites (user.github.io).
BASE_URL = os.environ.get("BASE_URL", "/ace-voting")

GITHUB_REPO = "https://github.com/ace-alliance/ace-voting"

MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December",
}


def format_month_label(dirname):
    """Convert '202511' to 'November 2025'."""
    year = dirname[:4]
    month = dirname[4:6]
    return f"{MONTH_NAMES.get(month, month)} {year}"


def derive_title(filepath):
    """Derive display title from filename."""
    stem = filepath.stem
    # Strip version suffixes for title
    clean = re.sub(r'(_v\d+|-revised)$', '', stem)
    # Extract GA number and description
    m = re.match(r'(?:ga[_-]?)(\d+)[_-]?(.*)', clean, re.IGNORECASE)
    if m:
        num = m.group(1)
        desc = m.group(2)
        # Handle rationale_xxx.json in mainnet dirs
        if not desc and 'rationale_' in stem:
            desc = stem.split('rationale_', 1)[-1]
        desc = desc.replace('_', ' ').replace('-', ' ').strip().title()
        return f"GA-{num}: {desc}" if desc else f"GA-{num}"
    # Fallback for files like rationale_xxx.json
    if stem.startswith('rationale_'):
        desc = stem.replace('rationale_', '').replace('_', ' ').title()
        return desc
    return stem.replace('_', ' ').replace('-', ' ').title()


def derive_slug(filepath):
    """Create URL slug from filename."""
    stem = filepath.stem.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', stem).strip('-')
    return slug


def derive_ga_number(filepath):
    """Extract numeric GA number for sorting/grouping."""
    m = re.match(r'(?:ga[_-]?)(\d+)', filepath.stem, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Mainnet rationale files - try parent dir
    m = re.match(r'ga[_-]?(\d+)', filepath.parent.name, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return 0


def is_superseded(filepath, all_files_in_dir):
    """Check if this file has been replaced by a newer version."""
    stem = filepath.stem
    ga_num = derive_ga_number(filepath)
    if ga_num == 0:
        return False

    for other in all_files_in_dir:
        if other == filepath:
            continue
        other_num = derive_ga_number(other)
        if other_num != ga_num:
            continue
        other_stem = other.stem
        # The other file is a revision of this one
        if re.search(r'(_v\d+|-revised|_\d{4})$', other_stem) and not re.search(r'(_v\d+|-revised|_\d{4})$', stem):
            return True
        # Or this file is shorter name and other is longer (e.g. ga90_budget_prcess vs ga90_budget_process_2026)
        if len(other_stem) > len(stem) and not re.search(r'(_v\d+|-revised)$', stem):
            return True
    return False


def linkify_uri(uri):
    """Convert IPFS and other URIs to clickable links."""
    if uri.startswith('ipfs://'):
        cid = uri[7:]
        url = f"https://ipfs.io/ipfs/{cid}"
        return f'<a href="{url}">{uri}</a>'
    if uri.startswith('http://') or uri.startswith('https://'):
        return f'<a href="{uri}">{uri}</a>'
    # Plain hash or other - just display
    return f'<code>{uri}</code>'


def gov_action_link(gov_id):
    """Create a link to CardanoScan for a governance action."""
    if gov_id:
        return f'<a href="https://cardanoscan.io/govAction/{gov_id}">{gov_id}</a>'
    return ""


def md(text):
    """Convert Markdown text to HTML."""
    if not text or text.strip().lower() == "none":
        return ""
    return markdown(text, extensions=[])


def discover_rationales():
    """Find all JSON rationale files, return list of (path, month_label, sort_key)."""
    results = []

    # Monthly directories
    for d in sorted(REPO_ROOT.glob("20[0-9][0-9][0-1][0-9]")):
        if not d.is_dir():
            continue
        month_label = format_month_label(d.name)
        sort_key = d.name  # e.g., "202511"
        json_files = list(d.glob("*.json"))
        for f in json_files:
            superseded = is_superseded(f, json_files)
            results.append((f, month_label, sort_key, superseded))

    # Mainnet directory
    mainnet = REPO_ROOT / "mainnet"
    if mainnet.is_dir():
        json_files = list(mainnet.rglob("*.json"))
        for f in json_files:
            results.append((f, "Pre-November 2025", "000000", False))

    return results


def parse_rationale(filepath, month_label, sort_key, superseded):
    """Parse a CIP-136 JSON file into a rationale dict."""
    with open(filepath, 'r', encoding='utf-8') as fh:
        data = json.load(fh)

    body = data.get("body", {})
    iv = body.get("internalVote", {})

    return {
        "gov_action_id": body.get("govActionId", ""),
        "summary": body.get("summary", ""),
        "rationale_statement": body.get("rationaleStatement", ""),
        "precedent": body.get("precedentDiscussion", ""),
        "counterargument": body.get("counterargumentDiscussion", ""),
        "conclusion": body.get("conclusion", ""),
        "vote": {
            "constitutional": iv.get("constitutional", 0),
            "unconstitutional": iv.get("unconstitutional", 0),
            "abstain": iv.get("abstain", 0),
            "didNotVote": iv.get("didNotVote", 0),
            "againstVote": iv.get("againstVote", 0),
        },
        "references": body.get("references", []),
        "authors": [a.get("name", "Ace Alliance") for a in data.get("authors", [{"name": "Ace Alliance"}])],
        "title": derive_title(filepath),
        "slug": derive_slug(filepath),
        "ga_number": derive_ga_number(filepath),
        "month_label": month_label,
        "sort_key": sort_key,
        "superseded": superseded,
        "source_path": str(filepath.relative_to(REPO_ROOT)),
    }


def determine_conclusion_type(conclusion):
    """Determine badge type from conclusion text."""
    lower = conclusion.lower()
    if "unconstitutional" in lower:
        return "unconstitutional"
    if "constitutional" in lower:
        return "constitutional"
    if "abstain" in lower:
        return "abstain"
    return "constitutional"


def render_vote_segments(vote, show_labels=False):
    """Render vote bar segment spans."""
    total = sum(vote.values())
    if total == 0:
        return ""

    segments = []
    for key, cls in [
        ("constitutional", "seg-constitutional"),
        ("unconstitutional", "seg-unconstitutional"),
        ("abstain", "seg-abstain"),
        ("didNotVote", "seg-did-not-vote"),
        ("againstVote", "seg-against"),
    ]:
        val = vote.get(key, 0)
        if val > 0:
            pct = (val / total) * 100
            label = str(val) if show_labels else ""
            segments.append(f'<span class="{cls}" style="width:{pct}%">{label}</span>')

    return "".join(segments)


def render_vote_bar(vote):
    """Render compact vote bar for cards."""
    segments = render_vote_segments(vote)
    if not segments:
        return ""
    return f'<div class="vote-bar">{segments}</div>'


def render_vote_legend(vote):
    """Render vote legend with dots and counts."""
    items = []
    labels = {
        "constitutional": ("Constitutional", "var(--color-constitutional)"),
        "unconstitutional": ("Unconstitutional", "var(--color-unconstitutional)"),
        "abstain": ("Abstain", "var(--color-abstain)"),
        "didNotVote": ("Did Not Vote", "var(--color-did-not-vote)"),
        "againstVote": ("Against", "var(--color-against)"),
    }
    for key, (label, color) in labels.items():
        val = vote.get(key, 0)
        if val > 0:
            items.append(
                f'<span class="legend-item">'
                f'<span class="dot" style="background:{color}"></span>'
                f'{label}: {val}</span>'
            )
    return "".join(items)


def render_card(r):
    """Render a rationale as a card link."""
    badge_type = determine_conclusion_type(r["conclusion"])
    badge_label = badge_type.title()
    badge_html = f'<span class="badge badge-{badge_type}">{badge_label}</span>'
    vote_bar = render_vote_bar(r["vote"])
    superseded_class = " superseded" if r["superseded"] else ""

    return (
        f'<a href="{BASE_URL}/rationales/{r["slug"]}/" class="card{superseded_class}">'
        f'<div class="card-title">{r["title"]}</div>'
        f'<div class="card-summary">{r["summary"]}</div>'
        f'<div class="card-meta">{badge_html}{vote_bar}</div>'
        f'</a>'
    )


def render_references(references):
    """Render references list."""
    if not references:
        return ""
    items = []
    for ref in references:
        label = ref.get("label", "")
        uri = ref.get("uri", "")
        ref_type = ref.get("@type", "Other")
        uri_html = linkify_uri(uri)
        items.append(f'<li><span class="ref-label">{label}</span> ({ref_type})<br><span class="ref-uri">{uri_html}</span></li>')

    return (
        f'<div class="references"><h2>References</h2>'
        f'<ul>{"".join(items)}</ul></div>'
    )


def load_template(name):
    """Load an HTML template."""
    return (TEMPLATES_DIR / name).read_text(encoding='utf-8')


def render_page(title, description, content):
    """Wrap content in the base template."""
    base = load_template("base.html")
    return base.format(
        title=title,
        description=description,
        content=content,
        base_url=BASE_URL,
    )


def build():
    """Main build function."""
    # Clean output
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Copy static files
    static_out = OUTPUT_DIR / "static"
    shutil.copytree(STATIC_DIR, static_out)

    # Discover and parse rationales
    raw = discover_rationales()
    rationales = [parse_rationale(fp, ml, sk, sup) for fp, ml, sk, sup in raw]

    # Sort: by sort_key (month) desc, then ga_number desc
    rationales.sort(key=lambda r: (r["sort_key"], r["ga_number"]), reverse=True)

    # Group by month
    months = {}
    for r in rationales:
        months.setdefault(r["month_label"], []).append(r)

    # --- Index page ---
    active_rationales = [r for r in rationales if not r["superseded"]]
    recent = active_rationales[:5]
    recent_cards = "\n".join(render_card(r) for r in recent)

    month_labels = list(months.keys())
    month_range = str(len(month_labels)) if month_labels else "0"

    index_tmpl = load_template("index.html")
    index_content = index_tmpl.format(
        base_url=BASE_URL,
        total_rationales=len(active_rationales),
        month_range=month_range,
        recent_cards=recent_cards,
    )
    index_html = render_page("Home", "Ace Alliance voting rationales for Cardano governance actions", index_content)
    (OUTPUT_DIR / "index.html").write_text(index_html, encoding='utf-8')

    # --- Browse page ---
    month_sections = []
    for month_label in months:
        cards = "\n".join(render_card(r) for r in months[month_label])
        month_sections.append(f'<h2 class="month-header">{month_label}</h2>\n{cards}')

    browse_tmpl = load_template("browse.html")
    browse_content = browse_tmpl.format(
        month_sections="\n".join(month_sections),
    )
    browse_html = render_page("All Rationales", "Browse all Ace Alliance governance action voting rationales", browse_content)
    rationales_dir = OUTPUT_DIR / "rationales"
    rationales_dir.mkdir(parents=True)
    (rationales_dir / "index.html").write_text(browse_html, encoding='utf-8')

    # --- Individual rationale pages ---
    detail_tmpl = load_template("rationale.html")
    for r in rationales:
        # Prepare content sections
        precedent_html = ""
        if r["precedent"] and r["precedent"].strip().lower() != "none":
            precedent_html = (
                f'<div class="content-section"><h2>Precedent Discussion</h2>'
                f'<div class="body">{md(r["precedent"])}</div></div>'
            )

        counter_html = ""
        if r["counterargument"] and r["counterargument"].strip().lower() != "none":
            counter_html = (
                f'<div class="content-section"><h2>Counterargument Discussion</h2>'
                f'<div class="body">{md(r["counterargument"])}</div></div>'
            )

        detail_content = detail_tmpl.format(
            base_url=BASE_URL,
            title=r["title"],
            gov_action_id_display=gov_action_link(r["gov_action_id"]),
            vote_bar_large=render_vote_segments(r["vote"], show_labels=True),
            vote_legend=render_vote_legend(r["vote"]),
            summary=f'<p>{r["summary"]}</p>',
            rationale_statement=md(r["rationale_statement"]),
            precedent_section=precedent_html,
            counterargument_section=counter_html,
            conclusion=md(r["conclusion"]),
            references_section=render_references(r["references"]),
            source_path=r["source_path"],
        )
        page_html = render_page(r["title"], r["summary"][:160], detail_content)

        page_dir = rationales_dir / r["slug"]
        page_dir.mkdir(parents=True, exist_ok=True)
        (page_dir / "index.html").write_text(page_html, encoding='utf-8')

    print(f"Built {len(rationales)} rationale pages to {OUTPUT_DIR}")
    print(f"  Active: {len(active_rationales)}, Superseded: {len(rationales) - len(active_rationales)}")


if __name__ == "__main__":
    build()
