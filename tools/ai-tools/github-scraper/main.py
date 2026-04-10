#!/usr/bin/env python3
"""GitHub Scraper CLI"""
import argparse, json, sys, os
from src.api import GitHubAPI
from src.scraper import GitHubScraper, UserProfile, RepoInfo
from src.analyzer import analyze_profile, print_analysis
from dataclasses import asdict


def cmd_user(args):
    api = GitHubAPI()
    scraper = GitHubScraper(api)
    profile = scraper.scrape_user(args.username)
    
    # 输出格式
    if args.format == "json":
        print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))
    elif args.format == "table":
        print("\n" + "=" * 60)
        print(f"  👤 {profile.name or profile.username} (@{profile.username})")
        if profile.bio: print(f"  💬 {profile.bio}")
        if profile.company: print(f"  🏢 {profile.company}")
        if profile.location: print(f"  📍 {profile.location}")
        print(f"  📦 {profile.public_repos} 仓库 | ⭐ {profile.followers} followers | {profile.following} following")
        print("=" * 60)
        print(f"\n  {'仓库名':<30} {'语言':<10} {'⭐':<8} {'fork':<6}")
        print("  " + "-" * 56)
        for r in profile.repos[:args.limit]:
            desc = r.description[:28] + ".." if len(r.description) > 30 else r.description or ""
            print(f"  {r.name:<30} {r.language:<10} {r.stars:<8} {r.forks:<6}")
            if desc: print(f"    └ {desc}")
        print()

    # 保存
    if args.save:
        path = args.save
    else:
        date = __import__("datetime").datetime.now().strftime("%Y%m%d")
        path = f"../../data/{profile.username}_{date}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(profile.to_dict(), f, ensure_ascii=False, indent=2)
    print(f"\n✅ 数据已保存: {path}")


def cmd_search(args):
    api = GitHubAPI()
    scraper = GitHubScraper(api)
    results = scraper.search(args.query)
    for i, r in enumerate(results[:args.limit], 1):
        print(f"\n{i}. {r['full_name']}")
        print(f"   ⭐ {r['stargazers_count']} | 🍴 {r['forks_count']} | {r.get('language', 'N/A')}")
        if r.get("description"):
            print(f"   {r['description'][:80]}")
        print(f"   {r['html_url']}")


def main():
    p = argparse.ArgumentParser(description="GitHub Scraper CLI")
    sub = p.add_subparsers()

    # 用户资料
    pu = sub.add_parser("user", help="爬取用户资料")
    pu.add_argument("username", help="GitHub 用户名")
    pu.add_argument("--limit", "-n", type=int, default=10, help="显示仓库数量")
    pu.add_argument("--format", "-f", choices=["table","json"], default="table")
    pu.add_argument("--save", "-s", help="保存路径")
    pu.set_defaults(func=cmd_user)

    # 搜索
    ps = sub.add_parser("search", help="搜索仓库")
    ps.add_argument("query", help="搜索关键词")
    ps.add_argument("--limit", "-n", type=int, default=10)
    ps.set_defaults(func=cmd_search)

    args = p.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
