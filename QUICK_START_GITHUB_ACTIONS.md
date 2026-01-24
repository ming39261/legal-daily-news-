# ⚡ GitHub Actions 云自动化 - 快速配置

## 🎯 只需3步，实现完全云自动化！

### 步骤1️⃣: 添加API密钥到GitHub（2分钟）

1. **打开密钥管理页面**
   ```
   https://github.com/ming39261/legal-daily-news-/settings/secrets/actions
   ```

2. **点击绿色按钮** `New repository secret`

3. **添加GLM API密钥**
   - Name (名称): `GLM_API_KEY`
   - Secret (密钥): `e96fd3e53ceb4ec3ac3c83053bbdf900.uTaVfpKoG49JeptV`

4. **点击** `Add secret`

✅ **密钥配置完成！**

---

### 步骤2️⃣: 手动测试运行（3分钟）

1. **打开Actions页面**
   ```
   https://github.com/ming39261/legal-daily-news-/actions
   ```

2. **点击左侧** `每日法律简报 - 完全自动化`

3. **点击右侧蓝色按钮** `Run workflow`

4. **确认运行** → 点击绿色 `Run workflow`

5. **等待运行完成**（大约1-2分钟）
   - 每个步骤会显示✅（成功）或❌（失败）
   - 点击步骤可以查看详细日志

---

### 步骤3️⃣: 完成！🎉

**配置完成后：**
- ✅ 每天北京时间早上8:00自动运行
- ✅ 无需你的电脑开机
- ✅ 自动采集、生成、部署
- ✅ 完全免费

---

## 🌐 访问你的网站

```
https://ming39261.github.io/legal-daily-news-/
```

---

## 📊 查看运行状态

**Actions页面**：
```
https://github.com/ming39261/legal-daily-news-/actions
```

可以看到：
- 历史运行记录
- 每次运行的状态
- 详细的执行日志

---

## 🆕 手动触发（可选）

如果不想等到明天早上8点，可以立即运行：

1. 打开Actions页面
2. 点击 `每日法律简报 - 完全自动化`
3. 点击 `Run workflow` → `Run workflow`

---

## ⏰ 定时说明

- **北京时间早上8:00** 自动运行
- 使用UTC时间（0点）
- Cron表达式: `0 0 * * *`

### 修改运行时间

编辑仓库中的 `.github/workflows/daily-auto.yml` 文件，找到这行：

```yaml
schedule:
  - cron: '0 0 * * *'  # 北京时间早上8点
```

改为：

```yaml
schedule:
  - cron: '0 1 * * *'  # 北京时间早上9点
  # 或
  - cron: '0 0,12 * * *'  # 每天早晚8点运行两次
```

保存后GitHub会自动使用新的时间。

---

## 📋 配置检查清单

完成以下步骤后打勾：

- [ ] 添加了GLM_API_KEY到GitHub Secrets
- [ ] 手动测试运行成功
- [ ] 查看了运行日志
- [ ] 网站能正常访问

---

## ❓ 遇到问题？

### 问题1: Actions显示失败

**解决方法**：
1. 点击红色的失败步骤
2. 查看错误信息
3. 检查是否添加了API密钥
4. 检查密钥值是否正确

### 问题2: 没有看到Actions

**解决方法**：
1. 确认在正确的页面：`/actions`
2. 点击 `I understand my workflows` 启用Actions

### 问题3: 网站没有更新

**解决方法**：
1. 等待2-3分钟，GitHub Pages需要部署时间
2. 检查Actions是否运行成功
3. 清除浏览器缓存后刷新

---

## 🎉 成功案例

配置成功后，你会看到：

```
GitHub Actions
│
├─ ✅ 1. 检出代码
├─ ✅ 2. 设置Python
├─ ✅ 3. 安装依赖
├─ ✅ 4. 采集法律资讯
├─ ✅ 5. AI生成简报
├─ ✅ 6. 转换为HTML
├─ ✅ 7. 提交到仓库
└─ ✅ 8. 部署到GitHub Pages
```

所有步骤都是绿色✅，表示成功！

---

## 🚀 现在开始配置吧！

**第一步：添加API密钥**

点击这个链接：
```
https://github.com/ming39261/legal-daily-news-/settings/secrets/actions
```

然后按照上面的步骤操作即可！

---

**配置好后告诉我，我帮你检查是否成功！** 🎊
