"""Read-only Reddit OAuth client (skeleton).

Only GET requests to an explicit allowlist of read endpoints are permitted.
Credentials are supplied at runtime from a secret store; nothing is persisted here.
"""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request

API = "https://oauth.reddit.com"
SCOPES = ("identity", "read", "mysubreddits", "history")
ALLOWED_PATHS = ("/api/v1/me", "/best", "/subreddits/mine/subscriber", "/user/{me}/saved")


class ReadOnlyRedditClient:
    def __init__(self, access_token: str, user_agent: str, username: str):
        self._token = access_token
        self._ua = user_agent
        self._me = username

    def _allowed(self, path: str) -> bool:
        return path in {p.replace("{me}", self._me) for p in ALLOWED_PATHS}

    def get(self, path: str, **params) -> dict:
        if not self._allowed(path):
            raise PermissionError(f"Path not in read-only allowlist: {path}")
        url = f"{API}{path}?{urllib.parse.urlencode({'raw_json': 1, **params})}"
        req = urllib.request.Request(url, method="GET", headers={
            "Authorization": f"Bearer {self._token}", "User-Agent": self._ua})
        with urllib.request.urlopen(req, timeout=30) as resp:
            remaining = float(resp.headers.get("X-Ratelimit-Remaining", "100"))
            reset = float(resp.headers.get("X-Ratelimit-Reset", "0"))
            body = json.load(resp)
        if remaining < 5:
            time.sleep(reset + 1)
        return body

    def listing(self, path: str, max_pages: int = 5, limit: int = 100):
        after = None
        for _ in range(max_pages):
            page = self.get(path, limit=limit, **({"after": after} if after else {}))
            data = page.get("data", {})
            yield from data.get("children", [])
            after = data.get("after")
            if not after:
                break

    def home(self, pages: int = 5):
        return self.listing("/best", max_pages=pages)

    def subscriptions(self):
        return self.listing("/subreddits/mine/subscriber", max_pages=10)

    def saved(self, pages: int = 5):
        return self.listing(f"/user/{self._me}/saved", max_pages=pages)
