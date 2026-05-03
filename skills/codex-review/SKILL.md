---
name: codex-review
description: Codex CLIで現在の変更をレビューし、指摘事項があればClaude Codeが修正する
---

# Codex Review

Codex CLIで現在の変更をレビューし、指摘事項があればClaude Codeが修正する。

## 実行方法

1. `git status` と `git branch` で現在の状態を確認
2. 状況に応じて `codex review` を実行:
   - 未コミットの変更がある → `codex review --uncommitted`
   - PRブランチにいる（未コミット変更なし） → `codex review --base staging`
   - 特定コミットを指定された → `codex review --commit <SHA>`
3. Codexのレビュー結果を確認
4. 指摘事項がある場合はClaude Codeが修正を実施
5. 修正後、再度 `codex review` を実行して指摘が解消されたことを確認
6. 結果をユーザーに報告

## Notes

- 指摘内容が的外れな場合は無視してよい
- 修正が不要な場合は「指摘なし」または「対応不要」とユーザーに報告
