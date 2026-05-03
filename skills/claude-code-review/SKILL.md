---
name: claude-code-review
description: Claude Codeのultrareviewで現在の変更をレビューし、指摘事項があれば修正する
---

# Claude Code Review

Claude Codeの`ultrareview`で現在の変更をレビューし、指摘事項があれば修正する。

## 実行方法

1. `git status` と `git branch` で現在の状態を確認
2. 状況に応じて `claude ultrareview` を実行:
   - 未コミットの変更がある → 先に差分を確認し、レビュー対象をユーザーに確認してから実行
   - PRブランチにいる → `claude ultrareview <base-branch>`
   - PR番号またはPR URLを指定された → `claude ultrareview <PR番号またはPR URL>`
   - 特に指定がない場合 → `claude ultrareview`
3. Claude Codeのレビュー結果を確認
4. 指摘事項がある場合は修正を実施
5. 修正後、再度 `claude ultrareview` を実行して指摘が解消されたことを確認
6. 結果をユーザーに報告

## Notes

- `claude ultrareview --timeout <minutes>` で待機時間を調整できる
- `--json` は機械的に結果を確認したい場合のみ使用する
- 指摘内容が的外れな場合は無視してよい
- 修正が不要な場合は「指摘なし」または「対応不要」とユーザーに報告
