# 📰 HN News Digest

> Hacker News 热门博客每日精选 - 自动推送至飞书

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 特性

- 📡 聚合 Hacker News 2025 年最流行的 90+ 博客 RSS 源
- 📰 每日自动抓取最新文章（7天内）
- 🌐 支持 **中文** / **English** 双语输出
- 📱 自动推送到飞书（Lark）
- 💾 本地保存 Markdown 格式日报
- ⚙️ 可配置抓取源数量和文章数量

## 📦 安装

```bash
# 克隆项目
git clone https://github.com/everything-for-ai/hn-news-digest.git
cd hn-news-digest

# 安装依赖
pip install python-dateutil feedparser

# 配置飞书（可选）
# 编辑 config.json 设置 language: "zh" 或 "en"
```

## ⚡ 快速开始

```bash
# 运行脚本
python3 fetch.py

# 设置语言为英文
# 编辑 config.json: {"language": "en"}
```

## 📁 项目结构

```
hn-news-digest/
├── fetch.py              # 主脚本
├── config.json           # 配置文件
├── state.json            # 运行状态（自动生成）
├── hn-popular-blogs-2025.opml  # RSS 源列表
├── README.md             # 本文档
├── LICENSE               # MIT License
└── news-digest/          # 生成的日报（自动创建）
    └── YYYY-MM-DD.md
```

## ⚙️ 配置

### `config.json`

```json
{
    "language": "zh",      // "zh" = 中文, "en" = English
    "max_articles": 20,    // 每日推送文章数
    "days_limit": 7,      // 只抓取 N 天内的文章
    "feishu_enabled": true,  // 是否推送到飞书
    "youdao": {            // 有道翻译配置（可选）
        "app_key": "",
        "app_secret": ""
    },
    "feishu": {
        "app_id": "",
        "user_id": "",
        "secret_path": "~/.openclaw/secrets/feishu_app_secret"
    }
}
```

### 🌐 有道翻译（可选）

设置后文章标题会自动翻译成中文：

1. 打开 [有道开放平台](https://ai.youdao.com/console/group/order.html)
2. 注册账号并创建应用
3. 获取 **App Key** 和 **App Secret**
4. 编辑 `config.json` 填入：

```json
"youdao": {
    "app_key": "你的appKey",
    "app_secret": "你的appSecret"
}
```

> 💡 免费版有道翻译每月约 100 万字符额度

### 环境变量（飞书）

需要配置飞书应用凭证：

```bash
# 创建配置目录
mkdir -p ~/.openclaw/secrets

# 保存飞书 App Secret（从飞书开放平台获取）
echo "your_feishu_app_secret" > ~/.openclaw/secrets/feishu_app_secret
```

飞书配置说明：
- **App ID**: 从飞书开放平台获取
- **User ID**: 从飞书开放平台获取
- **App Secret**: 保存到 `~/.openclaw/secrets/feishu_app_secret`

## 🔧 定时任务

### OpenClaw Cron

```bash
# 每日 09:00 自动运行
openclaw cron add --name "hn-daily-digest" \
  --schedule '{"kind": "cron", "expr": "0 9 * * *"}' \
  --payload '{"kind": "systemEvent", "text": "推送每日HN新闻"}' \
  --session-target main
```

### Linux Crontab

```bash
# 编辑 crontab
crontab -e

# 添加每日 9 点运行
0 9 * * * /usr/bin/python3 /path/to/fetch.py >> /var/log/hn-digest.log 2>&1
```

## 📊 数据源

RSS 源来自 [HN Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/)，包含：

| 类别 | 代表博客 |
|------|---------|
| AI/ML | simonwillison.net, lcamtuf.substack.com |
| 安全 | krebsonsecurity.com, troyhunt.com |
| 编程 | overreacted.io, matklad.github.io |
| 商业 | paulgraham.com, steveblank.com |
| 科技 | daringfireball.net, righto.com |

完整列表见 [`hn-popular-blogs-2025.opml`](hn-popular-blogs-2025.opml)，可导入任意 RSS 阅读器。

## 📝 输出示例

### 中文版

```markdown
# 📰 HN 热门博客每日精选 - 2026-02-11

**来源**: HN 2025 (30 个订阅源)
**文章数**: 42 篇
---

### 1. Introducing Showboat and Rodney
📅 02-10 17:45 | [simonwillison.net](https://simonwillison.net)
🔗 [原文](https://simonwillison.net/...)
> A key challenge working with coding agents...

### 2. Patch Tuesday, February 2026 Edition
📅 02-10 21:49 | [krebsonsecurity.com](https://krebsonsecurity.com)
...
```

### English Version

```markdown
# 📰 HN Popular Blogs Daily - 2026-02-11

Source: HN 2025 (30 feeds)
Articles: 42
---

### 1. Introducing Showboat and Rodney
📅 02-10 17:45 | [simonwillison.net](https://simonwillison.net)
🔗 [Link](https://simonwillison.net/...)
> A key challenge working with coding agents...
```

## 🛠️ 开发

```bash
# 测试抓取（不推送）
python3 fetch.py

# 检查语法
python3 -m py_compile fetch.py

# 切换语言
# 编辑 config.json: {"language": "en"}
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🤝 致谢

- [Hacker News](https://news.ycombinator.com/) - 优质内容来源
- [HN Popularity Contest](https://refactoringenglish.com/tools/hn-popularity/) - 博客排名数据
- [Feedparser](https://feedparser.readthedocs.io/) - RSS 解析库
- [Everything for AI](https://github.com/everything-for-ai) - 开源组织

---

**Made with ❤️ by [Everything for AI](https://github.com/everything-for-ai)**
