#!/usr/bin/env python3
"""Content Creator CLI"""
import argparse
from src.generator import ContentGenerator


def main():
    p = argparse.ArgumentParser(description="Content Creator CLI")
    sub = p.add_subparsers()

    # 生成帖子
    gen = sub.add_parser("gen", help="生成内容")
    gen.add_argument("--platform", "-p", default="weibo",
                     choices=["weibo","xiaohongshu","zhihu","wechat"])
    gen.add_argument("--type", "-t", choices=["tool","opinion","tutorial","news","fun"])
    gen.add_argument("--count", "-n", type=int, default=1)
    gen.add_argument("--save", "-s", help="保存路径")

    # 生成一周计划
    plan = sub.add_parser("plan", help="生成一周发布计划")
    plan.add_argument("--topic", default="ai")
    plan.set_defaults(func=lambda a: None)

    args = p.parse_args()

    if hasattr(args, "func"):
        args.func(args)
        return

    cg = ContentGenerator()
    posts = cg.generate(platform=args.platform,
                          topic_type=args.type,
                          count=args.count)
    
    for i, post in enumerate(posts, 1):
        print(f"\n{'='*50}")
        print(f"📌 #{i} [{post.platform}] {post.mood}")
        print(f"{'='*50}")
        print(post.title)
        print("-" * 40)
        print(post.body)
        print("-" * 40)
        print("🏷️ ", " ".join(f"#{h}" for h in post.hashtags))
        print("📣 ", post.cta)

    if hasattr(args, "save") and args.save:
        import json, datetime as dt
        data = [p.__dict__ for p in posts]
        with open(args.save, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 已保存: {args.save}")

    if args.type is None:
        print("\n" + cg.generate_weekly_plan())


if __name__ == "__main__":
    main()
