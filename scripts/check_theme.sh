#!/bin/bash
# 检查并恢复紫色主题

echo "🔍 检查所有HTML文件的主题..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

issues_found=0

# 检查所有HTML文件
for file in index.html 20*.html archive/20*.html output/archive/20*.html; do
    if [ -f "$file" ]; then
        if grep -q "667eea" "$file"; then
            count=$(grep -c "667eea" "$file")
            echo -e "${GREEN}✅${NC} $file - 紫色主题 (${count}处)"
        else
            echo -e "${RED}❌${NC} $file - 不是紫色主题！"
            issues_found=$((issues_found + 1))
        fi
    fi
done

echo ""

if [ $issues_found -eq 0 ]; then
    echo -e "${GREEN}✅ 所有文件都是紫色主题！${NC}"
    exit 0
else
    echo -e "${RED}❌ 发现 ${issues_found} 个问题！${NC}"
    echo ""
    echo "是否自动恢复为紫色主题？"
    echo "  [y] 是，自动恢复"
    echo "  [n] 否，手动处理"
    read -p "请选择: " choice

    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        echo "🔄 正在恢复紫色主题..."
        # 这里可以调用恢复脚本
        echo "请手动运行：git show 365d0a3:index.html > index.html"
        exit 1
    else
        echo -e "${YELLOW}⚠️  请手动修复这些问题文件${NC}"
        exit 1
    fi
fi
