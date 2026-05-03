---
name: review-and-push
description: 別エージェントでレビューし、問題なければcommit-pushする
---

# Review and Push

現在操作しているエージェントとは別のエージェントでレビューし、問題なければcommit-pushする。

## Steps

1. 現在操作しているエージェントを確認
2. 別エージェントのレビュースキルを実行:
   - Claude Codeで操作中 → `/codex-review`
   - Codexで操作中 → `/claude-code-review`
   - 判断できない場合 → ユーザーにどちらで操作中か確認
3. レビュー結果を確認:
   - 指摘あり → 修正してから同じレビュースキルを再度実行（指摘が解消されるまで繰り返す）
   - 指摘なし or 対応不要 → 次のステップへ
4. 未コミットの変更がある場合のみ `/commit-push` スキルを実行
