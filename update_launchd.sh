#!/bin/bash
# 更新launchd配置脚本

echo "🔄 更新定时任务配置..."
echo ""

PLIST_DIR="$HOME/Library/LaunchAgents"

# 1. 更新主定时任务（8:05运行）
echo "📋 更新主定时任务..."
cp com.legalnews.daily.plist "$PLIST_DIR/"
launchctl unload "$PLIST_DIR/com.legalnews.daily.plist" 2>/dev/null
launchctl load "$PLIST_DIR/com.legalnews.daily.plist"

# 2. 添加开机检查任务
echo "🔧 添加开机检查任务..."
cp com.legalnews.daily.bootcheck.plist "$PLIST_DIR/"
launchctl unload "$PLIST_DIR/com.legalnews.daily.bootcheck.plist" 2>/dev/null
launchctl load "$PLIST_DIR/com.legalnews.daily.bootcheck.plist"

echo ""
echo "✅ 配置更新完成！"
echo ""
echo "📅 任务列表："
echo "   1. 主任务：每天8:05定时运行"
echo "   2. 开机检查：开机后检查并补运行（如已错过8:05）"
echo ""
echo "🔍 查看任务状态："
echo "   launchctl list | grep legalnews"
echo ""
echo "📝 查看开机检查日志："
echo "   cat logs/boot-$(date +%Y%m%d).log"
