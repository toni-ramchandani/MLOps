# How to Run GitHub Actions CI/CD on GitHub

Complete step-by-step guide to trigger and monitor your CI/CD pipeline.

---

## 🚀 Method 1: Automatic Trigger (Push Code)

### Step 1: Make a Code Change Locally

```bash
cd /workspaces/MLOps

# Edit any file
echo "# Updated README" >> README.md

# Stage and commit
git add README.md
git commit -m "docs: update README"

# Push to GitHub
git push origin main
```

### Step 2: Watch It Run on GitHub

**Option A: Web Browser**
1. Go to: `https://github.com/toni-ramchandani/MLOps`
2. Click **Actions** tab (top navigation)
3. You'll see the workflow running in real-time:
   ```
   docs: update README
   ✓ Code Quality & Linting (In Progress)
   ✓ Unit Tests (In Progress)
   ✓ Security Scanning (In Progress)
   ✓ Deploy to Production (Queued - waits for others)
   ```

4. Click on the workflow to see:
   - Real-time logs from each job
   - Execution timeline
   - Status (✅ Passed or ❌ Failed)
   - Artifacts (coverage reports, scan results)

---

## 🎯 Method 2: Manual Trigger (Workflow Dispatch)

Run any workflow manually from GitHub without committing code.

### Option A: Via Web UI

1. Go to: `https://github.com/toni-ramchandani/MLOps/actions`
2. In left sidebar, select a workflow:
   - **CI/CD Pipeline**
   - **Security Scan** 
   - **Deploy to Production**

3. Click **Run workflow** button (blue button on right)
4. Select branch: `main`
5. Click **Run workflow** again to confirm
6. Watch it execute in real-time

### Option B: Via GitHub CLI

**Install GitHub CLI (if not already):**
```bash
# macOS
brew install gh

# Ubuntu/Linux
sudo apt install gh

# Windows
choco install gh
```

**Login to GitHub:**
```bash
gh auth login
```

**Trigger workflow manually:**
```bash
# Run CI/CD pipeline on main branch
gh workflow run ci-cd.yml --ref main

# Run security scan
gh workflow run security-scan.yml --ref main

# Run deployment
gh workflow run deploy.yml --ref main
```

**Monitor in real-time:**
```bash
# List all recent runs
gh run list --repo toni-ramchandani/MLOps

# Watch a specific run
gh run view <run-id> --watch

# See full logs
gh run view <run-id> --log
```

---

## 📊 Method 3: Pull Request (Testing Before Merge)

Test your code before merging to main.

### Step 1: Create a Feature Branch

```bash
cd /workspaces/MLOps

# Create new branch
git checkout -b feature/new-endpoint

# Make changes
echo "New feature code" > src/mlops_enterprise/new_feature.py

# Commit
git add .
git commit -m "feat: add new feature"

# Push to GitHub
git push origin feature/new-endpoint
```

### Step 2: Open Pull Request

1. Go to: `https://github.com/toni-ramchandani/MLOps`
2. Click **Pull requests** tab
3. Click **New pull request** button
4. Base branch: `main`
5. Compare branch: `feature/new-endpoint`
6. Click **Create pull request**
7. Add title and description
8. Click **Create pull request**

### Step 3: Watch Checks Run

CI/CD automatically runs on the PR:
- ✅ Code Quality & Linting
- ✅ Unit Tests & Coverage
- ✅ Security Scanning

**Note:** Deployment does NOT run on PRs (only on push to main)

View results:
- GitHub shows checks below PR description
- Click **Details** to see full logs
- Reviewers can see coverage changes

---

## 🔄 Automated Triggers (What Runs When)

| Trigger | What Runs |
|---------|-----------|
| **Push to `main`** | ✅ All 4 jobs (Lint, Test, Security, Deploy) |
| **Push to `develop`** | ✅ Lint, Test, Security (NO Deploy) |
| **Pull Request** | ✅ Lint, Test, Security (NO Deploy) |
| **Push tag `v*`** | ✅ Deploy with semantic version |
| **Manual dispatch** | ✅ Run any workflow manually |
| **Weekly schedule** | ✅ Security scan (Sundays) |

---

## 📈 Live Monitoring on GitHub

### Real-Time Status View

1. **Actions Tab** → `https://github.com/toni-ramchandani/MLOps/actions`
   - Shows all workflows
   - Current status (✅ or ❌)
   - Execution time
   - Click to expand details

### Drill Down into a Run

1. Click on workflow run (e.g., "docs: update README")
2. See 4 jobs side-by-side:
   ```
   Code Quality        Unit Tests        Security          Deploy
   ✓ 2m 45s           ✓ 3m 12s          ✓ 2m 18s          ⏸ Queued
   
   - Run black         - pytest          - bandit          - Docker build
   - Run isort         - Coverage        - safety check    - Push GHCR
   - Run flake8        - Upload codecov  - Trivy scan      - Tag images
   - Run mypy          - Archive HTML    - SARIF upload
   ```

3. Click on any job to see full logs
4. Search logs with Ctrl+F

---

## 📊 Viewing Results & Artifacts

### Coverage Reports

1. Go to workflow run
2. Click **Artifacts** section
3. Download `coverage-report` zip
4. Extract and open `htmlcov/index.html` in browser
   - See line-by-line coverage
   - Identify untested code
   - Track coverage trends

### Security Scan Results

1. Go to repo → **Security** tab
2. Click **Code scanning**
3. View all Trivy vulnerabilities found
4. Filter by severity

### Docker Images

1. Go to repo → **Packages** (right sidebar)
2. See all Docker images pushed to GHCR:
   ```
   ghcr.io/toni-ramchandani/mlops:main
   ghcr.io/toni-ramchandani/mlops:v1.0.0
   ghcr.io/toni-ramchandani/mlops:main-sha-abc123
   ```

3. Pull any image:
   ```bash
   docker pull ghcr.io/toni-ramchandani/mlops:main
   docker run -p 8000:8000 ghcr.io/toni-ramchandani/mlops:main
   ```

---

## 🧪 Live Demo Steps

### Step 1: Trigger Pipeline

```bash
cd /workspaces/MLOps
git add -A
git commit -m "demo: trigger CI/CD pipeline"
git push origin main
```

### Step 2: Open GitHub Actions in Browser

```bash
# Open Actions tab
"$BROWSER" "https://github.com/toni-ramchandani/MLOps/actions"
```

### Step 3: Watch Workflow Progress

- See 4 jobs running in parallel
- Refresh every 10-15 seconds to see progress
- Click on any job to see logs

### Step 4: Check Results After ~15 Minutes

1. **Code Quality** (✅ Passed)
   - All formatting and linting passed
   - No type errors

2. **Unit Tests** (✅ Passed)
   - All tests passed
   - Coverage: 78%
   - Download coverage report

3. **Security** (✅ Passed)
   - No critical vulnerabilities
   - All dependencies safe

4. **Deploy** (✅ Completed)
   - Docker image built
   - Pushed to GHCR
   - Image: `ghcr.io/toni-ramchandani/mlops:main`

---

## 🔗 GitHub Actions URLs to Reference

### Main Pages

```
Actions Dashboard:
https://github.com/toni-ramchandani/MLOps/actions

CI/CD Workflow:
https://github.com/toni-ramchandani/MLOps/actions/workflows/ci-cd.yml

Security Workflow:
https://github.com/toni-ramchandani/MLOps/actions/workflows/security-scan.yml

Deploy Workflow:
https://github.com/toni-ramchandani/MLOps/actions/workflows/deploy.yml

Packages (Docker Images):
https://github.com/toni-ramchandani/MLOps/pkgs/container/mlops

Security Tab:
https://github.com/toni-ramchandani/MLOps/security
```

---

## ⚙️ Workflow Files to Review

See how workflows are configured:

```bash
# View CI/CD configuration
cat .github/workflows/ci-cd.yml

# View Security Scan configuration
cat .github/workflows/security-scan.yml

# View Deploy configuration
cat .github/workflows/deploy.yml
```

Location in repo:
```
.github/
└── workflows/
    ├── ci-cd.yml          # Runs on push/PR
    ├── security-scan.yml  # Runs weekly + manual
    └── deploy.yml         # Runs on push to main + tags
```

---

## 📱 Quick Reference

### Push Code to Trigger All Workflows
```bash
git add .
git commit -m "your message"
git push origin main
```

### Manual Trigger via CLI
```bash
# List available workflows
gh workflow list

# Run a workflow
gh workflow run ci-cd.yml --ref main

# Check status
gh run list
```

### View in Browser
```
https://github.com/toni-ramchandani/MLOps/actions
```

---

## ✅ What You Should See

After pushing code to `main`:

```
✅ Workflow triggered
   ↓
✅ Code Quality (2-3 min) → ✓ PASSED
✅ Unit Tests (2-3 min) → ✓ PASSED
✅ Security Scan (2 min) → ✓ PASSED
   ↓
✅ Deploy (5-10 min) → ✓ COMPLETED
   Docker image pushed to GHCR
   
Total time: ~12-18 minutes
```

---

## 🎥 Demo Checklist

- [ ] Push code: `git push origin main`
- [ ] Open Actions tab on GitHub
- [ ] Show all 4 jobs running
- [ ] Click on a job to see logs
- [ ] Wait for completion (~15 min)
- [ ] Show coverage report artifact
- [ ] Check Docker image in Packages
- [ ] Point out: "All automated, no manual steps"

---

**Next:** See [DEMO.md](../DEMO.md) for interactive API testing or open [ci-cd-visualizer.html](../infra/docker/ci-cd-visualizer.html) for visual overview.
