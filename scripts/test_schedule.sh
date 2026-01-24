#!/bin/bash

# 测试定时任务配置

echo "=========================================="
echo " 定时任务配置测试"
echo "=========================================="
echo ""

PLIST_PATH="~/Library/LaunchAgents/com.legalnews.daily.plist"

echo "📋 定时任务配置："
echo ""
echo "执行时间: 每天早上 8:00"
echo ""
echo "执行的脚本: /Users/apple/legal-daily-news-skill/scripts/fully_auto.sh"
echo ""
echo "日志文件:"
echo "   - 标准输出: /Users/apple/legal-daily-news-skill/logs/auto.log"
echo "   - 错误输出: /Users/apple/legal-daily-news-skill/logs/auto.error.log"
echo ""

echo "=========================================="
echo "当前状态:"
echo "=========================================="
echo ""

# 查看定时任务
if launchctl list | grep -q "com.legalnews.daily"; then
    echo "✅ 定时任务已加载"
    echo ""
    echo "任务详情:"
    launchctl list | grep "com.legalnews.daily"
else
    echo "❌ 定时任务未加载"
    echo ""
    echo "请运行以下命令加载:"
    echo "launchctl load ~/Library/LaunchAgents/com.legalnews.daily.plist"
fi

echo ""
echo "=========================================="
echo "测试选项:"
echo "=========================================="
echo ""
echo "1. 立即运行一次测试:"
echo "   launchctl start com.legalnews.daily"
echo ""
echo "2. 查看日志:"
echo "   tail -f logs/auto.log"
echo ""
echo "3. 查看错误日志:"
echo "   tail -f logs/auto.error.log"
echo ""
echo "4. 停止定时任务:"
echo "   launchctl unload ~/Library/LaunchAgents/com.legalnews.daily.plist"
echo ""
echo "5. 重新加载定时任务:"
echo "   launchctl unload ~/Library/LaunchAgents/com.legalnews.daily.plist"
echo "   launchctl load ~/Library/LaunchAgents/com.legalnews.daily.plist"
echo ""
