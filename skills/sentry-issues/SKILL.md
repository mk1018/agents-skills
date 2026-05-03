---
name: sentry-issues
description: Sentry CLIでプロジェクトのエラー情報を取得・分析する
---


# Sentry Issues

Sentry CLIでプロジェクトのエラー情報を取得・分析する。

## 実行方法

1. `projects.md` を読んで対象のorg・projectを確認する
   - `projects.md` が存在しない場合は以下のセットアップを実行：
     1. `sentry-cli organizations list` でorg一覧を取得
     2. `sentry-cli projects list --org {org}` でproject一覧を取得
     3. ユーザーに対象のorg・projectを確認
     4. 確認した内容を `projects.md` に保存（スキルディレクトリ内に作成）
2. `sentry-cli issues list --org {org} --project {project}` で未解決のissue一覧を取得
3. 特定のissueの詳細を確認する場合は `sentry-cli issues show <issue-id> --org {org}` を実行

## Notes

- 認証は `sentry-cli login` で事前に設定済み
- issueのステータス: `unresolved`, `resolved`, `ignored`
- unresolvedのissueを優先的に確認する
- 複数orgがある場合は `sentry-cli organizations list` で確認可能
- プロジェクト一覧は `sentry-cli projects list --org {org}` で確認可能
