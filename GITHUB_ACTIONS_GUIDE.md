# 🚀 GitHub Actions 完全云自动化配置指南

## ✨ 优势

**无需你的电脑开机！** GitHub在云端服务器上自动运行所有任务。

- ✅ 24/7运行，不受本地电脑影响
- ✅ 完全免费
- ✅ 自动采集、生成、部署
- ✅ 每天北京时间早上8点自动更新

---

## 📋 配置步骤

### 第一步：添加GitHub Secrets（密钥）

1. **打开GitHub仓库**
   ```
   https://github.com/ming39261/legal-daily-news-/settings/secrets/actions
   ```

2. **点击** `New repository secret`

3. **添加以下密钥**：

   #### 密钥1：GLM_API_KEY（必需）
   - Name: `GLM_API_KEY`
   - Value: `e96fd3e53ceb4ec3ac3c83053bbdf900.uTaVfpKoG49JeptV`
   - 点击 `Add secret`

   #### 密钥2：TAVILY_API_KEY（可选）
   - Name: `TAVILY_API_KEY`
   - Value: 你的Tavily API密钥（如果有的话）
   - 点击 `Add secret`

---

### 第二步：启用GitHub Actions

1. **打开Actions设置**
   ```
   https://github.com/ming39261/legal-daily-news-/actions
   ```

2. **点击** `I understand my workflows, go ahead and enable them`（如果提示的话）

3. **手动测试运行**

   点击左侧的 `每日法律简报 - 完全自动化` workflow

   点击右侧 `Run workflow` → `Run workflow`

   等待运行完成

---

### 第三步：查看运行日志

1. 在Actions页面，点击最新的运行记录

2. 点击每个步骤查看详细日志

3. 确认所有步骤都成功（绿色✅）

---

## ⏰ 定时说明

- **运行时间**：每天北京时间早上8:00
- **UTC时间**：每天UTC 0:00
- **Cron表达式**：`0 0 * * *`

### 修改运行时间

编辑 `.github/workflows/daily-auto.yml` 文件：

```yaml
schedule:
  # 北京时间早上8点
  - cron: '0 0 * * *'

  # 改为北京时间早上9点（UTC 1点）
  # - cron: '0 1 * * *'

  # 改为每天运行两次（早上8点和晚上8点）
  # - cron: '0 0,12 * * *'
```

---

## 🔧 工作流程详解

```
GitHub Actions (每天UTC 0:00自动触发)
  │
  ├─ 1️⃣ 采集法律资讯
  │   └─ 调用Tavily API或使用模板
  │
  ├─ 2️⃣ AI生成简报
  │   └─ 调用GLM-4.7 API生成内容
  │
  ├─ 3️⃣ 转换HTML
  │   └─ Python脚本转换格式
  │
  ├─ 4️⃣ Git提交
  │   └─ 自动commit和push
  │
  └─ 5️⃣ 部署到GitHub Pages
      └─ 自动发布到网站
```

---

## 📊 运行状态监控

### 查看运行历史
```
https://github.com/ming39261/legal-daily-news-/actions
```

### 查看最新简报
```
https://ming39261.github.io/legal-daily-news-/
```

---

## 🆕 手动触发（立即运行）

如果不想等到定时任务，可以手动触发：

1. 打开Actions页面
2. 点击 `每日法律简报 - 完全自动化`
3. 点击 `Run workflow` 按钮
4. 选择分支 `main`
5. 点击 `Run workflow`

---

## ❓ 常见问题

### Q1: Actions显示失败怎么办？

**A:** 查看运行日志，找到失败的步骤：

1. 点击红色的失败步骤
2. 查看错误信息
3. 常见原因：
   - API密钥未配置或错误
   - 网络连接问题
   - 脚本语法错误

### Q2: 如何修改生成的内容？

**A:** 编辑以下文件：
- `scripts/auto_collect.py` - 采集逻辑
- `scripts/generate_brief.py` - AI生成逻辑
- `scripts/generate_html.py` - HTML转换逻辑

修改后提交到GitHub，下次运行会使用新代码。

### Q3: 运行时间不准确？

**A:** GitHub Actions使用UTC时间，需要注意时区转换：

- 北京时间 = UTC + 8
- 北京时间早上8点 = UTC 0点
- Cron表达式: `0 0 * * *`

### Q4: 如何查看API使用情况？

**A:**
- GLM API: 登录智谱AI开放平台查看
- GitHub Actions: 在Actions页面查看运行记录

### Q5: 可以更改运行频率吗？

**A:** 可以，修改`.github/workflows/daily-auto.yml`中的cron表达式：

```yaml
# 每小时运行一次
- cron: '0 * * * *'

# 每天运行两次（早晚8点）
- cron: '0 0,12 * * *'

# 每周一运行
- cron: '0 0 * * 1'
```

---

## 🎉 完成！

现在你的法律简报系统**完全自动化**了！

- ✅ 无需本地电脑开机
- ✅ 云端自动运行
- ✅ 每天自动更新
- ✅ 完全免费

**每天早上8点，网站自动更新，无需任何操作！** 🎊

---

## 📚 参考资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [Cron表达式帮助](https://crontab.guru/)
- [GitHub Secrets管理](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
