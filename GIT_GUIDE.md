# Quick Git Commands Reference

## Initial Setup (First Time Only)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Dream Journal Emotion Tracker v1.0.0"

# Create main branch (if needed)
git branch -M main

# Add remote repository (replace with your GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/dream-journal.git

# Push to GitHub
git push -u origin main
```

## Regular Workflow

```bash
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push

# Pull latest changes
git pull
```

## Creating a New Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `dream-journal` (or your preferred name)
3. Description: "AI-powered dream journal with emotion tracking and NLP analysis"
4. Choose Public or Private
5. **Do NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"
7. Follow the commands shown (or use the ones above)

## Useful Commands

```bash
# View commit history
git log --oneline

# Create and switch to new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature

# Tag a release
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

## .gitignore Already Set Up

The following are automatically ignored:
- Virtual environment (`venv/`)
- Python cache files (`__pycache__/`)
- Database files (`*.db`)
- IDE files (`.vscode/`, `.idea/`)
- Environment files (`.env`)

## First Push Checklist

- [ ] Git initialized
- [ ] All files added
- [ ] First commit created
- [ ] Remote repository created on GitHub
- [ ] Remote added to local repository
- [ ] Pushed to GitHub
- [ ] Verify files on GitHub

## Troubleshooting

**Problem**: `fatal: remote origin already exists`
```bash
git remote remove origin
git remote add origin YOUR_GITHUB_URL
```

**Problem**: Need to change commit message
```bash
git commit --amend -m "New message"
```

**Problem**: Accidentally committed database file
```bash
git rm --cached dream_journal.db
git commit -m "Remove database from tracking"
```
