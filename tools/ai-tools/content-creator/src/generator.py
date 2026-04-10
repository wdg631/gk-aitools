"""
内容生成器
根据主题自动生成社交媒体帖子
"""
import random, re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List


@dataclass
class Post:
    title: str
    body: str
    hashtags: List[str]
    platform: str
    mood: str  # hook/serious/fun/casual
    cta: str = ""  # call to action


TOPICS_AI = {
    "tool": [
        "AI 工具测评：用了3个月后真实感受",
        "免费又好用的 AI 工具，我只推荐这3个",
        "ChatGPT/Claude/Gemini 哪家强？实测对比",
        "这些 AI 工具让你的效率翻倍，不信试试",
        "AI 写作工具红黑榜｜用了半年总结",
    ],
    "opinion": [
        "AI 会不会取代你的工作？先看看这个",
        "普通人如何用 AI 副业赚钱？真实案例",
        "AI 时代，最保值的3个技能",
        "为什么我停止焦虑 AI 了",
        "AI 时代信息差正在消失，普通人机会在哪",
    ],
    "tutorial": [
        "AI 入门指南｜0基础3分钟学会用 AI",
        "如何用 AI 一天写100篇内容",
        "AI 提示词技巧｜一句话效果翻倍",
        "手把手教你用 AI 做副业",
        "零基础玩转 AI 绘画，只需5分钟",
    ],
    "news": [
        "刚刚，OpenAI 发布了重磅更新",
        "AI 圈又出大事了，这5点你需要知道",
        "最新 AI 融资盘点：谁拿到了钱？",
        "本周 AI 科技圈大事件汇总",
        "AI 监管新规出台，对普通人有什么影响",
    ],
    "fun": [
        "让 AI 用一句话评价我的工作",
        "用 AI 写了100条朋友圈，笑死了",
        "AI 眼中的程序员是这样的",
        "如果 AI 参加高考，能考多少分",
        "AI 生成的小说，比我还上头",
    ],
}

PLATFORMS = {
    "weibo": {
        "max_len": 2000,
        "hashtag_count": 3,
        "style": "短平快，情绪化开头，有争议性",
    },
    "xiaohongshu": {
        "max_len": 1000,
        "hashtag_count": 6,
        "style": "生活化，有干货，小姐姐风格",
    },
    "zhihu": {
        "max_len": 5000,
        "hashtag_count": 3,
        "style": "有深度，有数据支撑，逻辑清晰",
    },
    "wechat": {
        "max_len": 60000,
        "hashtag_count": 0,
        "style": "正式，有深度，有价值观",
    },
}

EMOJI_MAP = {
    "hook": ["🔥", "💥", "⚡", "🚀", "🎯"],
    "serious": ["📊", "📈", "💡", "🔍", "📌"],
    "fun": ["😂", "🤣", "😱", "🤯", "💀"],
    "casual": ["👀", "🙋", "✨", "👇", "👉"],
}


class ContentGenerator:
    def __init__(self, topic_area: str = "ai"):
        self.topic_area = topic_area
        self.topics = TOPICS_AI

    def generate(self, platform: str = "weibo",
                 topic_type: str = None,
                 count: int = 1) -> List[Post]:
        posts = []
        topic_types = [topic_type] if topic_type else list(self.topics.keys())
        for i in range(count):
            t = random.choice(topic_types)
            titles = self.topics.get(t, self.topics["opinion"])
            title = random.choice(titles)
            mood = random.choice(list(EMOJI_MAP.keys()))
            body = self._generate_body(title, platform, mood, t)
            hashtags = self._generate_hashtags(title, platform, t)
            cta = self._generate_cta(mood)
            posts.append(Post(
                title=title,
                body=body,
                hashtags=hashtags,
                platform=platform,
                mood=mood,
                cta=cta,
            ))
        return posts

    def _generate_body(self, title: str, platform: str, mood: str, topic_type: str) -> str:
        emoji = " ".join(random.sample(EMOJI_MAP[mood], 2))
        bodies = {
            "weibo": f"""{emoji}
{title}

{self._topic_body(topic_type, platform)}

{self._generate_cta(mood)}""",
            "xiaohongshu": f"""【{title}】

{emoji} {self._topic_body(topic_type, platform)}

{emoji} {self._topic_body(topic_type, platform)}

{emoji} {self._topic_body(topic_type, platform)}

——
你们还有什么想了解的？评论区见 👇""",
            "zhihu": f"""# {title}

## 前言

{self._topic_body(topic_type, platform)}

## 核心观点

{self._topic_body(topic_type, platform)}

## 深度分析

{self._topic_body(topic_type, platform)}

## 结论

{self._topic_body(topic_type, platform)}

---

{self._generate_cta(mood)}""",
            "wechat": f"""# {title}

> {emoji} {self._topic_body(topic_type, platform)}

{self._topic_body(topic_type, platform)}

## 一、背景

{self._topic_body(topic_type, platform)}

## 二、核心内容

{self._topic_body(topic_type, platform)}

## 三、实操方法

{self._topic_body(topic_type, platform)}

## 四、总结

{self._topic_body(topic_type, platform)}

**{self._generate_cta(mood)}**

---

原创不易，点个「在看」，我们下期见。
""",
        }
        return bodies.get(platform, bodies["weibo"])

    def _topic_body(self, topic_type: str, platform: str) -> str:
        bodies = {
            "tool": "最近深度体验了几款 AI 工具，从写作到做图到数据分析，全程用它辅助完成。整体感受是：效率提升明显，但关键还是要靠人把关。",
            "opinion": "AI 时代最大的机会，不是学会用 AI，而是学会用 AI 放大自己的独特优势。与其焦虑，不如现在开始用起来。",
            "tutorial": "跟着步骤做，3分钟就能跑通。关键是提示词的技巧，同样的工具，会用的人产出能差10倍。",
            "news": "这件事对行业的影响，可能比很多人想象的要大。先别急着下结论，看完这篇再说。",
            "fun": "这太真实了，简直就是我本人 😂 笑完之后冷静想想，其实也反映了一些问题...",
        }
        return bodies.get(topic_type, bodies["opinion"])

    def _generate_hashtags(self, title: str, platform: str, topic_type: str) -> List[str]:
        base = ["AI", "人工智能", "AI工具", "科技"]
        topic_tags = {
            "tool": ["AI工具", "效率神器", "科技好物"],
            "opinion": ["AI时代", "职场干货", "副业赚钱"],
            "tutorial": ["AI教程", "新手入门", "AI学习"],
            "news": ["AI资讯", "科技新闻", "行业观察"],
            "fun": ["AI趣闻", "沙雕日常", "科技段子"],
        }
        cfg = PLATFORMS.get(platform, PLATFORMS["weibo"])
        count = cfg.get("hashtag_count", 3)
        return (topic_tags.get(topic_type, []) + base)[:count]

    def _generate_cta(self, mood: str) -> str:
        ctas = {
            "hook": "你怎么看？评论区说说你的经历 👇",
            "serious": "如果觉得有收获，转发给需要的朋友",
            "fun": "你遇到过类似的情况吗？评论区聊聊 😄",
            "casual": "有用的话点个赞，我会继续分享更多 💪",
        }
        return ctas.get(mood, "点个赞再走呗 👍")

    def generate_weekly_plan(self, topic_area: str = None) -> str:
        area = topic_area or self.topic_area
        types = ["news", "tool", "tutorial", "opinion", "fun"]
        weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        lines = [
            f"# 📅 一周内容发布计划",
            f"**主题领域：{area.upper()}**",
            "",
            "| 星期 | 内容类型 | 选题 |",
            "|------|----------|------|",
        ]
        for i, (dow, t) in enumerate(zip(weekdays, types * 2)):
            titles = self.topics.get(t, self.topics["opinion"])
            title = random.choice(titles)
            type_names = {
                "news": "🔴 热点速递",
                "tool": "🛠️ 工具测评",
                "tutorial": "📖 教程干货",
                "opinion": "💭 观点讨论",
                "fun": "😂 轻松一刻",
            }
            lines.append(f"| {dow} | {type_names[t]} | {title} |")
        lines.append("")
        lines.append(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        return "\n".join(lines)
