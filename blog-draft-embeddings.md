TITLE: Adding semantic search to my MCP server

DATE: 21 July 2026

TAGS: MCP, Python, Azure OpenAI, SQLite, Embeddings

EXCERPT (for blog index + meta description):
Bolting vector search onto the ITGlue MCP server: what an embedding actually is, how documents get embedded cheaply, and why everything still falls back to keyword search the moment it can't.

---

BODY:

Sometimes the search tool on my ITGlue MCP server would miss documents related to the search query that should obviously be related. I'd been using FTS5 (a way of searching through the SQLite database) but if the contents didn't match the words in the query there was no way of the tool knowing what to filter for e.g a query for "How to VPN to the company server" would not find a document called "Remote Access Configuration". Adding a way of searching by meaning through vector embedding proved to be a cost-effective resolution if set up correctly.

## Vector Embedding

An embedding is just a list of numbers, a vector, that represents the meaning of a piece of text. Azure OpenAI's text-embedding-3-small model turns any text into 1,536 of them. The useful property is that texts with similar meaning end up as vectors pointing in similar directions, so "reset a user's password" and "how to change someone's login credentials" land close together even though they don't share a word. You measure "close together" with cosine similarity, and because these vectors are unit-normalised (between 0 and 1), the dot product of two of them is the cosine similarity directly. 

## Cost-Efficiency

The sync that populates ITGlue documentation runs a full sync every 24 hours and rewrites every document's body each time, whether it actually changed or not. Embedding on every sync would mean re-embedding the entire ~3,800-document corpus four times a day for no reason, which is an easy way to turn a free side project into an Azure bill you notice. So each document's row carries a second column alongside its embedding: a SHA-256 hash of the exact text that produced it. Before re-embedding anything, the sync compares the new hash to the stored one, and skips it on a match. In steady state almost nothing changes between syncs, so almost nothing gets re-sent to Azure. The same function does double duty as the backfill: on a fresh database nothing has a hash yet, so everything is "pending" and the whole corpus gets embedded once, which is how all 3,822 docs got their first vectors in one pass.

## No separate vector database

I didn't reach for a vector database or sqlite-vec for this. Each document's embedding just lives as a BLOB column on the existing `documents` table, 1,536 float32s packed into 6,144 bytes, next to that hash column. At query time the whole set of stored embeddings gets loaded into a NumPy matrix and multiplied against the query's embedding in one shot, producing a similarity score for every document at once. At a few thousand documents that multiply takes milliseconds, which is well inside the budget of one MCP tool call, and it means there's no second system to run, back up, or keep in sync with the primary database. sqlite-vec remains as a possible upgrade in the future.

## Falling back to FTS5

Every part of this is optional. If the Azure environment variables aren't set, the embed pass is skipped entirely and the server just runs on FTS5, no errors. If the live call to embed a user's query fails, times out, or gets rate-limited, that's caught and treated the same as "no vector results". And because a vector search always returns its top-k regardless of whether any of it is actually relevant, there's a similarity floor: if the best match is still below it, the result is discarded and the tool falls back to keyword search rather than confidently handing the agent a document that only loosely matches. Right now that floor is set to zero, on purpose, because text-embedding-3's scores run lower than I expected and I'd rather log real similarity scores from production for a week or two than guess at a threshold. Early results are landing in the 0.5–0.6 range for good matches, so the floor will probably end up somewhere around 0.2–0.4 once there's enough data to justify picking a number.

---
NOTES TO SELF / OPEN QUESTIONS FOR REVIEW:
- Matches the voice/structure of the two existing MCP posts (blog/mcp-itglue-documentation-server.html, blog/adding-datto-rmm-to-my-mcp-server.html): first person, h2-separated sections, no bullet lists, closing reflection paragraph.
- Once approved, this becomes blog/adding-semantic-search-to-my-mcp-server.html via new-post.py, with the TODO paragraphs replaced by the body above.
