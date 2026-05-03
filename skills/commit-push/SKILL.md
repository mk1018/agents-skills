---
name: commit-push
description: 新しいブランチを作成し、変更をコミットしてプッシュし、PRを作成する
---

# Commit and Push

新しいブランチを作成し、変更をコミットしてプッシュし、PRを作成します。

## 手順

1. **ブランチの作成**
   - 現在のブランチ状況を確認
   - 新しいブランチを作成するか、既存のブランチを使用するかをユーザーに確認
   - ユーザーに新しいブランチ名を確認（提案する場合は feature/xxx, fix/xxx, docs/xxx などのプレフィックスを使用）
   - ベースブランチを特定し、そこから新しいブランチを作成（必要に応じてベースブランチを最新化）
     - `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` でデフォルトブランチを確認
     - ユーザーからマージ先ブランチの指示がある場合は、それをベースブランチとして使用

2. **ブランチの確認（必須）**
   - `git branch --show-current` で現在のブランチを確認する
   - **ベースブランチ（main, master, develop, staging など）にいる場合は絶対にコミット・プッシュしない**。必ず新しいブランチを作成してから作業すること
   - 作業ブランチにいることを確認してから次のステップに進む

3. **変更のコミット**
   - git status で変更内容を確認
   - git diff で差分を確認
   - 明確な指示がない限り変更されているファイルはすべて含める。 `git add .` を使用
   - 変更内容に応じた適切なコミットメッセージを作成
   - 変更をステージングしてコミット
   - コミットメッセージには以下を含める：
     - Conventional Commits形式のプレフィックスを必ず付ける：
       - `feat:` 新機能
       - `fix:` バグ修正
       - `docs:` ドキュメントのみの変更
       - `chore:` ビルドやツール、設定の変更
       - `refactor:` リファクタリング
       - `test:` テストの追加・修正
       - `style:` コードスタイルの変更（動作に影響しない）
     - プレフィックスに続けて簡潔な変更内容の要約
     - フッターに以下を追加：

       ```text
       🤖 Generated with [Claude Code](https://claude.com/claude-code)

       Co-Authored-By: Claude <noreply@anthropic.com>
       ```

4. **リモートへのプッシュ**
   - `git push -u origin {branch-name}` でリモートにプッシュ
   - プッシュ後の状態を確認

5. **PRの作成**
   - `gh pr create --assignee @me` でPRを作成し、操作しているユーザーを担当者にアサイン
   - PRのタイトルはコミットメッセージの要約を使用
   - PRの本文には以下を含める：
     - `## Summary` - 変更内容の要約（1-3行）
     - `## Related Issues` - 関連するGitHub issueがある場合、紐づけを記載する
       - 変更がissueを完了させる場合: `Closes #123`
       - 部分的に関連する場合: `Related to #123`
       - 複数issueがある場合は改行で列挙する
       - `gh issue list` や変更内容から関連issueを特定する
     - `## Test plan` - テスト方法のチェックリスト
     - フッターに以下を追加：

       ```text
       🤖 Generated with [Claude Code](https://claude.com/claude-code)
       ```

   - ベースブランチは手順1で特定したブランチを指定（`--base <branch>`）
   - 作成後、PRのURLをユーザーに表示

6. **レビューコメントの追加**
   - レビュアーに説明が必要な変更箇所がある場合、該当行にコメントを追加する
   - 以下のコマンドで特定の行にコメントを追加：

     ```bash
     gh api repos/{owner}/{repo}/pulls/{PR番号}/comments \
       -f body="コメント内容" \
       -f path="ファイルパス" \
       -F position=diff内の行位置 \
       -f commit_id="$(git rev-parse HEAD)"
     ```

## 注意事項

- ブランチ名は機能や修正内容がわかるように命名する
- コミット前に必ず変更内容を確認する
- .env や credentials.json などの機密情報をコミットしないよう注意する
- ベースブランチはリポジトリのデフォルトブランチまたはユーザー指定のブランチを使用する
- ベースブランチに直接プッシュしない
