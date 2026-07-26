# Release Process for OpenTDF Python SDK

This document describes the automated release process for the OpenTDF Python SDK using Release Please and GitHub Actions.

## Overview

The OpenTDF Python SDK publishes stable releases from the `main` branch:

- **`main` branch**: Creates stable releases (e.g., `v1.0.0`) → Published to PyPI

There is currently no `develop` branch and no alpha/prerelease channel. All releases are stable releases published to PyPI.

## Automated Release Process

### Prerequisites

✅ **All tests must pass** before any release:
- Unit tests via GitHub Actions test suite
- Integration tests
- Code quality checks (linting, formatting)

### Creating a Stable Release

1. **Commit with Conventional Commit Messages** to `main`:
   ```bash
   git checkout main
   git commit -m "feat: add new encryption algorithm support"
   git commit -m "fix: resolve TDF decryption issue with large files"
   git push origin main
   ```

2. **Automated Process**:
   - Release Please creates a PR with a version bump and changelog
   - Once the PR is merged, GitHub Actions automatically:
     - Runs the full test suite
     - Builds the package
     - Creates a GitHub release
     - Publishes to PyPI

## Version Numbering

Release Please uses `.release-please-manifest.json` to track the last released version. When it runs, it:
1. Reads the manifest to find the last released version
2. Analyzes conventional commits since that version
3. Calculates the next version based on commit types (`feat`, `fix`, etc.)

Stable versions follow semantic versioning (e.g., `v0.10.0`, `v0.10.1`) and are published to PyPI (pypi.org).

## Manual Release Triggers

You can manually trigger a release via GitHub Actions:
- Go to **Actions** → **"Release Please"** → **"Run workflow"**

## Conventional Commit Messages

Release Please determines version bumps based on commit message types:

- `feat:` → Minor version bump (new features)
- `fix:` → Patch version bump (bug fixes)
- `BREAKING CHANGE:` → Major version bump (breaking changes)
- `docs:`, `chore:`, `style:` → No version bump

Examples:
```bash
git commit -m "feat: add support for new TDF format"          # Minor bump
git commit -m "fix: resolve memory leak in encryption"       # Patch bump
git commit -m "feat!: redesign SDK API (BREAKING CHANGE)"    # Major bump
```

## Testing a Release

```bash
# Install from PyPI
pip install otdf-python==0.10.0

# Test functionality
python -c "import otdf_python; print('Release works!')"
```

## Multi-Package Releases

This repository manages two packages:
- `otdf-python` (main SDK)
- `otdf-python-proto` (protobuf submodule)

Release Please automatically updates version references in both packages using the `extra-files` configuration.

## Troubleshooting

### No Release Created
- Verify commits use conventional commit format
- Check that tests pass in GitHub Actions
- Ensure commits were pushed to `main`

### Failed Publishing
- Check GitHub Actions logs for detailed error messages
- Verify PyPI trusted publisher configuration
- Ensure the version doesn't already exist on PyPI

## Emergency Procedures

### Hotfix for Stable Release
```bash
# Create hotfix directly on main
git checkout main
git commit -m "fix: critical security vulnerability"
git push origin main
# Release Please will create a patch release
```

## Configuration Files

- `.release-please-config.json`: Release configuration
- `.release-please-manifest.json`: Version tracking
- `.github/workflows/release-please.yaml`: GitHub Actions workflow

## Support

For release issues:
1. Check GitHub Actions logs in the "Release Please" workflow
2. Review the Release Please documentation
3. Create a GitHub issue with workflow logs
4. Contact repository maintainers
