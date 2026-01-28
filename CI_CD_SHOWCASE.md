# GitHub Actions CI/CD Pipeline Showcase

A complete overview of the automated CI/CD pipeline running on GitHub Actions for the MLOps Enterprise project.

---

## 📊 CI/CD Overview

Our pipeline automates **code quality**, **testing**, **security scanning**, and **deployment** for every push and pull request.

### Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD Flow                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  TRIGGER EVENTS                                                 │
│  ├─ Push to main/develop                                        │
│  ├─ Pull Request to main/develop                                │
│  ├─ Manual workflow dispatch                                    │
│  └─ Scheduled (Security scans)                                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               PIPELINE STAGES (Parallel)                │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                          │  │
│  │  Stage 1: CODE QUALITY       │  Stage 2: UNIT TESTS    │  │
│  │  ├─ Black (formatting)       │  ├─ Pytest              │  │
│  │  ├─ isort (imports)          │  ├─ Coverage report     │  │
│  │  ├─ flake8 (linting)         │  ├─ Codecov upload      │  │
│  │  └─ mypy (type checking)     │  └─ Archive artifacts   │  │
│  │                               │                         │  │
│  │  Stage 3: SECURITY SCANNING  │  Stage 4: DEPLOYMENT   │  │
│  │  ├─ Bandit (code audit)      │  └─ Docker build & push│  │
│  │  ├─ Safety (dependencies)    │     (main branch only)  │  │
│  │  └─ Trivy (vuln scan)        │                         │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  REPORTING & NOTIFICATIONS                                     │
│  ├─ GitHub Checks (Pass/Fail)                                  │
│  ├─ Coverage reports (Codecov)                                 │
│  ├─ Security alerts (GitHub Security)                          │
│  └─ Docker images pushed to GHCR                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Workflows & Jobs

### 1. **CI/CD Pipeline** (`ci-cd.yml`)
**Triggers:** `push` (main/develop), `pull_request` (main/develop)

#### Job 1.1: Code Quality & Linting
```yaml
name: Code Quality & Linting
runs-on-version: ubuntu-latest
tools: black, isort, flake8, mypy
duration: ~2-3 minutes
```

**What it does:**
- ✅ Checks code formatting with **Black**
- ✅ Validates import sorting with **isort**
- ✅ Lints code with **flake8** (detects E9, F63, F7, F82 errors)
- ✅ Type-checks with **mypy**

**Example output on GitHub:**
```
✓ Run black
  All checks passed

✓ Run isort
  All imports correctly sorted

✓ Run flake8
  No critical errors found

✓ Run mypy
  Type checking completed
```

---

#### Job 1.2: Unit Tests & Coverage
```yaml
name: Unit Tests
runs-on-version: ubuntu-latest
tools: pytest, pytest-cov, codecov
duration: ~2-3 minutes
```

**What it does:**
- ✅ Runs full test suite with **pytest**
- ✅ Generates coverage report
- ✅ Uploads to **Codecov** for tracking
- ✅ Archives HTML coverage report as artifact

**Example output:**
```
tests/test_validation.py::test_feature_validation PASSED
tests/test_smoke_imports.py::test_imports PASSED

coverage: 78%
report: htmlcov/index.html
```

**View coverage:** Download the `coverage-report` artifact from GitHub Actions run

---

#### Job 1.3: Security Scanning (in CI/CD)
```yaml
name: Security Scanning
tools: bandit, safety
duration: ~2 minutes
```

**What it does:**
- ✅ Scans Python code with **Bandit** (detects common vulnerabilities)
- ✅ Checks dependencies with **Safety** (known vulnerabilities)

---

### 2. **Security Scanning** (`security-scan.yml`)
**Triggers:** `schedule` (weekly), `workflow_dispatch` (manual)

#### Job 2.1: Dependency Check
```yaml
name: Dependency Check
schedule: Every Sunday at 00:00 UTC
tools: pip-audit, pip-tools
```

**What it does:**
- ✅ Audits Python packages for vulnerabilities using **pip-audit**
- ✅ Checks for outdated packages with **pip-tools**

---

#### Job 2.2: Trivy Vulnerability Scan
```yaml
name: Trivy Scan
tools: aquasecurity/trivy
```

**What it does:**
- ✅ Scans entire filesystem for vulnerabilities
- ✅ Generates SARIF report
- ✅ Uploads to GitHub Security tab

**View results:** Go to GitHub repo → Security → Code scanning

---

### 3. **Deploy to Production** (`deploy.yml`)
**Triggers:** `push` (main branch only), `tags` (v*), `workflow_dispatch`

#### Job 3.1: Build & Push Docker Image
```yaml
name: Deploy Services
tools: Docker Buildx, GHCR (GitHub Container Registry)
duration: ~5-10 minutes
```

**What it does:**
- ✅ Builds Docker image using **Docker Buildx**
- ✅ Generates metadata (branch, version, SHA tags)
- ✅ Pushes to **GitHub Container Registry** (GHCR)

**Image naming:**
```
ghcr.io/toni-ramchandani/mlops:main        # Branch tag
ghcr.io/toni-ramchandani/mlops:v1.0.0      # Version tag (semver)
ghcr.io/toni-ramchandani/mlops:main-sha... # Commit SHA
```

**Pull image locally:**
```bash
docker pull ghcr.io/toni-ramchandani/mlops:main
docker run -p 8000:8000 ghcr.io/toni-ramchandani/mlops:main
```

---

## 📈 How to Monitor & View Results

### Option 1: GitHub Web UI

1. Go to your repository: `https://github.com/toni-ramchandani/MLOps`
2. Click **Actions** tab
3. Select workflow run to view:
   - ✅ Job status (Passed/Failed)
   - 📊 Execution timeline
   - 📝 Logs for each step
   - 📦 Artifacts (coverage reports, scan results)

### Option 2: View Real-Time Results

After pushing code, GitHub Actions runs automatically. You can:

```bash
# Option A: Check status on GitHub
# → Actions tab shows live progress

# Option B: View specific workflow run
gh run view <run-id> --log

# Option C: List recent runs
gh run list --repo toni-ramchandani/MLOps
```

---

## 🎯 Example Workflow Triggers

### Push to `main` branch

```bash
git commit -m "feat: add new model training feature"
git push origin main
```

**Automatically runs:**
- ✅ Code Quality & Linting
- ✅ Unit Tests & Coverage
- ✅ Security Scanning (Bandit/Safety)
- ✅ Build & Push Docker Image

**Timeline:** ~12-15 minutes total

---

### Pull Request to `main`

```bash
git checkout -b feature/new-endpoint
git commit -m "feat: add /predict endpoint"
git push origin feature/new-endpoint
# Open PR on GitHub
```

**Automatically runs:**
- ✅ Code Quality & Linting
- ✅ Unit Tests & Coverage
- ✅ Security Scanning

**No deployment** (only on push to `main`)

---

### Manual Trigger (Workflow Dispatch)

Go to **Actions** → Select workflow → **Run workflow**

**Useful for:**
- Running security scans on-demand
- Deploying specific commits
- Testing workflow changes

---

## 📊 Status Badges

Add these badges to your README to show pipeline status:

```markdown
![CI/CD Pipeline](https://github.com/toni-ramchandani/MLOps/actions/workflows/ci-cd.yml/badge.svg?branch=main)
![Security Scan](https://github.com/toni-ramchandani/MLOps/actions/workflows/security-scan.yml/badge.svg)
![Deploy](https://github.com/toni-ramchandani/MLOps/actions/workflows/deploy.yml/badge.svg?branch=main)
```

**Renders as:**

![CI/CD Pipeline](https://github.com/toni-ramchandani/MLOps/actions/workflows/ci-cd.yml/badge.svg?branch=main)
![Security Scan](https://github.com/toni-ramchandani/MLOps/actions/workflows/security-scan.yml/badge.svg)
![Deploy](https://github.com/toni-ramchandani/MLOps/actions/workflows/deploy.yml/badge.svg?branch=main)

---

## 🔐 Security Features

### GitHub Security Tab Integration

1. **Dependabot Alerts**: Automatic notifications for vulnerable dependencies
2. **Code Scanning**: Trivy results appear in **Security → Code scanning**
3. **Secret Scanning**: Detects accidentally committed secrets

### Workflow Permissions

```yaml
permissions:
  contents: read      # Can read repo
  packages: write     # Can push Docker images
```

**No secrets stored in code** — Uses `${{ secrets.GITHUB_TOKEN }}`

---

## 📈 Performance & Metrics

| Workflow | Duration | Cost |
|----------|----------|------|
| Code Quality | ~2-3 min | Free (GitHub-hosted) |
| Unit Tests | ~2-3 min | Free |
| Security Scan | ~2 min | Free |
| Docker Build | ~5-10 min | Free |
| **Total** | **~12-18 min** | **Free** |

*GitHub Actions provides 2,000 free minutes/month for public repos*

---

## 🚀 Demo Workflow

### Step 1: Make a Code Change

```bash
cd /workspaces/MLOps
echo "# New feature" >> README.md
git add README.md
git commit -m "docs: update README"
git push origin main
```

### Step 2: Watch Actions Run

```bash
# Option A: View on GitHub
# → https://github.com/toni-ramchandani/MLOps/actions

# Option B: Use GitHub CLI
gh run list --repo toni-ramchandani/MLOps
gh run view <run-id> --log
```

### Step 3: Review Results

- ✅ Check status: Passed/Failed
- 📊 View coverage: Download `coverage-report` artifact
- 🔒 View security: Check Security tab
- 📦 View Docker image: `ghcr.io/toni-ramchandani/mlops:main`

---

## 🔧 Advanced: Customize Workflows

### Example: Add Slack Notifications

```yaml
- name: Notify Slack on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Pipeline failed: ${{ github.run_id }}"
      }
```

### Example: Add Performance Benchmarks

```yaml
- name: Run benchmarks
  run: |
    python -m pytest benchmarks/ --benchmark-only
```

### Example: Deploy to Multiple Environments

```yaml
deploy-staging:
  if: github.ref == 'refs/heads/develop'
  
deploy-production:
  if: github.ref == 'refs/heads/main' && startsWith(github.ref, 'refs/tags')
```

---

## 📚 Resources

- **Workflow Files**: [`.github/workflows/`](.github/workflows/)
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Docker & GHCR**: https://docs.github.com/en/packages/working-with-a-github-packages-registry
- **Codecov Integration**: https://codecov.io

---

## ✅ Checklist for Demo

- [ ] Show the workflows in `.github/workflows/` directory
- [ ] Trigger a workflow by pushing a commit
- [ ] Show GitHub Actions tab with live run
- [ ] View coverage report artifact
- [ ] Check Docker image in GHCR
- [ ] Show security scanning results
- [ ] Mention: 12-18 min pipeline, all automated, zero manual steps
- [ ] Reference status badges for CI/CD status

---

**Next:** See [DEMO.md](DEMO.md) for interactive API/MLflow demo, or [DEPLOYMENT.md](DEPLOYMENT.md) for Kubernetes deployment steps.
