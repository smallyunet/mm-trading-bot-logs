# Daily changelog agent workflow

The user authorized a daily public MM Trading Bot changelog and automatic commit/push to `smallyunet/mm-trading-bot-logs`. Keep all source repositories read-only. Write only this logs repository. Do not run wallet generation, trading, production database operations, application deployment, or messages to other services.

1. Read README.md and data/config.json. Work in this repository, with its parent as the source workspace. Verify GitHub identity and origin target before pushing. Never expose credentials or key material.
2. Inspect this repository's Git status. Preserve unrelated changes. If clean, fetch origin and fast-forward only. If there is a prior incomplete publication, recover its existing commit/push/Pages run before assuming any receipt is published. Never reset, force-push, or discard content.
3. Run `python3 scripts/collect.py > pending.json`. It scans immediate child Git repositories, including newly added children, excluding this repo. It reads non-merge commits reachable from each current HEAD, exact `%an == smallyunet`, with committer timestamps since the configured bootstrap date. Receipt membership prevents duplicates; there is no moving timestamp cutoff that could skip late-arriving commits. Failures must be reported, not silently skipped.
4. Read every candidate's actual `git show` diff, using file stats only to choose safe, relevant paths. Do not read secrets, wallet output, `.env`, or private data. Confirm canonical GitHub repository URLs. Organize the report by the business lines below, merging frontend, backend and chain-adapter changes into each business outcome. Do not organize by repository, commit order or technical layer. Cite full commit URLs with 7–8 character labels. Do not infer shipped behavior or tests from commit titles. If a commit is local only, explicitly label it and do not claim it is pushed or deployed.
5. Use the actual Asia/Shanghai run date for `logs/YYYY-MM-DD.md`, with actual update time and coverage information. For catch-up runs, explain the covered interval. For same-date reruns, merge new information into the existing report and preserve prior entries. If no candidates, say there are no new eligible commits. If candidates have only mechanical changes, say no user-facing changes and describe that briefly; still record their IDs.
6. Merge all reviewed candidate `{repository, sha}` records into that date's `data/receipts/YYYY-MM-DD.json` under `commits`, without duplicates. Keep previous records. Receipts represent report inclusion, NOT successful deployment. Do not store secrets, machine paths or email addresses in public metadata. Never advance collection config.start to skip failures.
7. Run `git diff --check`, `python3 -m unittest discover -s tests -v`, and `python3 scripts/build.py --check`. Inspect the generated homepage, dated page and source links. Commit only intended log-repo files. Push main without force; if remote advanced, preserve both sets of logs using a normal merge or rebase only when safe.
8. Verify the exact pushed SHA via remote readback, the GitHub Pages workflow for that SHA, and an HTTP read of the live dated page with expected content. Push success is not Pages success. On failure, retain work and report the failed stage; next run must repair publication before proceeding. Record successful publication SHA, workflow, URL and time in the task's final response. Do not claim a future scheduled execution has happened.

Commands for site validation are in README.md. Scheduling is managed by Codex, not OS cron or GitHub Actions; the workflow only publishes after a push. Runtime changes to the schedule should use the existing automation, avoiding duplicate tasks.

## Business-line report structure

Use `##` headings in this stable order, including only lines with relevant changes:

1. 钱包工具与批量创建：生成、恢复、导入导出、钱包组和钱包管理。
2. Wallet Warmup：钱包预热配置、执行和结果。
3. Snipe：开池监听、快速买入、执行追踪和结果。
4. Trading Strategy：区间、网格、动量等策略配置、执行和绩效。
5. Market Intelligence：行情、池子、地址分析、持仓分布和成本统计。
6. 资金流转：跨链入金、CEX 提币、转账、归集和清仓等独立资金操作。
7. 平台与基础设施：确实跨业务的项目权限、网络配置、公共界面和构建发布改动。

These are extensible business lines, not mandatory daily slots. Add a new business line only when actual changes justify it. Summarize each active line in a short paragraph or a few outcome-based items: what users can do or observe, what changed, and material limitations. Keep feature-specific UI, reliability and infrastructure fixes with their business line. Describe shared changes once, with cross-references only when useful. Never repeat the same change to fill multiple sections, impose a fixed item count, or add empty sections. Keep the collection window and publication status outside the business sections. Apply this structure to future reports; do not rewrite historical reports unless asked.
