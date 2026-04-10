#!/usr/bin/env python3
"""
AI 科技早报生成器
"""
import urllib.request
import json
import re
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR   = os.path.dirname(SCRIPT_DIR)
NOTES_DIR  = os.path.join(REPO_DIR, "notes")

def fetch_news():
    # 多个 RSS 源，依次尝试
    feeds = [
        ("腾讯科技", "https://news.qq.com/rss/tech.xml"),
        ("36kr", "https://36kr.com/feed"),
        ("少数派", "https://sspai.com/feed"),
    ]
    for name, url in feeds:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
            })
            with urllib.request.urlopen(req, timeout=10) as r:
                xml = r.read().decode('utf-8', errors='ignore')
            # 解析 item
            items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
            news = []
            for item in items[:8]:
                title = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', item)
                link  = re.search(r'<link>(.*?)</link>', item)
                if title:
                    t = title.group(1).strip()
                    if t and t not in [n['title'] for n in news]:
                        news.append({'title': t, 'link': link.group(1).strip() if link else ''})
            if news:
                return name, news
        except Exception as e:
            continue
    return None, []

def generate_report(news, source):
    date = datetime.now().strftime('%Y年%m月%d日 %A')
    lines = [
        f"# 🤖 AI 科技早报",
        f"**{date}**",
        f"📡 数据来源：{source}",
        "",
        "---",
        ""
    ]
    if not news:
        lines.append("*（今日 RSS 源暂无数据，以下为占位内容）*")
        lines.append("")
        lines.append("**1. AI 行业动态**\n   暂无最新资讯，请稍后重试")
        lines.append("**2. 新工具发布**\n   暂无最新工具")
        lines.append("**3. 融资并购**\n   暂无最新融资")
        lines.append("**4. 政策监管**\n   暂无最新政策")
    else:
        for i, n in enumerate(news, 1):
            lines.append(f"**{i}. {n['title']}**")
            if n['link']:
                lines.append(f"   🔗 {n['link']}")
            lines.append("")
    lines.append("---")
    lines.append(f"*由 AI 自动生成 · {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    return '\n'.join(lines)

if __name__ == '__main__':
    print("📡 正在获取 AI 科技新闻...")
    source, news = fetch_news()
    if source:
        print(f"✅ 成功从 {source} 获取 {len(news)} 条新闻")
    else:
        print("⚠️  所有 RSS 源均获取失败，将生成模板占位内容")
    report = generate_report(news, source or "无")
    print("\n" + "="*50)
    print(report)
    
    # 保存
    os.makedirs(NOTES_DIR, exist_ok=True)
    save_path = os.path.join(NOTES_DIR, datetime.now().strftime('%Y-%m-%d') + '-ai-news.md')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n✅ 已保存到 {save_path}")
