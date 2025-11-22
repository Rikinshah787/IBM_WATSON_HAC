# Version Management Guide

## Overview

OrchestrateIQ uses [Semantic Versioning](https://semver.org/) (SemVer) for version management.

**Format:** `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

- **MAJOR**: Breaking changes that are not backward compatible
- **MINOR**: New features that are backward compatible
- **PATCH**: Bug fixes and minor improvements

## Current Version

The current version is tracked in multiple places:
- `package.json` (root)
- `frontend/package.json`
- `VERSION` file
- `docs/meta/CHANGELOG.md`

## How to Update Version

### Quick Commands

```bash
# For bug fixes (1.0.0 → 1.0.1)
npm run version:patch

# For new features (1.0.0 → 1.1.0)
npm run version:minor

# For breaking changes (1.0.0 → 2.0.0)
npm run version:major

# To check current version
npm run version:show
```

### What These Commands Do

When you run a version command, it automatically:
1. ✅ Updates `package.json` version
2. ✅ Updates `frontend/package.json` version
3. ✅ Updates `VERSION` file
4. ✅ Adds entry to `CHANGELOG.md`

### Complete Workflow

1. **Make your changes** to the codebase

2. **Update the version** based on the type of change:
   ```bash
   npm run version:patch  # or minor/major
   ```

3. **Update CHANGELOG.md** with details of your changes:
   - Open `CHANGELOG.md`
   - Find the newly created version section
   - Replace `[Add your changes here]` with actual changes
   - Categorize under: Added, Changed, Fixed, Removed, Security

4. **Commit all changes** including version updates:
   ```bash
   git add .
   git commit -m "chore: bump version to X.Y.Z"
   ```

5. **Create a git tag** (optional but recommended):
   ```bash
   git tag v1.1.0
   ```

6. **Push to remote** with tags:
   ```bash
   git push origin main
   git push origin --tags
   ```

## Version Update Checklist

Before pushing code, ensure:

- [ ] Version number has been updated appropriately
- [ ] `CHANGELOG.md` has been updated with changes
- [ ] All version files are in sync (package.json, VERSION)
- [ ] Changes are committed
- [ ] Git tag created (if applicable)
- [ ] Tests pass (if applicable)

## Pre-commit Hook

A pre-commit hook (`scripts/check-version.js`) will remind you to update the version when you commit code changes. This is a reminder, not a blocker.

## Examples

### Example 1: Bug Fix

```bash
# Fix a bug in the code
# ... make changes ...

# Update version
npm run version:patch

# Update CHANGELOG.md manually
# Add: "- Fixed authentication timeout issue"

# Commit
git add .
git commit -m "fix: resolve authentication timeout issue"

# Tag and push
git tag v1.0.1
git push origin main --tags
```

### Example 2: New Feature

```bash
# Add a new feature
# ... make changes ...

# Update version
npm run version:minor

# Update CHANGELOG.md manually
# Add: "- Added export to PDF functionality"

# Commit
git add .
git commit -m "feat: add PDF export functionality"

# Tag and push
git tag v1.1.0
git push origin main --tags
```

### Example 3: Breaking Change

```bash
# Make breaking changes
# ... make changes ...

# Update version
npm run version:major

# Update CHANGELOG.md manually
# Add: "- BREAKING: Changed API response format"

# Commit
git add .
git commit -m "feat!: redesign API response structure"

# Tag and push
git tag v2.0.0
git push origin main --tags
```

## Conventional Commits

We recommend using [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

- `feat:` - New feature (minor version)
- `fix:` - Bug fix (patch version)
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `feat!:` or `fix!:` - Breaking changes (major version)

## Troubleshooting

### Versions are out of sync

Run the update script manually:
```bash
node scripts/update-version.js
```

### Need to see current version

```bash
npm run version:show
```

### Made a mistake with version

1. Manually edit `package.json` to correct version
2. Run: `node scripts/update-version.js`
3. Commit the fixes

## Best Practices

1. **Always update version before pushing** to main/production
2. **Update CHANGELOG.md** with meaningful descriptions
3. **Use semantic versioning correctly**:
   - Patch: Bug fixes, typos, minor improvements
   - Minor: New features, non-breaking changes
   - Major: Breaking changes, API redesigns
4. **Tag releases** for easy rollback and tracking
5. **Keep CHANGELOG.md up to date** - it's your project's history
6. **Review changes** before committing version updates

## Integration with CI/CD

The version number can be used in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Get version
  run: echo "VERSION=$(cat VERSION)" >> $GITHUB_ENV

- name: Build with version
  run: npm run build
  env:
    REACT_APP_VERSION: ${{ env.VERSION }}
```

## Questions?

- Check the current version: `npm run version:show`
- Review version history: Check `CHANGELOG.md`
- See git tags: `git tag -l`
