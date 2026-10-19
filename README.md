# personal-reddit-digest

A small, self-hosted, **read-only** tool that turns one person's own Reddit account into a weekly digest.

The goal is to check Reddit less often. Instead of opening the app many times a day, the owner gets one short
weekly page of the posts from their subscribed communities and saved items that they are most likely to care
about. Every item links back to Reddit, where reading and discussion happen.

## What it does

Once a week, authenticated via OAuth **as the owner's own account**, it:

1. Reads the owner's Home/Best listing (a few pages).
2. Reads the owner's subscribed-communities list (`/subreddits/mine/subscriber`).
3. Reads the owner's saved posts/comments (`/user/{me}/saved`).
4. Ranks those items against the owner's personal reading interests.
5. Renders a private web page (~20–30 items: title, subreddit, short excerpt, link back to Reddit),
   reachable only on the owner's private network.

## What it does NOT do

- No posting, commenting, voting, messaging, following, or moderation — no write scopes are requested.
- No access to other users' data beyond what appears in the owner's own feed.
- No AI/ML model training, dataset building, resale, redistribution, sharing, or advertising.
- Not a multi-user service. One user, one account, one private page.
- Not tied to any subreddit or community install.

## API usage

| Item | Value |
|---|---|
| Auth | OAuth 2.0, owner's own account, permanent refresh token |
| Scopes | `identity`, `read`, `mysubreddits`, `history` |
| Endpoints | `/best`, `/subreddits/mine/subscriber`, `/user/{me}/saved`, `/api/v1/me` |
| Frequency | One scheduled run per week |
| Volume | Normally < 100 requests per run (far below the 100 QPM free-tier limit) |
| Rate limits | Honors `X-Ratelimit-*` headers; backs off on 429 |
| User-Agent | `linux:personal-reddit-digest:v0.1 (by /u/<owner>)` |

## Data handling

- OAuth client secret and tokens are stored in a password manager, never in this repository.
- Raw post/comment content is deleted within 48 hours of retrieval.
- Only titles, permalinks, subreddit names, and short excerpts are retained, for the owner's own reference.
- The digest page is self-hosted and accessible only on the owner's private network.

## Why not Devvit

Devvit apps run inside Reddit and are installed into communities (games, mod tools, interactive posts). This
tool reads one user's personalized feed and saved listings for that user's own off-platform weekly review, so
standard OAuth Data API access is the appropriate fit.

## Status

Early development. API access is pending approval under Reddit's Responsible Builder Policy. The read-only
client skeleton is in `src/reddit_digest/`.

## License

MIT
