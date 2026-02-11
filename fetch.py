#!/usr/bin/env python3
"""
HN News Digest - Hacker News 热门博客每日精选
支持中英文输出配置
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
import feedparser
from pathlib import Path
import sys
import os

# ============= 配置 =============
OPML_PATH = "/root/.openclaw/workspace/hn-popular-blogs-2025.opml"
STATE_PATH = "/root/.openclaw/workspace/skills/hn-news-digest/state.json"
CONFIG_PATH = "/root/.openclaw/workspace/skills/hn-news-digest/config.json"
MAX_ARTICLES = 20
TIMEOUT = 5

# 飞书配置（敏感信息从配置读取）
FEISHU_SECRET_PATH = "~/.openclaw/secrets/feishu_app_secret"

# 中英文文本模板
TEXTS = {
    "zh": {
        "title": "📰 HN 热门博客每日精选 - {date}",
        "source": "来源: HN 2025 ({count} 个订阅源)",
        "articles": "文章数: {count} 篇",
        "fetching": "📡 抓取 {count} 个 RSS 源...",
        "success": "✓ {source}: +{count} 篇",
        "failed": "✗ {source}",
        "done": "📊 共 {count} 篇",
        "saved": "📁 已保存: {path}",
        "feishu_pushing": "📱 推送飞书...",
        "feishu_ok": "✓ 飞书推送成功",
        "feishu_fail": "✗ 飞书失败: {error}",
        "feishu_error": "✗ 飞书异常: {error}",
        "no_articles": "⚠ 没有新文章",
        "finish": "✅ 完成!",
        "item_prefix": "### {i}. {title}",
        "item_meta": "📅 {date} | [{source}]({url})",
        "item_link": "🔗 [原文]({url})",
        "item_summary": "> {summary}...",
    },
    "en": {
        "title": "📰 HN Popular Blogs Daily - {date}",
        "source": "Source: HN 2025 ({count} feeds)",
        "articles": "Articles: {count}",
        "fetching": "📡 Fetching {count} RSS feeds...",
        "success": "✓ {source}: +{count}",
        "failed": "✗ {source}",
        "done": "📊 Total: {count} articles",
        "saved": "📁 Saved: {path}",
        "feishu_pushing": "📱 Pushing to Feishu...",
        "feishu_ok": "✓ Feishu push success",
        "feishu_fail": "✗ Feishu failed: {error}",
        "feishu_error": "✗ Feishu error: {error}",
        "no_articles": "⚠ No new articles",
        "finish": "✅ Done!",
        "item_prefix": "### {i}. {title}",
        "item_meta": "📅 {date} | [{source}]({url})",
        "item_link": "🔗 [Link]({url})",
        "item_summary": "> {summary}...",
    }
}

# 优先级源列表
PRIORITY_SOURCES = [
    "simonwillison.net", "krebsonsecurity.com", "paulgraham.com",
    "daringfireball.net", "lcamtuf.substack.com", "overreacted.io",
    "mitchellh.com", "jeffgeerling.com", "devblogs.microsoft.com/oldnewthing",
    "shkspr.mobi", "pluralistic.net", "lucumr.pocoo.org",
    "johndcook.com", "matklad.github.io", "garymarcus.substack.com",
    "xeiaso.net", "gwern.net", "dwarkesh.com", "tedunangst.com",
    "rachelbythebay.com", "steveblank.com", "troyhunt.com",
    "righto.com", "dynomight.net", "geohot.github.io",
]

# 全局语言设置
LANGUAGE = "zh"


def t(key, **kwargs):
    """获取翻译文本"""
    text = TEXTS[LANGUAGE].get(key, TEXTS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text


def load_config():
    """加载配置"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH) as f:
            return json.load(f)
    return {"language": LANGUAGE}


def save_config(config):
    """保存配置"""
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)


def load_sources(limit=30):
    """加载 RSS 源，按优先级排序"""
    all_sources = []
    tree = ET.parse(OPML_PATH)
    for outline in tree.findall(".//outline"):
        if outline.get("type") == "rss":
            all_sources.append({
                "title": outline.get("title", ""),
                "xmlUrl": outline.get("xmlUrl", ""),
                "htmlUrl": outline.get("htmlUrl", "")
            })
    
    prioritized = []
    others = []
    for s in all_sources:
        if s["title"] in PRIORITY_SOURCES:
            prioritized.append(s)
        else:
            others.append(s)
    
    prioritized.sort(key=lambda x: PRIORITY_SOURCES.index(x["title"]) if x["title"] in PRIORITY_SOURCES else 999)
    return (prioritized + others)[:limit]


def parse_date(entry):
    """解析文章日期"""
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        return datetime(*entry.published_parsed[:6])
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        return datetime(*entry.updated_parsed[:6])
    return None


def fetch_articles(sources):
    """抓取所有文章"""
    all_articles = []
    for i, s in enumerate(sources, 1):
        try:
            req = Request(s["xmlUrl"], headers={"User-Agent": "HN-Digest/1.0"})
            with urlopen(req, timeout=TIMEOUT) as resp:
                parsed = feedparser.parse(resp.read())
                count = 0
                for entry in parsed.entries[:5]:
                    pub = parse_date(entry)
                    if pub and pub > datetime.utcnow() - timedelta(days=7):
                        all_articles.append({
                            "title": entry.get("title", "Untitled"),
                            "link": entry.get("link", ""),
                            "published": pub,
                            "source": s["title"],
                            "source_url": s["htmlUrl"],
                            "summary": entry.get("summary", "")[:80]
                        })
                        count += 1
                print(t("success", source=s["title"], count=count))
        except Exception as e:
            print(t("failed", source=s["title"]))
    
    all_articles.sort(key=lambda x: x["published"], reverse=True)
    return all_articles


def generate_digest(articles, source_count):
    """生成日报"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [t("title", date=today), ""]
    lines.append(t("source", count=source_count))
    lines.append(t("articles", count=len(articles)))
    lines.append("---")
    lines.append("")
    
    for i, a in enumerate(articles[:MAX_ARTICLES], 1):
        ds = a["published"].strftime("%m-%d %H:%M")
        lines.append(t("item_prefix", i=i, title=a["title"]))
        lines.append(t("item_meta", date=ds, source=a["source"], url=a["source_url"]))
        lines.append(t("item_link", url=a["link"]))
        if a["summary"]:
            lines.append(t("item_summary", summary=a["summary"]))
        lines.append("")
    
    return "\n".join(lines)


def send_feishu(text, config):
    """推送到飞书"""
    if not config.get("feishu_enabled", False):
        print("⏭️ 飞书未启用，跳过推送")
        return False
    
    print(t("feishu_pushing"))
    
    try:
        # 从配置文件读取敏感信息
        feishu_config = config.get("feishu", {})
        app_id = feishu_config.get("app_id")
        user_id = feishu_config.get("user_id")
        app_secret_path = os.path.expanduser(feishu_config.get("secret_path", FEISHU_SECRET_PATH))
        
        if not app_id or not user_id:
            print(t("feishu_error", error="Missing app_id or user_id in config"))
            return False
        
        with open(app_secret_path) as f:
            app_secret = f.read().strip()
        
        # 获取 token
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        req = Request(url, data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
                     headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=TIMEOUT) as resp:
            token = json.loads(resp.read().decode()).get("tenant_access_token")
        
        if not token:
            print(t("feishu_fail", error="No token"))
            return False
        
        # 发送消息
        msg_url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id={user_id}&receive_id_type=open_id"
        msg_data = json.dumps({
            "receive_id": user_id,
            "msg_type": "text",
            "content": json.dumps({"text": text[:7000]})
        })
        
        req = Request(msg_url, data=msg_data.encode(),
                     headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                     method="POST")
        with urlopen(req, timeout=TIMEOUT) as resp:
            result = json.loads(resp.read().decode())
            if result.get("code") == 0:
                print(t("feishu_ok"))
                return True
            else:
                print(t("feishu_fail", error=result))
                return False
    except Exception as e:
        print(t("feishu_error", error=str(e)))
        return False


def main():
    global LANGUAGE
    
    # 加载配置
    config = load_config()
    LANGUAGE = config.get("language", "zh")
    
    print("\n" + "="*50)
    print(f"🚀 HN News Digest - {datetime.now().strftime('%Y-%m-%d %H:%M')} [{LANGUAGE.upper()}]")
    print("="*50 + "\n")
    
    sources = load_sources(30)
    print(t("fetching", count=len(sources)))
    
    articles = fetch_articles(sources)
    print(t("done", count=len(articles)) + "\n")
    
    if not articles:
        print(t("no_articles"))
        return
    
    # 生成日报
    digest = generate_digest(articles, len(sources))
    
    # 保存
    today = datetime.now().strftime("%Y-%m-%d")
    output = f"/root/.openclaw/workspace/news-digest/{today}.md"
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        f.write(digest)
    print(t("saved", path=output))
    
    # 飞书推送
    send_feishu(digest, config)
    
    # 保存状态
    with open(STATE_PATH, "w") as f:
        json.dump({"last_updated": datetime.utcnow().isoformat()}, f)
    
    print("\n" + t("finish"))


if __name__ == "__main__":
    main()
