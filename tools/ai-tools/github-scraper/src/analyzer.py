"""
数据分析模块
"""
from collections import Counter
from dataclasses import asdict
from typing import List
from .scraper import RepoInfo, UserProfile


def analyze_profile(profile: UserProfile) -> dict:
    repos = profile.repos
    total_stars = sum(r.stars for r in repos)
    total_forks = sum(r.forks for r in repos)
    avg_stars = total_stars / len(repos) if repos else 0
    langs = Counter(r.language for r in repos if r.language)
    top_repos = sorted(repos, key=lambda r: r.stars, reverse=True)[:5]
    
    return {
        "username": profile.username,
        "total_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "avg_stars": round(avg_stars, 2),
        "language_distribution": dict(lang_counts := Counter(
            r.language for r in repos if r.language
        ).most_common(10)),
        "top_repos": [asdict(r) for r in top_repos],
        "has_blog": bool(profile.blog),
        "has_bio": bool(profile.bio),
    }


def print_analysis(analysis: dict):
    print(f"\n📊 GitHub 分析报告: @{analysis['username']}")
    print("=" * 50)
    print(f"  📦 仓库总数  : {analysis['total_repos']}")
    print(f"  ⭐ 获得 stars: {analysis['total_stars']}")
    print(f"  🍴 总 forks  : {analysis['total_forks']}")
    print(f"  📈 平均 stars : {analysis['avg_stars']}")
    langs = analysis.get("language_distribution", {})
    if langs:
        print(f"\n  🛠️  语言分布:")
        for lang, cnt in list(langs.items())[:5]:
            bar = "█" * cnt
            print(f"    {lang:<12} {bar} {cnt}")
    top = analysis.get("top_repos", [])
    if top:
        print(f"\n  ⭐ 最热门仓库:")
        for r in top[:3]:
            desc = (r["description"] or "无描述")[:40]
            print(f"    • {r['name']}  ⭐{r['stars']}  {desc}")
