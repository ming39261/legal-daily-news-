# Git自动化与手动操作冲突解决方案

## 🎯 核心原则

**明确文件归属：**
- 🤖 **自动生成**：每日简报HTML（2026-01-XX.html）
- 👨 **手动维护**：index.html、设计主题脚本、工作流配置

---

## 📋 方案一：.gitignore 保护关键文件（推荐）

### 1. 保护紫色主题的index.html

```bash
# 修改.gitignore，让index.html不受GitHub Actions影响
```

**操作步骤：**
1. 将index.html从自动提交列表中移除
2. GitHub Actions只生成每日简报
3. 手动更新index.html时不会冲突

### 2. 修改GitHub Actions工作流

**当前问题：**
```yaml
git add "$TODAY.html" "output/archive/$TODAY.md" "output/archive/$TODAY.html" "index.html"
# ^^^ 这个会覆盖手动修改的index.html
```

**修改后：**
```yaml
git add "$TODAY.html" "archive/$TODAY.html" "output/archive/$TODAY.md" "output/archive/$TODAY.html"
# 只提交当日简报，不碰index.html
```

---

## 📋 方案二：分支策略优化

### 当前问题
- main和gh-pages频繁冲突
- GitHub Actions在两个分支都提交

### 解决方案

**选项A：只用gh-pages部署**
```yaml
# GitHub Actions只在gh-pages提交
- name: 提交到gh-pages
  run: |
    git checkout gh-pages
    git merge main --no-edit
    # 生成文件...
    git push origin gh-pages
```

**选项B：使用子目录**
```
main分支：
├── index.html (手动维护)
├── archive/ (手动维护归档)
└── .github/workflows/

gh-pages分支：
├── index.html (自动生成，可覆盖)
├── 2026-01-24.html
└── 2026-01-25.html
```

---

## 📋 方案三：本地预览 + 手动确认（最佳实践）

### 工作流程

```
1. 本地生成（每天早上8:05）
   └─ python3 scripts/generate_with_dedup.py
      └─ 查看preview/2026-01-26.md
      └─ 确认内容不重复
      └─ 手动转换为HTML
      └─ 本地测试

2. 手动提交（确认无误后）
   └─ git add .
   └─ git commit -m "Update: 2026-01-26 简报"
   └─ git push

3. GitHub Actions（可选备份）
   └─ 只用于部署，不生成内容
```

### 优点
- ✅ 完全掌控内容
- ✅ 避免自动化覆盖
- ✅ 可以先预览再发布

---

## 📋 方案四：Pre-commit钩子保护

### 安装pre-commit
```bash
pip install pre-commit
```

### 创建.pre-commit-config.yaml
```yaml
repos:
  - repo: local
    hooks:
      - id: protect-index-html
        name: 保护紫色主题index.html
        entry: bash -c 'git diff --cached index.html && echo "⚠️  index.html已修改，请确认是否使用紫色主题"'
        language: system
```

---

## 📋 方案五：使用Git分支保护

### GitHub仓库设置

1. **Settings → Branches**
2. **Add rule**: `main`分支
3. **勾选**：
   - ✅ Require pull request before merging
   - ✅ Require status checks to pass
4. **Exclude**: `.github/workflows/` 文件

---

## 🎯 推荐方案组合

### 最佳实践：方案一 + 方案三

**实施步骤：**

1. **修改GitHub Actions**（已完成✅）
   - 不自动提交index.html
   - 使用紫色主题脚本

2. **建立本地预览流程**（已创建✅）
   ```bash
   ./scripts/generate_local.sh
   ```

3. **手动确认后发布**
   - 查看preview文件
   - 确认是紫色主题
   - 手动git push

4. **保护关键文件**
   ```bash
   # 在本地仓库
   git update-index --skip-worktree index.html
   ```

---

## 🛠️ 立即可以做的操作

### 1. 锁定index.html（防止被覆盖）
```bash
# 告诉Git不要追踪index.html的更改
git update-index --assume-unchanged index.html

# 如果需要修改
git update-index --no-assume-unchanged index.html
```

### 2. 创建保护脚本
```bash
cat > scripts/safe_push.sh << 'EOF'
#!/bin/bash
echo "🔍 检查文件完整性..."

# 检查紫色主题
if ! grep -q "667eea" index.html; then
    echo "❌ 错误：index.html不是紫色主题！"
    echo "请检查后再提交"
    exit 1
fi

# 检查25号内容
if ! grep -q "食品安全" 2026-01-25.html; then
    echo "⚠️  警告：25号内容可能不对"
fi

echo "✅ 检查通过"
git push "$@"
EOF

chmod +x scripts/safe_push.sh
```

使用方式：
```bash
./scripts/safe_push.sh origin main
```

---

## 📝 新的每日流程（推荐）

### 方式A：完全手动（最安全）

```bash
# 1. 生成内容
python3 scripts/generate_with_dedup.py

# 2. 查看预览
cat preview/2026-01-26.md

# 3. 转换HTML
python3 scripts/md_to_purple_html.py output/archive/2026-01-26.md > 2026-01-26.html

# 4. 检查主题
grep "667eea" 2026-01-26.html

# 5. 安全推送
./scripts/safe_push.sh origin main
```

### 方式B：保留GitHub Actions（折中）

```yaml
# .github/workflows/daily-auto.yml 修改
on:
  schedule:
    - cron: '0 0 * * *'  # 北京时间8点
  workflow_dispatch:  # 手动触发

jobs:
  # 只在手动触发时运行
  manual-briefing:
    if: github.event_name == 'workflow_dispatch'
    ...
```

这样每天8点不会自动运行，只有手动触发才运行。

---

## 🎯 最终建议

**短期（立即）：**
1. ✅ 使用`git update-index --assume-unchanged index.html`
2. ✅ 创建safe_push.sh检查脚本
3. ✅ 修改GitHub Actions不提交index.html（已完成）

**中期（优化）：**
1. 建立本地预览流程
2. 每天手动确认后推送
3. 禁用GitHub Actions的自动运行

**长期（理想）：**
1. 完全手动控制发布流程
2. GitHub Actions只用于部署gh-pages
3. 使用CI/CD pipeline，但有审批步骤

---

需要我帮你实施哪个方案？最简单的方案1（锁定index.html）可以立即执行。
