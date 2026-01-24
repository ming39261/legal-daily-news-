#!/bin/bash

# 快速部署今天的简报到GitHub

echo "=========================================="
echo " 快速部署 - 今天(2026-01-24)的简报"
echo "=========================================="
echo ""

PROJECT_ROOT="/Users/apple/legal-daily-news-skill"
cd "$PROJECT_ROOT"

TODAY="2026-01-24"

echo "📅 日期: $TODAY"
echo ""

# 检查Markdown文件是否存在
if [ ! -f "output/archive/$TODAY.md" ]; then
    echo "❌ Markdown文件不存在: output/archive/$TODAY.md"
    exit 1
fi

echo "✅ Markdown文件存在"

# 检查HTML文件是否存在
if [ ! -f "output/archive/$TODAY.html" ]; then
    echo "⚠️  HTML文件不存在，需要先生成..."
    echo ""
    echo "请复制以下HTML内容到GitHub："
    echo ""
    echo "文件路径: archive/$TODAY.html"
    echo ""

    # 如果有generate_html.py，尝试生成
    if [ -f "scripts/generate_html.py" ]; then
        echo "正在生成HTML..."
        python3 scripts/generate_html.py "output/archive/$TODAY.md" > "output/archive/$TODAY.html" 2>&1

        if [ -f "output/archive/$TODAY.html" ]; then
            echo "✅ HTML生成成功"
        else
            echo "❌ HTML生成失败"
            echo "   请使用手动方式上传"
            exit 1
        fi
    fi
else
    echo "✅ HTML文件已存在"
fi

echo ""
echo "📤 准备上传到GitHub..."
echo ""

# 使用Python脚本上传
if [ -f "scripts/auto_upload_to_github.py" ]; then
    python3 scripts/auto_upload_to_github.py
else
    echo "❌ 上传脚本不存在"
    exit 1
fi

echo ""
echo "✅ 完成！"
