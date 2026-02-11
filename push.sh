#!/bin/bash
# 推送到 GitHub

if [ -z "$1" ]; then
    echo "用法: ./push.sh <github_token>"
    echo "示例: ./push.sh ghp_xxxxxxxxxxxx"
    exit 1
fi

echo "🚀 推送到 GitHub..."
git push "https://$1@github.com/everything-for-ai/hn-news-digest.git" main
