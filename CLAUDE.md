# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Jeremy Lam's personal portfolio site, hosted at jeremylam.netlify.app. It is a static, no-build multi-page HTML site — no package.json, no bundler, no framework. Pages are plain `.html` files at the repo root that link directly to CSS/JS under `assets/`.

## Running / previewing

There is no build or dev-server tooling in this repo. Preview by serving the root statically, e.g.:

```
python3 -m http.server 8123
```

Then open `http://localhost:8123/index.html` (or any other page). There are no tests or linters configured.

## Architecture

- **Current design system**: `assets/css/style.css` — a single custom stylesheet (CSS custom properties, OKLCH colors, Space Grotesk/IBM Plex Sans/IBM Plex Mono via Google Fonts). Every current page (`index.html`, `about.html`, `projects.html`, `contact.html`, `blog.html`, and blog post pages) uses **only** this stylesheet, is vanilla HTML/CSS with a small inline `<script>` per page for the mobile nav toggle, and shares no other JS.
- **Legacy template (unused, still present)**: `assets/css/main.css`, `assets/js/*` (jQuery, `main.js`, `util.js`, breakpoints/browser/scrollex/scrolly helpers), `assets/sass/`, and `portfolio site.zip` are leftovers from the original HTML5UP-style template the site was redesigned from. No current page references them — don't wire new pages into this stack; treat it as dead weight rather than an alternate system to extend.
- **Per-page structure is copy-pasted, not templated**: since there's no build step, every page repeats the same `<header class="nav">` and `<footer>` markup verbatim (brand mark, nav links with one `class="active"` per page, mobile hamburger toggle script). When adding a nav link or changing the footer, it must be edited in every `.html` file individually — grep across `*.html` to find all copies.
- **Blog is a flat list of static pages**: `blog.html` is a hand-maintained index (`.post-list` of `.post-row` entries) linking to individual post pages named `blog-<slug>.html` at the repo root (e.g. `blog-mcp-itglue-documentation-server.html`). There's no CMS or data file — adding a post means creating a new HTML file styled with the `.post-hero`/`.post-body` classes in `style.css` and adding a matching `.post-row` entry to `blog.html`.
- **Projects list** (`projects.html`) is similarly hand-maintained: each project is an `.card` article with `data-categories` used by the inline JS filter buttons (`.filters button[data-filter]`). Category values (`Data`, `Web`, `Cloud`) must match between a card's `data-categories` and the filter buttons for filtering to work.
- Images referenced by pages live in `images/`; several `*.jfif:Zone.Identifier`/`:Zone.Identifier` files are Windows artifacts, not real assets.
