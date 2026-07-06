This is my portfolio site, hosted at jeremylam.netlify.app

Adding a blog post
-------------------
1. Copy an existing post file, e.g. blog-mcp-itglue-documentation-server.html,
   to a new file named blog-<slug>.html at the repo root (slug = short,
   hyphenated title).
2. Update the <title>/<meta description>, the <h1> in .post-hero, the date
   and tags in .post-meta/.post-tags, and the body content inside
   .post-body. Keep the nav/footer markup as-is (just make sure the "Blog"
   link doesn't get a stray "active" class removed).
3. Open blog.html and add a new <article class="post-row"> entry above (or
   in place of) the existing ones, linking to your new file, with a date,
   a short excerpt, and matching tags.
4. Preview locally (e.g. `python3 -m http.server 8123`) and check both
   blog.html and the new post page render correctly.

No build step, database or CMS is involved — posts are just plain HTML
files styled by assets/css/style.css.
