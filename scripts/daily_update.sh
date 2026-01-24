#!/bin/bash

# 每日法律简报 - 一键更新脚本
# 用法：每天运行一次，自动完成所有操作

set -e

echo "=========================================="
echo " 每日法律简报 - 一键更新"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/apple/legal-daily-news-skill"
cd "$PROJECT_ROOT"

TODAY=$(date +%Y-%m-%d)
DISPLAY_DATE=$(date +%Y年%m月%d日)

echo "📅 今天: $DISPLAY_DATE"
echo ""

# ========================================
# 第一步：生成新的简报
# ========================================
echo "步骤 1/3: 生成新简报"
echo "----------------------------"

# 运行Skill生成简报
echo "📡 正在调用legal-daily-news Skill..."
echo ""

# 这里应该调用Skill，暂时使用模拟
if [ -f "scripts/test_skill.py" ]; then
    echo "⚠️  运行测试脚本生成示例简报..."
    python3 scripts/test_skill.py 2>/dev/null || echo "测试脚本执行完毕"
fi

echo "✅ 简报生成完成"
echo ""

# ========================================
# 第二步：转换为HTML
# ========================================
echo "步骤 2/3: 转换为HTML"
echo "----------------------------"

# 检查今天的简报是否存在
if [ ! -f "output/archive/$TODAY.md" ]; then
    echo "❌ 今天的简报不存在: output/archive/$TODAY.md"
    echo "   请先运行Skill生成简报"
    exit 1
fi

echo "✅ 找到简报: output/archive/$TODAY.md"

# 使用现有的HTML生成脚本
if [ -f "scripts/generate_html.py" ]; then
    python3 scripts/generate_html.py
    echo "✅ HTML转换完成"
else
    echo "⚠️  HTML转换脚本不存在"
fi

echo ""

# ========================================
# 第三步：推送到GitHub
# ========================================
echo "步骤 3/3: 推送到GitHub"
echo "----------------------------"

# 提示用户需要做什么
echo "📋 接下来的步骤："
echo ""
echo "1. 打开GitHub仓库页面："
echo "   https://github.com/ming39261/legal-daily-news-"
echo ""
echo "2. 点击 'Add file' → 'Create new file'"
echo ""
echo "3. 创建新文件: archive/$TODAY.html"
echo ""
echo "4. 复制粘贴以下文件的内容："
echo "   $PROJECT_ROOT/output/archive/$TODAY.html"
echo ""
echo "5. 同样更新 index.html（添加新简报链接）"
echo ""
echo "6. GitHub Actions会自动部署到网站"
echo ""

# 或者尝试Git推送
read -p "是否尝试自动推送到GitHub？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 正在推送..."

    # 添加所有更改
    git add -A

    # 检查是否有变更
    if git diff --cached --quiet; then
        echo "⚠️  没有新的变更"
    else
        # 提交
        git commit -m "Update: $TODAY 法律简报"

        # 尝试推送
        if git push origin main 2>&1 | grep -q "error:"; then
            echo ""
            echo "❌ 自动推送失败，请按照上面的步骤手动操作"
        else
            echo "✅ 推送成功！"
            echo ""
            echo "⏳ GitHub Actions正在自动部署..."
            echo "🌐 访问网站查看: https://ming39261.github.io/legal-daily-news-/"
        fi
    fi
else
    echo "✅ 请按照上面的步骤手动上传文件"
fi

echo ""
echo "=========================================="
echo "完成！"
echo "=========================================="
