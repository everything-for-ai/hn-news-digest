#!/bin/bash
# 推送到 GitHub

# 设置 Git 用户信息（如果尚未设置）
git config user.name "Your Name"
git config user.email "your@email.com"

# 添加远程仓库（如果尚未添加）
# git remote add origin https://github.com/everything-for-ai/hn-news-digest.git

# 推送（需要 GitHub Personal Access Token）
# 方法1: 使用 git credentials
# echo "your_github_token" | git push origin main

# 方法2: 使用环境变量
# GITHUB_TOKEN=your_token gh repo sync

# 方法3: 手动推送后输入密码
git push origin main
