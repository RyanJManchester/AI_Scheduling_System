### contributing

cloning the repository to your local machine:

```bash
git clone https://github.com/yourusername/repo-name.git
cd repo-name
```

#### 2. Create a New Branch

Before making any changes, create a new branch to isolate your work. Use a descriptive branch name:

```bash
git checkout -b name/your-feature-name
```


#### 3. Pull the Latest Changes from `main`

Always ensure your branch is up-to-date with the `main` branch to avoid conflicts:

```bash
git fetch origin
git checkout main
git pull origin main
```

#### 4. Rebase Your Branch

If your branch is behind `main`, rebase it before starting work to maintain a clean commit history:

```bash
git checkout feature/your-feature-name
git rebase main
```

> **Note**: Resolve any conflicts during the rebase, then continue:

```bash
git rebase --continue
```

#### 5. Make Your Changes

Now, you can start working on your feature or bug fix.

#### 6. Add and Commit Your Changes

commit  example:

```bash
git commit -m "docs(README): update setup instructions"
```

### 7. Rebase Again Before Pushing

If other team members have pushed changes to `main` while you were working, rebase your branch onto `main` again:

```bash
git fetch origin
git checkout main
git pull origin main
git checkout name/your-feature-name
git rebase main
```
This helps avoid merge conflicts later.

### 8. Push Your Changes to the Remote Repository

Once you're ready, push your BRANCH:
```bash
git push origin name/your-feature-name
```

#### 9. Open a Pull Request

Go to the repository on GitHub/GitLab and open a pull request (PR) to the `main` branch. Ensure your PR includes:

- A description of the changes.
- Relevant documentation updates.

#### 10. Code Review

Wait for a code review. If changes are requested:

- use the feedback in your local branch.
- Commit the changes.
- Push the branch again using the same `git push` command.

#### 11. Merging the Pull Request

After approval, merge your PR into the `main` branch. If you need to merge it locally:

1. Switch to `main`:

```bash
git checkout main
```

2. Pull the latest changes from `main`:

```bash
git pull origin main
```

3. Merge your feature branch into `main`:

```bash
git merge feature/your-feature-name
```

4. Push the updated `main` branch:

```bash
git push origin main
```

#### 12. Delete the Feature Branch

After merging, it’s good practice to delete your feature branch:

```bash
git branch -d feature/your-feature-name
git push origin --delete feature/your-feature-name
```