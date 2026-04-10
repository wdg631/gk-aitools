"""
GitHub API 封装
支持 REST API，自动处理分页和速率限制
"""
import os, time, json, urllib.request, urllib.error
from typing import Optional


class GitHubAPI:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self.token = token or self._get_token()
        self.headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "GitHub-Scraper/1.0",
        }
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def _get_token(self) -> Optional[str]:
        try:
            import subprocess
            r = subprocess.run(["gh", "auth", "token"],
                             capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                return r.stdout.strip()
        except Exception:
            pass
        return None

    def _request(self, url: str) -> dict | list:
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                remaining = int(resp.headers.get("X-RateLimit-Remaining", 9999))
                if remaining < 5:
                    reset_ts = int(resp.headers.get("X-RateLimit-Reset", 0))
                    wait = max(0, reset_ts - time.time()) + 1
                    print(f"  ⏳ 速率限制，等待 {int(wait)}s...")
                    time.sleep(wait)
                return json.loads(resp.read().decode("utf-8", errors="ignore"))
        except urllib.error.HTTPError as e:
            print(f"  ❌ HTTP {e.code}: {e.reason}")
            return [] if "repos" in url else {}

    def get_user(self, username: str) -> dict:
        return self._request(f"{self.BASE_URL}/users/{username}")

    def get_user_repos(self, username: str, sort: str = "updated") -> list:
        repos, page = [], 1
        while True:
            data = self._request(
                f"{self.BASE_URL}/users/{username}/repos"
                f"?sort={sort}&per_page=100&page={page}"
            )
            if not data:
                break
            repos.extend(data)
            if len(data) < 100:
                break
            page += 1
            time.sleep(0.5)
        return repos

    def get_repo_languages(self, owner: str, repo: str) -> dict:
        return self._request(f"{self.BASE_URL}/repos/{owner}/{repo}/languages")

    def search_repos(self, query: str, sort: str = "stars") -> list:
        r = self._request(
            f"{self.BASE_URL}/search/repositories"
            f"?q={urllib.request.quote(query)}&sort={sort}&per_page=30"
        )
        return r.get("items", []) if isinstance(r, dict) else []

    def get_user_events(self, username: str) -> list:
        return self._request(f"{self.BASE_URL}/users/{username}/events?per_page=100")
