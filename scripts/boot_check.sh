#!/bin/bash
# 开机后补运行脚本（检查并生成今日简报）

PROJECT_DIR="/Users/apple/legal-daily-news-skill"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/boot-$(date +%Y%m%d).log"
TODAY=$(date +%Y-%m-%d)
NOW_HOUR=$(date +%H)

mkdir -p "$LOG_DIR"

echo "🔄 开机检查：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"

cd "$PROJECT_DIR" || exit 1

# 检查今日简报是否已存在
if [ -f "output/archive/$TODAY.md" ]; then
    echo "✅ 今日简报已存在，无需生成" | tee -a "$LOG_FILE"
    exit 0
fi

# 检查当前时间是否在合理范围内（避免半夜运行）
if [ "$NOW_HOUR" -lt 6 ] || [ "$NOW_HOUR" -ge 23 ]; then
    echo "⏰ 当前时间不适宜生成（$NOW_HOUR点），等待定时任务" | tee -a "$LOG_FILE"
    exit 0
fi

# 如果在8:00-12:00之间，说明8:05的定时任务可能错过了
if [ "$NOW_HOUR" -ge 8 ] && [ "$NOW_HOUR" -lt 12 ]; then
    echo "📝 检测到8:05定时任务可能已错过，立即生成简报..." | tee -a "$LOG_FILE"

    # 运行自动生成脚本
    ./scripts/auto_generate_and_push.sh >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ 开机补运行成功" | tee -a "$LOG_FILE"
        osascript -e 'display notification "每日法律简报" with title "🔄 开机补运行成功"' 2>/dev/null
    else
        echo "❌ 开机补运行失败" | tee -a "$LOG_FILE"
        osascript -e 'display notification "每日法律简报" with title "❌ 开机补运行失败"' 2>/dev/null
    fi
else
    echo "⏰ 等待8:05定时任务运行" | tee -a "$LOG_FILE"
fi
