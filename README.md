# MM Trading Bot Logs

MM Trading Bot 每日中文变动日志。每天北京时间 **20:00**，由本地 Codex 定时任务检查项目各子仓库的实际提交，整理功能变化并推送到本仓库。

- 日志仓库：https://github.com/smallyunet/mm-trading-bot-logs
- 在线阅读：https://smallyunet.github.io/mm-trading-bot-logs/
- 参考 Virae Logs 的公开日志与静态页面形式，独立保存 MM Trading Bot 的内容。

## 汇总范围

扫描本仓库父目录下的直接子 Git 仓库，排除本日志仓库。目前包括 `eth-wallet-generator`、`trading-bot`、`trading-bot-dashboard`，以后新增的项目子仓库也会自动发现。

从 2026-09-13 开始，只收录当前检出分支可达、作者名精确等于 `smallyunet` 的非合并提交。未提交改动不进入日报；不扫描整个 GitHub 账号的仓库，也不采集其他本地定时任务的内容。跨仓库的同一功能合并说明，附 GitHub commit 链接。代码提交不等于生产部署。

没有新提交时写明「今日无新增符合条件的提交」，不编造更新。相同日期重复执行时更新同一篇日志，保留此前已收录内容。停机漏跑后，下次运行收录尚未报道的提交并注明覆盖时间，不伪造过去的运行记录。

## 本地操作

需要 Python 3.9+、Git、已登录的 GitHub CLI；无第三方 Python 依赖。

```sh
python3 scripts/collect.py > pending.json
python3 -m unittest discover -s tests -v
python3 scripts/build.py --check
python3 -m http.server 8000 --directory _site
```

`collect.py` 只读取来源仓库，输出候选提交元数据；AI 必须继续检查实际 diff 才能撰写日志。它不会生成内容、提交或推送。`pending.json` 被 Git 忽略。

- `logs/YYYY-MM-DD.md`：公开中文日报，首行必须为一级标题。
- `data/config.json`：作者、起始日期与排除规则。
- `data/receipts/YYYY-MM-DD.json`：日报已收录的仓库名及提交 SHA，用于去重；这是内容清单，不是部署成功证明。
- `scripts/build.py`、`assets/`：生成带搜索、日历导航的静态站点。
- `.github/workflows/pages.yml`：main 推送后验证并发布 GitHub Pages。
- `AGENTS.md`：定时任务和 AI 的完整操作流程。

正文支持 HTTP(S) Markdown 链接，链接文字可以是提交哈希、仓库名加哈希或中文说明，例如 `[项目说明](https://example.com/docs)`。反引号内的链接示例保持为代码。测试会逐篇检查历史日报中的显式链接确实渲染为可点击链接，而不只是检查 URL 字符串存在。

## 定时任务

调度在本地 Codex 中管理，名称为「MM Trading Bot 每日变动日志」，每天 20:00（Asia/Shanghai）。本机需要开机、Codex 可执行任务，并能访问 GitHub；它不是服务器常驻任务。任务运行时会读取本仓库的最新说明。修改脚本不改变调度时间，改时间需要更新 Codex 自动化。

只允许写入和推送日志仓库；不运行交易、不连接生产数据库、不修改或部署来源项目。公开内容不包含钱包密钥、助记词、密码、RPC 凭据或用户数据。
