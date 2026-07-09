#!/usr/bin/env python3
"""Scaffold a new blog post.

Usage:
  python3 new-post.py "My Post Title"
  python3 new-post.py "My Post Title" --tags "Python, MCP" --excerpt "One-line summary for the blog index."
  python3 new-post.py "My Post Title" --date "6 June 2026"

Creates blog/<slug>.html from the built-in template and inserts a matching
entry at the top of the list in blog/index.html. Then open the new file and
replace the TODO paragraphs with your content.
"""

import argparse
import datetime
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

POST_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title} — Jeremy Lam</title>
  <meta name="description" content="{excerpt}" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../assets/css/style.css" />
</head>
<body>

  <!-- NAV -->
  <header class="nav" role="banner">
    <div class="wrap">
      <a class="brand" href="../index.html" aria-label="Jeremy Lam — home">
        <span class="mark" aria-hidden="true">JL</span> Jeremy Lam
      </a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false" id="navToggle">
        <svg width="22" height="22" viewBox="0 0 22 22" fill="none" aria-hidden="true">
          <rect y="4" width="22" height="2" rx="1" fill="currentColor"/>
          <rect y="10" width="22" height="2" rx="1" fill="currentColor"/>
          <rect y="16" width="22" height="2" rx="1" fill="currentColor"/>
        </svg>
      </button>
      <nav id="mainNav" aria-label="Main navigation">
        <a href="../index.html">Home</a>
        <a href="../projects.html">Projects</a>
        <a href="./" class="active">Blog</a>
        <a href="../about.html">About</a>
        <a href="../contact.html">Contact</a>
      </nav>
      <a class="cta" href="../contact.html">Get in touch</a>
    </div>
  </header>

  <main>
    <section class="post-hero wrap">
      <a class="back mono" href="./"><span aria-hidden="true">←</span> Back to blog</a>
      <h1>{title}</h1>
      <div class="post-meta">
        <span>{date}</span>
      </div>
      <div class="post-tags">
        {tag_spans}
      </div>
    </section>

    <article class="post-body wrap">

      <p>TODO: opening paragraph.</p>

      <h2>TODO: first section heading</h2>

      <p>TODO: section content.</p>

      <div class="post-cta">
        <a class="btn btn-ghost" href="./">← Back to blog</a>
        <a class="btn btn-primary" href="../contact.html">Get in touch <span class="ar" aria-hidden="true">↗</span></a>
      </div>

    </article>
  </main>

  <footer role="contentinfo">
    <div class="wrap">
      <span>© {year} Jeremy Lam</span>
      <span>Designed clean · built with rhythm</span>
    </div>
  </footer>

<script>
  // mobile nav toggle
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('mainNav');
  if(toggle && nav){{
    toggle.addEventListener('click', function(){{
      const open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    }});
  }}
</script>
</body>
</html>
"""

LIST_ENTRY_TEMPLATE = """
        <article class="post-row">
          <div class="post-main">
            <div class="post-date mono">{date}</div>
            <h3><a href="{filename}">{title}</a></h3>
            <p>{excerpt}</p>
            <div class="post-tags">
              {tag_spans}
            </div>
          </div>
          <span class="post-arrow" aria-hidden="true">↗</span>
        </article>
"""


def slugify(title: str) -> str:
    slug = title.lower()
    slug = re.sub(r"[''']", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold a new blog post.")
    parser.add_argument("title", help="Post title, e.g. \"Building an MCP server\"")
    parser.add_argument("--tags", default="", help="Comma-separated tags, e.g. \"Python, MCP\"")
    parser.add_argument("--excerpt", default="TODO: one-line summary for the blog index.",
                        help="Short summary shown on the blog index and in the meta description")
    parser.add_argument("--date", default=None, help="Display date, e.g. \"6 June 2026\" (default: today)")
    parser.add_argument("--slug", default=None, help="Override the auto-generated filename slug")
    args = parser.parse_args()

    today = datetime.date.today()
    date = args.date or f"{today.day} {today.strftime('%B %Y')}"
    slug = args.slug or slugify(args.title)
    filename = f"{slug}.html"
    post_path = ROOT / "blog" / filename
    blog_index = ROOT / "blog" / "index.html"

    if post_path.exists():
        print(f"error: blog/{filename} already exists — pass --slug to pick another name", file=sys.stderr)
        return 1
    if not blog_index.exists():
        print("error: blog/index.html not found — run this from the repo root", file=sys.stderr)
        return 1

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    tag_spans = "".join(f"<span>{html.escape(t)}</span>" for t in tags) or "<span>TODO</span>"

    title_esc = html.escape(args.title)
    excerpt_esc = html.escape(args.excerpt)

    post_path.write_text(POST_TEMPLATE.format(
        title=title_esc, excerpt=excerpt_esc, date=date,
        tag_spans=tag_spans, year=today.year,
    ), encoding="utf-8")

    index_html = blog_index.read_text(encoding="utf-8")
    marker = '<div class="post-list">'
    if marker not in index_html:
        print("error: couldn't find the post list in blog/index.html — add the entry by hand", file=sys.stderr)
        return 1
    entry = LIST_ENTRY_TEMPLATE.format(
        date=date, filename=filename, title=title_esc,
        excerpt=excerpt_esc, tag_spans=tag_spans,
    )
    blog_index.write_text(index_html.replace(marker, marker + entry, 1), encoding="utf-8")

    print(f"created  blog/{filename}")
    print(f"updated  blog/index.html (new entry added at the top)")
    print()
    print("next steps:")
    print(f"  1. open blog/{filename} and replace the TODO paragraphs with your content")
    if not tags:
        print(f"  2. replace the TODO tag in both files (or rerun with --tags next time)")
    if args.excerpt.startswith("TODO"):
        print(f"  3. replace the TODO excerpt in blog/index.html and the meta description in blog/{filename}")
    print(f"  preview: python3 -m http.server 8123  →  http://localhost:8123/blog/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
