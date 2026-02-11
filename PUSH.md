# 🚀 推送到 GitHub

## 方式 1: 使用 Personal Access Token

```bash
# 设置 GitHub Token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"

# 推送
cd /root/.openclaw/workspace/hn-news-digest
git push https://$GITHUB_TOKEN@github.com/everything-for-ai/hn-news-digest.git main
```

## 方式 2: 手动创建仓库后推送

1. 在 GitHub 创建仓库: https://github.com/organizations/everything-for-ai/repositories/new

2. 本地推送:
```bash
cd /root/.openclaw/workspace/hn-news-digest
git remote add origin https://github.com/everything-for-ai/hn-news-digest.git
git push -u origin main
```

## 方式 3: 使用 gh CLI

```bash
# 安装 gh CLI
brew install gh

# 登录
gh auth login

# 创建并推送
gh repo create hn-news-digest --org everything-for-ai --public --clone
cd hn-news-digest
cp /root/.openclaw/workspace/hn-news-digest/* .
git add .
git commit -m "Initial commit"
git push
```
