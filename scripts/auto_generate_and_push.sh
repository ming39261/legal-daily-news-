#!/bin/bash
# 本地自动生成简报脚本（用于launchd定时调用）

# 设置
PROJECT_DIR="/Users/apple/legal-daily-news-skill"
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/auto-$(date +%Y%m%d).log"
TODAY=$(date +%Y-%m-%d)

# 创建日志目录
mkdir -p "$LOG_DIR"

# 记录开始时间
echo "========================================" | tee -a "$LOG_FILE"
echo "📅 开始生成每日简报：$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"

# 切换到项目目录
cd "$PROJECT_DIR" || {
    echo "❌ 错误：无法切换到项目目录 $PROJECT_DIR" | tee -a "$LOG_FILE"
    exit 1
}

# 1. 检查今日简报是否已存在
if [ -f "output/archive/$TODAY.md" ]; then
    echo "⚠️  今日简报已存在，跳过生成" | tee -a "$LOG_FILE"
    exit 0
fi

# 2. 生成简报（带去重，非交互模式）
echo "🤖 正在生成简报内容..." | tee -a "$LOG_FILE"
AUTO_CONFIRM=true python3 scripts/generate_with_dedup.py >> "$LOG_FILE" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ 简报生成失败" | tee -a "$LOG_FILE"
    exit 1
fi

# 3. 检查预览文件
if [ ! -f "preview/$TODAY.md" ]; then
    echo "❌ 预览文件不存在" | tee -a "$LOG_FILE"
    exit 1
fi

# 4. 转换为HTML（紫色主题）
echo "🎨 正在转换为紫色主题HTML..." | tee -a "$LOG_FILE"
python3 scripts/md_to_purple_html.py "output/archive/$TODAY.md" > "$TODAY.html" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ HTML转换失败" | tee -a "$LOG_FILE"
    exit 1
fi

# 5. 复制到各位置
echo "📋 正在复制文件到各位置..." | tee -a "$LOG_FILE"
cp "$TODAY.html" "archive/$TODAY.html" 2>&1 | tee -a "$LOG_FILE"
cp "$TODAY.html" "output/archive/$TODAY.html" 2>&1 | tee -a "$LOG_FILE"

# 6. 检查主题
echo "🔍 正在检查主题..." | tee -a "$LOG_FILE"
if ! grep -q "667eea" "$TODAY.html"; then
    echo "❌ 错误：生成的HTML不是紫色主题！" | tee -a "$LOG_FILE"
    exit 1
fi

# 7. 提交到Git
echo "📤 正在提交到Git..." | tee -a "$LOG_FILE"
git add output/archive/$TODAY.md "$TODAY.html" archive/$TODAY.html output/archive/$TODAY.html preview/$TODAY.md >> "$LOG_FILE" 2>&1

if git diff --staged --quiet; then
    echo "⚠️  没有新的变更需要提交" | tee -a "$LOG_FILE"
else
    git commit -m "Auto: $TODAY 法律简报" >> "$LOG_FILE" 2>&1

    # 8. 推送到GitHub
    echo "🚀 正在推送到GitHub..." | tee -a "$LOG_FILE"
    ./scripts/safe_push.sh origin main >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        echo "✅ 成功推送到GitHub" | tee -a "$LOG_FILE"

        # 发送通知（可选）
        osascript -e 'display notification "每日法律简报" with title "✅ 生成成功"' 2>/dev/null
    else
        echo "❌ 推送失败" | tee -a "$LOG_FILE"
        osascript -e 'display notification "每日法律简报" with title "❌ 推送失败"' 2>/dev/null
        exit 1
    fi
fi

echo "✅ 任务完成！$(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 清理旧日志（保留最近30天）
find "$LOG_DIR" -name "auto-*.log" -mtime +30 -delete 2>/dev/null
