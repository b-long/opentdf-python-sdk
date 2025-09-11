# Release Process for OpenTDF Python SDK

This document describes the automated release process for the OpenTDF Python SDK using Release Please and GitHub Actions.

## Overview

The OpenTDF Python SDK uses a **dual-branch release strategy** with automated publishing:

- **`develop` branch**: Creates alpha prereleases (e.g., `v1.0.0-alpha.1`) → Published to TestPyPI
- **`main` branch**: Creates stable releases (e.g., `v1.0.0`) → Published to PyPI

This ensures that alpha and stable releases have distinct version numbers and publishing destinations, preventing conflicts between development and production releases.

## Branch Strategy

### Develop Branch (Alpha Releases)
- **Purpose**: Development and testing
- **Release Type**: Alpha prereleases (`v1.0.0-alpha.1`, `v1.0.0-alpha.2`, etc.)
- **GitHub Status**: Marked as "pre-release"
- **Publishing Target**: TestPyPI (test.pypi.org)
- **Trigger**: Push to `develop` branch with conventional commits

### Main Branch (Stable Releases)
- **Purpose**: Production releases
- **Release Type**: Stable releases (`v1.0.0`, `v1.0.1`, etc.)
- **GitHub Status**: Marked as stable release
- **Publishing Target**: PyPI (pypi.org)
- **Trigger**: Push to `main` branch with conventional commits

## Automated Release Process

### Prerequisites

✅ **All tests must pass** before any release:
- Unit tests via GitHub Actions test suite
- Integration tests
- Code quality checks (linting, formatting)

### For Alpha Releases (Develop Branch)

1. **Commit with Conventional Commit Messages** to `develop` branch:
   ```bash
   git checkout develop
   git commit -m "feat: add new encryption algorithm support"
   git commit -m "fix: resolve TDF decryption issue with large files"
   git push origin develop
   ```

2. **Automated Process**:
   - Release Please creates a PR with alpha version bump and changelog
   - Once PR is merged, GitHub Actions automatically:
     - Runs full test suite
     - Builds the package
     - Creates GitHub release marked as "pre-release"
     - Publishes to TestPyPI (if version > 0.3.2)

**Note**: The develop branch uses separate configuration files (`.release-please-config-develop.json` and `.release-please-manifest-develop.json`) to ensure proper alpha version tracking independent of the main branch.

### For Stable Releases (Main Branch)

1. **Merge from develop** (or commit directly):
   ```bash
   git checkout main
   git merge develop
   # OR make direct commits with conventional commit messages
   git commit -m "feat: stable feature ready for production"
   git push origin main
   ```

2. **Automated Process**:
   - Release Please creates a PR with stable version bump and changelog
   - Once PR is merged, GitHub Actions automatically:
     - Runs full test suite
     - Builds the package
     - Creates GitHub release marked as stable
     - Publishes to PyPI

## Version Numbering

### How Version Tracking Works

Release Please uses manifest files to track the "last released version" for each branch:

- **`.release-please-manifest.json`**: Tracks the last stable release from main branch
- **`.release-please-manifest-develop.json`**: Tracks the last alpha release from develop branch

When Release Please runs, it:
1. Reads the manifest to find the last released version
2. Analyzes conventional commits since that version
3. Calculates the next version based on commit types (feat, fix, etc.)
4. For develop branch: Applies alpha suffix due to prerelease configuration

### Alpha Versions (from develop)
- Format: `vX.Y.Z-alpha.N` (e.g., `v0.3.1-alpha.1`, `v0.3.1-alpha.2`)
- Automatically incremented by Release Please using separate configuration files
- Marked as pre-release on GitHub
- Published to TestPyPI
- Tracked independently from main branch versions

### Stable Versions (from main)
- Format: `vX.Y.Z` (e.g., `v0.3.1`, `v0.3.2`)
- Follow semantic versioning
- Marked as stable release on GitHub
- Published to PyPI
- Use main branch configuration files

## Manual Release Triggers

You can manually trigger releases via GitHub Actions:
- Go to **Actions** → **"Release Please"** → **"Run workflow"**
- Select the appropriate branch (`develop` for alpha, `main` for stable)

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

## Testing Process

### Testing Alpha Releases
```bash
# Install from TestPyPI (alpha versions use the format X.Y.Z-alphaX)
pip install --index-url https://test.pypi.org/simple/ otdf-python==0.3.1a1

# Test functionality
python -c "import otdf_python; print('Alpha version works!')"
```

### Testing Stable Releases
```bash
# Install from PyPI
pip install otdf-python==0.3.1

# Test functionality
python -c "import otdf_python; print('Stable version works!')"
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
- Ensure commits were pushed to the correct branch

### Failed Publishing
- Check GitHub Actions logs for detailed error messages
- Verify PyPI trusted publisher configuration
- Ensure version doesn't already exist on the target repository

### Release Please Configuration Errors
- **Error: "Missing required manifest versions"**: Ensure both `.release-please-config-develop.json` and `.release-please-manifest-develop.json` are committed to the repository
- **Dynamic file creation errors**: The develop-specific configuration files must exist in the repository, not generated at runtime
- **Wrong branch configuration**: Verify the workflow uses the correct config and manifest files for each branch

### Version Conflicts
- Alpha and stable releases use separate configuration and manifest files to prevent conflicts
- Develop branch uses `.release-please-config-develop.json` and `.release-please-manifest-develop.json`
- Main branch uses `.release-please-config.json` and `.release-please-manifest.json`
- If conflicts occur, check the appropriate Release Please configuration files for the target branch

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

- `.release-please-config.json`: Main branch release configuration (stable releases)
- `.release-please-manifest.json`: Main branch version tracking
- `.release-please-config-develop.json`: Develop branch release configuration (alpha releases)
- `.release-please-manifest-develop.json`: Develop branch version tracking
- `.github/workflows/release-please.yaml`: GitHub Actions workflow

## Support

For release issues:
1. Check GitHub Actions logs in the "Release Please" workflow
2. Review the Release Please documentation
3. Create a GitHub issue with workflow logs
4. Contact repository maintainers
