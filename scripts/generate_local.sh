#!/bin/bash
# 本地生成简报脚本（自动发布版）

echo "📅 开始生成每日法律简报..."
echo "========================================"

# 设置环境变量（如果有API密钥）
export GLM_API_KEY="${GLM_API_KEY:-e96fd3e53ceb4ec3ac3c83053bbdf900.uTaVfpKoG49JeptV}"

# 运行生成脚本（自动确认）
cd /Users/apple/legal-daily-news-skill

# 检查今天的简报是否已存在
TODAY=$(date +%Y-%m-%d)
if [ -f "output/archive/$TODAY.md" ]; then
    echo "⚠️  今天的简报已存在: output/archive/$TODAY.md"
    echo ""
    read -p "是否要重新生成? [y/N]: " choice
    if [ "$choice" != "y" ] && [ "$choice" != "Y" ]; then
        echo "❌ 已取消"
        exit 0
    fi
    # 备份现有文件
    mv "output/archive/$TODAY.md" "output/archive/$TODAY.md.backup"
fi

# 生成简报
python3 scripts/generate_with_dedup.py

echo ""
echo "========================================"
echo "✅ 生成完成!"
echo ""
echo "📂 文件位置:"
echo "   - 预览: preview/$TODAY.md"
echo "   - 正式: output/archive/$TODAY.md"
echo ""
echo "📊 下一步:"
echo "   1. 查看预览: cat preview/$TODAY.md"
echo "   2. 转换HTML: python3 scripts/generate_html.py output/archive/$TODAY.md > $TODAY.html"
echo "   3. 提交GitHub: git add . && git commit -m 'Auto: $TODAY 法律简报'"
