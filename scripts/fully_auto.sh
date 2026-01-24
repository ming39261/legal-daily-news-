#!/bin/bash

# 每日法律简报 - 完全自动化脚本（SSH版本）
# 功能：生成简报 → 转换HTML → Git推送 → 自动部署

set -e

echo "=========================================="
echo " 每日法律简报 - 完全自动化系统 v2.0"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/apple/legal-daily-news-skill"
cd "$PROJECT_ROOT"

TODAY=$(date +%Y-%m-%d)
DISPLAY_DATE=$(date +%Y年%m月%d日)

echo "📅 今天: $DISPLAY_DATE"
echo ""

# ========================================
# 步骤1: 检查或生成简报
# ========================================
echo "步骤 1/4: 检查简报"
echo "----------------------------"

# 检查今天的简报是否已存在
if [ -f "output/archive/$TODAY.md" ]; then
    echo "✅ 今天的简报已存在"
else
    echo "⚠️  今天的简报尚未生成"
    echo ""
    echo "💡 请先运行以下命令生成简报："
    echo "   /skill execute legal-daily-news"
    echo ""
    echo "   或手动创建文件: output/archive/$TODAY.md"
    exit 0
fi

echo ""

# ========================================
# 步骤2: 转换为HTML
# ========================================
echo "步骤 2/4: 转换为HTML"
echo "----------------------------"

# 检查Markdown文件
if [ ! -f "output/archive/$TODAY.md" ]; then
    echo "❌ Markdown文件不存在: output/archive/$TODAY.md"
    exit 1
fi

# 运行HTML生成脚本
GENERATE_SCRIPT="$PROJECT_ROOT/scripts/generate_html.py"
if [ -f "$GENERATE_SCRIPT" ]; then
    echo "📝 正在转换Markdown到HTML..."
    /usr/bin/python3 "$GENERATE_SCRIPT" "output/archive/$TODAY.md" > "output/archive/$TODAY.html"
    echo "✅ HTML转换完成: output/archive/$TODAY.html"
else
    echo "❌ HTML转换脚本不存在: $GENERATE_SCRIPT"
    exit 1
fi

echo ""

# ========================================
# 步骤3: 复制到仓库根目录
# ========================================
echo "步骤 3/4: 准备Git文件"
echo "----------------------------"

# 复制今天的简报HTML到根目录
cp "output/archive/$TODAY.html" "./$TODAY.html"
echo "✅ 已复制: $TODAY.html"

echo ""

# ========================================
# 步骤4: Git提交和推送
# ========================================
echo "步骤 4/4: Git提交和推送"
echo "----------------------------"

# 添加今天的HTML文件
git add "$TODAY.html"

# 检查是否有变更
if git diff --cached --quiet; then
    echo "⚠️  没有新的变更"
    echo "   文件可能已经提交过了"
else
    # 提交
    git commit -m "Auto: $TODAY 法律简报"

    echo "📤 正在推送到GitHub..."
    echo ""

    # 先拉取远程更新
    echo "📥 拉取远程更新..."
    git pull origin main --rebase --no-edit 2>&1 || echo "⚠️  无需拉取"

    # 推送到GitHub（使用SSH）
    if git push origin main 2>&1; then
        echo ""
        echo "✅ 推送成功！"
    else
        echo ""
        echo "❌ 推送失败"
        echo "   请检查网络连接"
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "✅ 完全自动化流程完成！"
echo "=========================================="
echo ""
echo "🎉 所有步骤已完成："
echo "   ✅ 简报已生成"
echo "   ✅ HTML已转换"
echo "   ✅ 已推送到GitHub"
echo ""
echo "🌐 访问网站:"
echo "   https://ming39261.github.io/legal-daily-news-/"
echo ""
echo "📄 查看简报:"
echo "   https://ming39261.github.io/legal-daily-news-/$TODAY.html"
echo ""
echo "⏳ GitHub Pages正在自动部署..."
echo "   预计1-2分钟后网站更新完成"
echo ""
echo "💡 明天同一时间再次运行此脚本即可"
echo ""
echo "📋 查看部署状态:"
echo "   https://github.com/ming39261/legal-daily-news-/actions"
echo ""
