# Release Process for Maintainers

This document provides comprehensive guidance for maintainers on the OpenTDF Python SDK release process, including both automated releases and feature branch testing.

## Release Overview

The OpenTDF Python SDK uses **Release Please** for automated version management and publishing. The system supports:

- **Alpha releases** (e.g., `0.3.0a7`): Automated publishing to both test.pypi.org and pypi.org
- **Stable releases** (e.g., `0.3.0`): Automated publishing to pypi.org only
- **Feature branch testing**: Manual alpha releases from development branches

## Current Version Status

```bash
# Check current version
uv version --short

# Preview next alpha version
uv version --bump alpha --dry-run

# Preview next stable version  
uv version --bump minor --dry-run  # or patch/major
```

## Automated Release Process (Main Branch)

### Prerequisites

✅ **All tests must pass** before any release:
- Unit tests: `uv run pytest tests/`
- Integration tests: `uv run pytest tests/ -m integration`
- Linting: `uv run ruff check` and `uv run ruff format`
- Platform integration tests (via GitHub Actions)

### Standard Release Flow

1. **Commit with Conventional Commit Messages** to `main` branch:
   ```bash
   git commit -m "feat: add new encryption algorithm support"
   git commit -m "fix: resolve TDF decryption issue with large files"
   git commit -m "docs: update SDK configuration examples"
   ```

2. **Push to Main**:
   ```bash
   git push origin main
   ```

3. **Automated Process**:
   - Release Please creates a PR with version bump and changelog
   - Once PR is merged, GitHub Actions automatically:
     - Runs full test suite (unit, integration, platform tests)
     - Builds wheels for multiple platforms (macOS, Linux x86_64, Linux ARM)
     - Publishes to PyPI (alpha versions go to both test.pypi.org and pypi.org)
     - Creates GitHub release with artifacts

### Release Type Determination

The system automatically determines release type based on version format:

- **Alpha**: `X.Y.ZaN` (e.g., `0.3.0a7`) → Published to test.pypi.org + pypi.org
- **Stable**: `X.Y.Z` (e.g., `0.3.0`) → Published to pypi.org only

## Manual Release Management

### Bootstrap Release Please (First Time Setup)

If this is the first time setting up Release Please:

```bash
# Bootstrap Release Please for the repository
npx release-please bootstrap \
  --repo-url=b-long/opentdf-python-sdk \
  --release-type=python

# This creates the initial configuration files and release PR
```

### Preview Release Changes

```bash
# See what Release Please would create (after bootstrap)
npx release-please release-pr \
  --repo-url=b-long/opentdf-python-sdk \
  --config-file=.release-please-config.json \
  --manifest-file=.release-please-manifest.json
```

### Manual Release Creation

```bash
# Manually trigger GitHub release (if needed)
npx release-please github-release \
  --repo-url=b-long/opentdf-python-sdk \
  --config-file=.release-please-config.json \
  --manifest-file=.release-please-manifest.json
```

### Workflow Dispatch

You can manually trigger releases via GitHub Actions:
- Go to Actions → "Release Please" → "Run workflow"
- Or Actions → "PyPIBuild" → "Run workflow"

## Feature Branch Alpha Releases (For Testing)

### When to Use Feature Branch Releases

Use this approach when you need to test changes before merging to main:
- Testing breaking changes with external users
- Validating integration with downstream systems
- Providing preview releases for feedback

### Process for Feature Branch Releases

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-encryption-method
   # Make your changes
   git commit -m "feat: implement new encryption method"
   ```

2. **Manually Bump Version** (create unique alpha version):
   ```bash
   # Option A: Use uv to bump version in pyproject.toml
   uv version --bump alpha
   
   # Option B: Edit pyproject.toml directly to create unique alpha
   # If current is 0.3.0a7, you might use 0.3.0a7.dev1 or 0.3.1a1
   ```

3. **Update Version Files**:
   ```bash
   # Update any version references in extra files
   # (Release Please normally handles this)
   sed -i 's/0.3.0a7/0.3.0a7.dev1/g' src/otdf_python/cli.py
   ```

4. **Commit Version Changes**:
   ```bash
   git add .
   git commit -m "chore: bump version for feature testing to 0.3.0a7.dev1"
   ```

5. **Push Feature Branch**:
   ```bash
   git push origin feature/new-encryption-method
   ```

6. **Manual Build and Publish**:
   
   **Option A: GitHub Actions (Recommended)**
   - Push to a temporary branch that matches main branch patterns
   - Or trigger workflow dispatch with your branch
   
   **Option B: Local Build** (for internal testing):
   ```bash
   # Build wheel locally
   uv build
   
   # Install for testing
   pip install dist/otdf_python-0.3.0a7.dev1-*.whl
   
   # Or upload to test.pypi.org manually
   uv publish --repository testpypi dist/*
   ```

### Feature Branch Naming Convention

For feature branches that need releases, use clear naming:
- `feature/new-encryption-method`
- `experimental/performance-improvements`
- `preview/api-v2`

### Cleanup After Feature Branch Testing

```bash
# After merging feature to main, clean up
git branch -d feature/new-encryption-method
git push origin --delete feature/new-encryption-method

# The main branch release will supersede the feature branch alpha
```

## Version Numbering Strategy

### Alpha Versions
- **Sequential alphas**: `0.3.0a1`, `0.3.0a2`, `0.3.0a3`...
- **Feature branch alphas**: `0.3.0a7.dev1`, `0.3.1a1.dev1`
- **Experimental**: `0.4.0a1.experimental`

### Stable Versions
- **Patch releases**: `0.3.0` → `0.3.1` (bug fixes)
- **Minor releases**: `0.3.0` → `0.4.0` (new features)
- **Major releases**: `0.3.0` → `1.0.0` (breaking changes)

## Testing Release Candidates

### Before Publishing
```bash
# Run full test suite
uv run pytest tests/ -v

# Run integration tests
uv run pytest tests/ -m integration -v

# Check code quality
uv run ruff check
uv run ruff format --check

# Type checking (if configured)
uvx ty check src/
```

### After Publishing
```bash
# Test installation from PyPI
pip install otdf-python==0.3.0a7

# Test basic functionality
python -c "import otdf_python; print('Import successful')"

# Run smoke tests
uv run pytest tests/test_sdk.py::test_basic_functionality
```

## Troubleshooting Releases

### Failed Test Suite
```bash
# Check what failed
uv run pytest tests/ -v --tb=short

# Fix issues and re-run
uv run pytest tests/ -v
```

### Failed Build
- Check GitHub Actions logs
- Verify all platforms build successfully
- Ensure version format is correct

### Failed PyPI Upload
- Verify PyPI trusted publisher setup
- Check for version conflicts
- Ensure all required metadata is present

### Version Conflicts
```bash
# If version already exists on PyPI
uv version --bump patch  # increment to next available version
```

## Multi-Package Releases

This repository manages two packages:
- `otdf-python` (main SDK)
- `otdf-python-proto` (protobuf submodule)

Both packages should maintain version sync. Release Please handles this automatically for main branch releases.

## Security Considerations

- Never commit API keys or credentials
- Trusted publishing prevents credential management
- All releases require passing security tests
- Alpha releases are publicly available on PyPI

## Rollback Procedures

### Yanking a Bad Release
```bash
# Yank from PyPI (makes it unavailable for new installs)
uv publish --yank "0.3.0a7" --reason "Critical security issue"

# Create hotfix release
git checkout main
# Make fixes
git commit -m "fix: critical security issue"
# Follow normal release process
```

### Emergency Hotfix
```bash
# Create hotfix branch from last good release
git checkout v0.3.0
git checkout -b hotfix/security-fix

# Make minimal fix
git commit -m "fix: security vulnerability"

# Merge back to main and release
git checkout main
git merge hotfix/security-fix
# Follow normal release process
```

## Release Checklist for Maintainers

### Pre-Release
- [ ] All tests passing locally
- [ ] Integration tests passing
- [ ] Documentation updated
- [ ] CHANGELOG reviewed
- [ ] Version bump appropriate
- [ ] No security issues

### During Release
- [ ] GitHub Actions tests pass
- [ ] Build artifacts created successfully
- [ ] PyPI upload successful
- [ ] GitHub release created

### Post-Release
- [ ] Test installation from PyPI
- [ ] Verify SDK functionality
- [ ] Update any dependent projects
- [ ] Communicate release to users
- [ ] Monitor for issues

## Support and Escalation

For release issues:
1. Check GitHub Actions logs
2. Review PyPI trusted publisher setup
3. Verify release-please configuration
4. Contact repository maintainers
5. Create GitHub issue for persistent problems