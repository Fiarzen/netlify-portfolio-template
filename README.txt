This is my portfolio site, hosted at jeremylam.netlify.app

Adding a blog post
-------------------
Run the scaffolding script from the repo root:

  python3 new-post.py "My Post Title" --tags "Python, MCP" --excerpt "One-line summary for the blog index."

This creates blog-<slug>.html and adds a matching entry to the top of the
list in blog.html, dated today (pass --date "6 June 2026" to override).

Then open the new blog-<slug>.html and replace the TODO paragraphs with your
content — use <p> for paragraphs, <h2> for section headings, <code> for
inline code.

Preview locally before pushing:

  python3 -m http.server 8123
  → http://localhost:8123/blog.html

No build step, database or CMS is involved — posts are just plain HTML
files styled by assets/css/style.css. If you'd rather not use the script,
copy an existing blog-*.html file, edit its content, and add a matching
<article class="post-row"> entry to blog.html by hand.
