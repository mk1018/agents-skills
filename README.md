# Claude Code Skills

Claude Code で使用する個人的なカスタムスキル集です。

## スキル一覧

| スキル | Claude Code コマンド | 説明 |
| -------- | ---------- | ------ |
| [commit-push](skills/commit-push/SKILL.md) | `/commit-push` | 新しいブランチを作成し、変更をコミットしてプッシュし、PRを作成する |
| [review-and-push](skills/review-and-push/SKILL.md) | `/review-and-push` | 別エージェントでレビューし、問題なければcommit-pushする |
| [codex-review](skills/codex-review/SKILL.md) | `/codex-review` | Codex CLIで現在の変更をレビューし、指摘事項があれば修正する |
| [claude-code-review](skills/claude-code-review/SKILL.md) | `/claude-code-review` | Claude Codeのultrareviewで現在の変更をレビューし、指摘事項があれば修正する |
| [create-issues](skills/create-issues/SKILL.md) | `/create-issues` | 指示されたタスクからGitHub Issuesを作成する |
| [sentry-issues](skills/sentry-issues/SKILL.md) | `/sentry-issues` | Sentry CLIでプロジェクトのエラー情報を取得・分析する |

## 他のリポジトリでの使い方

### インストール

使いたいリポジトリで以下を実行します。

```bash
# すべてのスキルをインストール
npx skills add mk1018/claude-code-skills

# 特定のスキルのみインストール
npx skills add mk1018/claude-code-skills --skill commit-push

# グローバルにインストール（全リポジトリで使用可能）
npx skills add mk1018/claude-code-skills -g
```

### スキルの呼び出し

Claude Code では、チャットで `/` から始まるコマンドを入力して実行します。

```text
/commit-push
/review-and-push
/codex-review
/claude-code-review
/create-issues
/sentry-issues
```

Codex では、メッセージ内で `$` 付きのスキル名、またはスキル名そのものを指定します。`/` は Codex のスキル呼び出しとしては扱われません。

```text
$commit-push を使ってPRを作成して
codex-review で現在の変更をレビューして
```
