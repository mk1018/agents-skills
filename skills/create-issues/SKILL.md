---
name: create-issues
description: 指示されたタスクからGitHub Issuesを作成する
---

# Create Issues

Create GitHub Issues from instructed tasks.

## Steps

1. **Identify Repository**
   - Detect the repository from the current working directory using `gh repo view --json nameWithOwner -q .nameWithOwner`
   - If not in a git repository, ask the user to specify `owner/repo`

2. **Confirm Tasks**
   - Confirm task content instructed by user
   - If there are multiple tasks, create separate Issues for each

3. **Create Issue**
   - Create Issue with the following command:

     ```bash
     gh issue create --repo <owner/repo> --title "Title" --body "Description"
     ```

   - Issue body should include:
     - Task overview
     - Detailed description or acceptance criteria as needed
     - If specific code lines are mentioned, include a link to the code:
       - Format: `https://github.com/<owner/repo>/blob/{commit-hash}/{file-path}#L{start}-L{end}`

   - **GitHub Project linking**:
     - If the user specifies a GitHub Project, link the issue after creation
     - If the user does not specify a project, list available projects using:

       ```bash
       gh project list --owner <owner> --format json
       ```

       and ask the user which project to link (or whether to skip linking)
     - Command: `gh project item-add <project-number> --owner <owner> --url <issue-url>`

4. **Completion Report**
   - Display list of created Issue URLs

## Notes

- Name titles to be concise and clearly indicate the content
- Check if similar Issues already exist
- Use `--label` or `--assignee` options if labels or assignments are needed
- **Write Issue titles and content in Japanese**
