#!/bin/bash

# 每日法律简报 - 一键部署到GitHub Pages
# 使用脚本自动完成部署流程

set -e

echo "=========================================="
echo " 每日法律简报 - 一键部署脚本"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/apple/legal-daily-news-skill"
cd "$PROJECT_ROOT"

# 检查是否已有远程仓库
if git remote | grep -q "origin"; then
    echo "⚠️  检测到已有远程仓库配置"
    git remote -v
    echo ""
    echo "是否使用现有仓库？(y/n)"
    read -r USE_EXISTING

    if [ "$USE_EXISTING" != "y" ]; then
        git remote remove origin
        NEED_NEW=true
    else
        NEED_NEW=false
    fi
else
    NEED_NEW=true
fi

# 步骤1: 创建GitHub仓库
if [ "$NEED_NEW" = true ]; then
    echo ""
    echo "步骤 1/5: 创建GitHub仓库"
    echo "----------------------------"
    echo ""
    echo "📝 请按以下步骤操作："
    echo ""
    echo "1. 访问 https://github.com/new"
    echo "2. 填写仓库信息："
    echo "   - 仓库名称: legal-daily-news"
    echo "   - 描述: 每日法律简报 - AI驱动的法律资讯聚合平台"
    echo "   - 可见性: Public (公开) 或 Private (私有)"
    echo "   - ⚠️  不要勾选 'Add a README file' (我们已经有了)"
    echo "   - ⚠️  不要勾选 'Add .gitignore' (我们已经有了)"
    echo ""
    echo "3. 点击 'Create repository' 创建仓库"
    echo ""
    echo "创建完成后，按回车继续..."
    read -r

    # 获取用户名
    echo ""
    echo "请输入你的GitHub用户名:"
    read -r GITHUB_USERNAME

    # 添加远程仓库
    REPO_URL="https://github.com/$GITHUB_USERNAME/legal-daily-news.git"
    git remote add origin "$REPO_URL"

    echo ""
    echo "✓ 远程仓库已添加: $REPO_URL"
fi

# 步骤2: 推送到GitHub
echo ""
echo "步骤 2/5: 推送代码到GitHub"
echo "----------------------------"
echo ""
echo "📤 正在推送代码..."

if git push -u origin main 2>&1 | tee /tmp/git_push.log; then
    echo ""
    echo "✅ 代码推送成功！"
else
    echo ""
    echo "❌ 推送失败，请检查："
    echo "1. GitHub Token是否正确配置"
    echo "2. 仓库名称是否正确"
    echo "3. 网络连接是否正常"
    echo ""
    echo "错误信息:"
    cat /tmp/git_push.log
    exit 1
fi

# 步骤3: 配置GitHub Pages
echo ""
echo "步骤 3/5: 配置GitHub Pages"
echo "----------------------------"
echo ""
echo "📝 接下来需要手动配置GitHub Pages："
echo ""
echo "1. 访问你的GitHub仓库页面"
echo "   例如: https://github.com/$GITHUB_USERNAME/legal-daily-news"
echo ""
echo "2. 点击 'Settings' 标签"
echo ""
echo "3. 在左侧菜单中找到 'Pages'"
echo ""
echo "4. 配置以下选项："
echo "   - **Source**: Deploy from a branch"
    echo "   - **Branch**: main"
    echo "   - **Folder**: /(root)"
    echo ""
    echo "5. 点击 'Save' 保存"
echo ""
echo "⏳  等待1-2分钟部署完成..."
echo ""

# 步骤4: 等待用户配置完成
echo "配置完成后按回车继续..."
read -r

# 步骤5: 访问网站
echo ""
echo "步骤 4/5: 访问你的网站"
echo "----------------------------"
echo ""
echo "🌐 你的网站地址是:"
echo "   https://$GITHUB_USERNAME.github.io/legal-daily-news/"
echo ""
echo "   (或者显示为: https://$GITHUB_USERNAME.github.io/legal-daily-news/index.html)"
echo ""
echo "📌 请收藏这个地址！"
echo ""

# 完成
echo ""
echo "=========================================="
echo "✅ 部署完成！"
echo "=========================================="
echo ""
echo "📊 部署信息:"
echo "   仓库地址: https://github.com/$GITHUB_USERNAME/legal-daily-news"
echo "   网站地址: https://$GITHUB_USERNAME.github.io/legal-daily-news/"
echo ""
echo "📝 后续更新流程:"
echo "   1. 生成新简报: /skill execute legal-daily-news"
echo "   2. 推送到GitHub: git push"
echo "   3. 网站自动更新 (1-2分钟)"
echo ""
echo "🎉 恭喜！你的法律简报网站已经上线！"
echo ""
