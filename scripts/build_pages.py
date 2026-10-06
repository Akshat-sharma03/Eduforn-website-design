#!/usr/bin/env python3
"""Prepare the static Eduforn site for GitHub Pages without editing source files."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist" / "github-pages"
WEB_EXTENSIONS = {".html", ".css", ".js", ".webmanifest", ".xml"}
ROOT_PATH_LITERAL = re.compile(r"(?P<quote>[\"'`])/(?!/)")


def deployment_base(explicit: str | None) -> str:
    value = explicit
    if value is None:
        value = os.environ.get("PAGES_BASE_PATH") or None
    if value is None:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if "/" in repository:
            owner, name = repository.split("/", 1)
            value = "" if name.casefold() == f"{owner}.github.io".casefold() else name
        else:
            value = ""

    value = value.strip()
    if value in {"", "/"}:
        return ""
    if ".." in value or "?" in value or "#" in value:
        raise ValueError("Base path must be a simple repository path, for example /Eduforn-website-design/")
    return "/" + value.strip("/") + "/"


def ignore_source(directory: str, names: list[str]) -> set[str]:
    ignored = {".git", ".github", ".codex", ".agents", "sources", "scripts", "dist", "__pycache__"}
    ignored_files = {"AGENTS.md", "README.md", ".gitignore"}
    return {name for name in names if name in ignored or name in ignored_files or name.startswith(".")}


def build(base_path: str) -> Path:
    # Regenerate authored static pages before taking the deploy snapshot.
    import subprocess
    import sys
    subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_content_pages.py")], check=True, cwd=ROOT)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "wire_internal_pages.py")], check=True, cwd=ROOT)
    # This is a fixed, generated subdirectory. Refuse to remove anything else.
    if OUTPUT.exists():
        resolved_output = OUTPUT.resolve()
        expected_output = (ROOT / "dist" / "github-pages").resolve()
        if resolved_output != expected_output or resolved_output.parent != (ROOT / "dist").resolve():
            raise RuntimeError(f"Refusing to clean unexpected output directory: {resolved_output}")
        shutil.rmtree(resolved_output)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT, OUTPUT, ignore=ignore_source)

    if base_path:
        for file_path in OUTPUT.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in WEB_EXTENSIONS:
                source = file_path.read_text(encoding="utf-8")
                file_path.write_text(ROOT_PATH_LITERAL.sub(lambda match: match.group("quote") + base_path, source), encoding="utf-8")

    site_url = os.environ.get("PAGES_SITE_URL", "").strip().rstrip("/")
    site_url = site_url.lower()
    if not site_url:
        repository = os.environ.get("GITHUB_REPOSITORY", "")
        if "/" in repository:
            owner, name = repository.split("/", 1)
            site_url = f"https://{owner.casefold()}.github.io"
    if site_url:
        enrich_html(site_url, base_path)
        (OUTPUT / "robots.txt").write_text(
            "User-agent: *\nAllow: /\n\n"
            "User-agent: OAI-SearchBot\nAllow: /\n\n"
            "User-agent: GPTBot\nDisallow: /\n\n"
            f"Sitemap: {site_url}{base_path}sitemap.xml\n",
            encoding="utf-8",
        )
        (OUTPUT / "sitemap.xml").write_text(make_sitemap(site_url, base_path), encoding="utf-8")

    (OUTPUT / ".nojekyll").write_text("", encoding="utf-8")
    return OUTPUT


def page_url(site_url: str, base_path: str, file_path: Path) -> str:
    relative = file_path.relative_to(OUTPUT).as_posix()
    route = "" if relative == "index.html" else relative[:-10] if relative.endswith("/index.html") else relative
    return f"{site_url}{base_path}{route}" if route else f"{site_url}{base_path}"


def enrich_html(site_url: str, base_path: str) -> None:
    for file_path in OUTPUT.rglob("*.html"):
        source = file_path.read_text(encoding="utf-8")
        canonical = page_url(site_url, base_path, file_path)
        title_match = re.search(r"<title>(.*?)</title>", source, re.I | re.S)
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"\s*/?>', source, re.I)
        title = html_unescape(title_match.group(1).strip()) if title_match else "Eduforn"
        description = html_unescape(desc_match.group(1).strip()) if desc_match else "Study abroad guidance from Eduforn."
        graph_type = "Article" if "/resource-corner/articles/" in file_path.as_posix() else "WebPage"
        graph = {
            "@context": "https://schema.org",
            "@graph": [
                {"@type": "Organization", "@id": f"{site_url}{base_path}#organization", "name": "Eduforn Overseas Pvt. Ltd.", "url": f"{site_url}{base_path}", "logo": {"@type": "ImageObject", "url": f"{site_url}{base_path}assets/eduforn-logo.webp"}, "email": "enquiry@eduforn.com", "telephone": "+91 85888 51085"},
                {"@type": graph_type, "@id": f"{canonical}#page", "url": canonical, "name": title, "description": description, "inLanguage": "en", "isPartOf": {"@id": f"{site_url}{base_path}#website"}, "publisher": {"@id": f"{site_url}{base_path}#organization"}},
            ],
        }
        if graph_type == "Article":
            graph["@graph"][1].update({"headline": title, "mainEntityOfPage": {"@id": f"{canonical}#page"}})
        head_extras = (
            f'<link rel="canonical" href="{canonical}">\n'
            f'<meta property="og:type" content="{"article" if graph_type == "Article" else "website"}">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{description}">\n'
            f'<meta property="og:url" content="{canonical}">\n'
            f'<meta property="og:image" content="{site_url}{base_path}assets/eduforn-logo.webp">\n'
            '<meta name="twitter:card" content="summary">\n'
            f'<meta name="twitter:title" content="{title}">\n'
            f'<meta name="twitter:description" content="{description}">\n'
            f'<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>\n'
        )
        if not re.search(r'rel="canonical"', source, re.I):
            source = re.sub(r"</head>", head_extras + "</head>", source, count=1, flags=re.I)
        file_path.write_text(source, encoding="utf-8")


def make_sitemap(site_url: str, base_path: str) -> str:
    locations = []
    for file_path in sorted(OUTPUT.rglob("*.html")):
        if re.search(r'<meta\s+name="robots"\s+content="noindex', file_path.read_text(encoding="utf-8"), re.I):
            continue
        loc = page_url(site_url, base_path, file_path)
        locations.append(f"  <url><loc>{loc}</loc></url>")
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(locations) + "\n</urlset>\n"


def html_unescape(value: str) -> str:
    import html
    return html.unescape(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-path", help="Override the GitHub Pages path, e.g. /Eduforn-website-design/; use / for a root domain")
    args = parser.parse_args()
    base_path = deployment_base(args.base_path)
    output = build(base_path)
    print(f"Prepared {output.relative_to(ROOT)} (base path: {base_path or '/'})")


if __name__ == "__main__":
    main()
