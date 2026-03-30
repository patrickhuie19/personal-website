# Static assets by post

Each folder matches a blog slug (or topic). Co-locate images with optional long-form notes (e.g. `research.md`).

| Folder | Post / use |
|--------|------------|
| `bio-adversaries/` | [bio-adversaries](/blog/bio-adversaries/) |
| `economics-of-local-llms/` | [economics-of-local-llms](/blog/economics-of-local-llms/) — charts; `research.md` in this folder links to the blog (static `.md` is not rendered as HTML) |
| `mcp-learn/` | [mcp-learn](/blog/mcp-learn/) |

In `posts/*.md`, reference files with root-relative URLs: `/assets/<folder>/<file>`.
