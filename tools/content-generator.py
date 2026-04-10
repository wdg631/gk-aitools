#!/usr/bin/env python3
"""
内容选题灵感生成器
输入关键词，自动生成 7 天社交媒体发布计划
"""
import random
import sys
from datetime import datetime, timedelta

TOPICS = {
    'ai': [
        'ChatGPT/Claude/Gemini 最新动态',
        'AI 工具测评：哪款最适合你',
        'AI 行业融资新闻解读',
        'AI 取代哪些职业？怎么应对',
        'AI 入门教程：从 0 到 1',
        'AI + 生活：用了就回不去的 5 个场景',
        '大模型技术原理（通俗版）',
    ],
    'tech': [
        '本周最值得关注的科技产品',
        '苹果/谷歌/微软 本周大事件',
        '手机/电脑 选购指南',
        '科技圈八卦/争议事件',
        '未来科技趋势预测',
        '程序员必备工具推荐',
        '数码博主装备清单',
    ],
    'life': [
        '早睡早起计划执行记录',
        '极简生活：我不再买的 10 样东西',
        '时间管理：我的每日 3 小时深度工作法',
        '读书笔记分享',
        '低成本爱好：钓鱼/徒步/骑行',
        '独居一周真实体验',
    ]
}

def generate_plan(topic='ai', days=7):
    base = datetime.now()
    lines = [
        f"# 📅 内容发布计划",
        f"**主题：{topic.upper()} · 共 {days} 天**",
        "",
        "| 日期 | 星期 | 内容类型 | 选题示例 |",
        "|------|------|----------|----------|",
    ]
    types = ['热点速递', '工具测评', '深度干货', '行业洞察', '观点讨论', '轻松一刻', '汇总预告']
    for i in range(days):
        d = base + timedelta(days=i)
        t = types[i % len(types)]
        opts = TOPICS.get(topic.lower(), TOPICS['ai'])
        title = random.choice(opts)
        dow = ['周一','周二','周三','周四','周五','周六','周日'][d.weekday()]
        date_str = d.strftime('%m/%d')
        lines.append(f"| {date_str} | {dow} | {t} | {title} |")
    return '\n'.join(lines)

if __name__ == '__main__':
    topic = sys.argv[1].lower() if len(sys.argv) > 1 else 'ai'
    plan = generate_plan(topic)
    print(plan)
