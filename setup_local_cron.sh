#!/bin/bash
# 安装macOS定时任务（launchd）

echo "🚀 设置本地定时任务..."
echo ""

# 创建日志目录
mkdir -p logs

# 复制plist文件到LaunchDaemons
PLIST_FILE="com.legalnews.daily.plist"
LAUNCH_DAEMTS="$HOME/Library/LaunchAgents"

echo "📋 安装定时任务..."
cp "$PLIST_FILE" "$LAUNCH_DAEMTS/"

echo "🔧 加载定时任务..."
launchctl unload "$LAUNCH_DAEMTS/$PLIST_FILE" 2>/dev/null
launchctl load "$LAUNCH_DAEMTS/$PLIST_FILE"

echo ""
echo "✅ 安装完成！"
echo ""
echo "📅 任务信息："
echo "   - 运行时间：每天早上8:05"
echo "   - 运行脚本：scripts/auto_generate_and_push.sh"
echo "   - 日志位置：logs/auto-YYYYMMDD.log"
echo ""
echo "🔍 查看日志："
echo "   tail -f logs/auto-$(date +%Y%m%d).log"
echo ""
echo "📝 查看任务状态："
echo "   launchctl list | grep legalnews"
echo ""
echo "⚠️  注意：电脑需要在8:05时开机才能运行"
echo ""
echo "💡 手动测试："
echo "   ./scripts/auto_generate_and_push.sh"
