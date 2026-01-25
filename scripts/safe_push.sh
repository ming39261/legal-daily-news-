#!/bin/bash
# 安全推送脚本 - 防止覆盖紫色主题

echo "🔍 检查文件完整性..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查index.html是否是紫色主题
if grep -q "667eea" index.html; then
    echo -e "${GREEN}✅ index.html 是紫色主题${NC}"
else
    echo -e "${RED}❌ 错误：index.html 不是紫色主题！${NC}"
    echo -e "${RED}   可能会被GitHub Actions覆盖为深海蓝主题${NC}"
    echo ""
    read -p "是否继续推送？[y/N]: " choice
    if [ "$choice" != "y" ] && [ "$choice" != "Y" ]; then
        echo -e "${YELLOW}⚠️  已取消推送${NC}"
        exit 1
    fi
fi

# 检查最新的简报文件
TODAY=$(date +%Y-%m-%d)
if [ -f "${TODAY}.html" ]; then
    if grep -q "667eea" "${TODAY}.html"; then
        echo -e "${GREEN}✅ ${TODAY}.html 是紫色主题${NC}"
    else
        echo -e "${YELLOW}⚠️  警告：${TODAY}.html 可能不是紫色主题${NC}"
    fi
fi

# 统计紫色主题代码出现次数
count=$(grep -c "667eea" index.html 2>/dev/null || echo "0")
if [ "$count" -gt 5 ]; then
    echo -e "${GREEN}✅ index.html 包含 ${count} 处紫色主题代码${NC}"
fi

echo ""
echo -e "${GREEN}✅ 所有检查通过！${NC}"
echo "📝 即将推送到远程仓库..."
echo ""

# 执行git push
git push "$@"

exit_code=$?
if [ $exit_code -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 推送成功！${NC}"
else
    echo ""
    echo -e "${RED}❌ 推送失败，错误代码：${exit_code}${NC}"
fi

exit $exit_code
