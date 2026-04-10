from typing import Optional
"""
GitHub 数据爬虫
"""
from .api import GitHubAPI
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List
import json


@dataclass
class RepoInfo:
    name: str = ""
    full_name: str = ""
    description: str = ""
    language: str = ""
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    open_issues: int = 0
    license: str = ""
    topics: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    pushed_at: str = ""
    url: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "RepoInfo":
        lic = d.get("license")
        return cls(
            name=d.get("name", ""),
            full_name=d.get("full_name", ""),
            description=d.get("description") or "",
            language=d.get("language") or "",
            stars=d.get("stargazers_count", 0),
            forks=d.get("forks_count", 0),
            watchers=d.get("watchers_count", 0),
            open_issues=d.get("open_issues_count", 0),
            license=lic.get("spdx_id", "") if isinstance(lic, dict) else "",
            topics=d.get("topics", []),
            created_at=d.get("created_at", ""),
            updated_at=d.get("updated_at", ""),
            pushed_at=d.get("pushed_at", ""),
            url=d.get("html_url", ""),
        )


@dataclass
class UserProfile:
    username: str = ""
    name: str = ""
    bio: str = ""
    company: str = ""
    blog: str = ""
    location: str = ""
    email: str = ""
    public_repos: int = 0
    public_gists: int = 0
    followers: int = 0
    following: int = 0
    created_at: str = ""
    avatar_url: str = ""
    repos: List[RepoInfo] = field(default_factory=list)

    @classmethod
    def from_username(cls, api: GitHubAPI, username: str) -> "UserProfile":
        user = api.get_user(username)
        repos_data = api.get_user_repos(username)
        repos = [RepoInfo.from_dict(r) for r in repos_data]
        return cls(
            username=user.get("login", ""),
            name=user.get("name") or "",
            bio=user.get("bio") or "",
            company=user.get("company") or "",
            blog=user.get("blog") or "",
            location=user.get("location") or "",
            email=user.get("email") or "",
            public_repos=user.get("public_repos", 0),
            public_gists=user.get("public_gists", 0),
            followers=user.get("followers", 0),
            following=user.get("following", 0),
            created_at=user.get("created_at", ""),
            avatar_url=user.get("avatar_url", ""),
            repos=repos,
        )

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "repos": [asdict(r) for r in self.repos],
        }


class GitHubScraper:
    def __init__(self, api: Optional[GitHubAPI] = None):
        self.api = api or GitHubAPI()

    def scrape_user(self, username: str) -> UserProfile:
        print(f"  🔍 正在爬取用户 {username}...")
        profile = UserProfile.from_username(self.api, username)
        print(f"  ✅ followers={profile.followers} | repos={len(profile.repos)}")
        return profile

    def search(self, query: str) -> List[dict]:
        print(f"  🔍 搜索: {query}")
        results = self.api.search_repos(query)
        print(f"  ✅ 找到 {len(results)} 个结果")
        return results
