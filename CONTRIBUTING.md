# MLOps Enterprise - Contributing Guide

## Development Setup

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git
- Make (optional but recommended)

### Local Setup

```bash
# Clone repository
git clone https://github.com/toni-ramchandani/MLOps.git
cd MLOps

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

## Code Standards

### Style Guide

We follow PEP 8 with these tools:

- **Black**: Code formatting (line length: 100)
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

### Pre-commit Checks

```bash
# Run all checks before committing
make lint

# Or individually:
black src tests
isort src tests
flake8 src tests --max-line-length=100
mypy src --ignore-missing-imports
```

### Running Tests

```bash
# All tests
pytest -v

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_api.py -v

# Watch mode
pytest-watch tests/
```

## Commit Guidelines

Use conventional commits:

```
feat: add health check endpoint
fix: resolve model loading race condition
docs: update deployment guide
test: add integration tests
refactor: simplify prediction logic
chore: update dependencies
```

## Pull Request Process

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -m "feat: my feature"`
3. Push branch: `git push origin feature/my-feature`
4. Create PR with detailed description
5. Automated checks run automatically
6. Address review feedback
7. Merge when approved

## Project Structure

### Source Code (`src/mlops_enterprise/`)

- `api.py`: FastAPI application and endpoints
- `train.py`: Training pipeline
- `monitoring.py`: Metrics and monitoring
- `registry.py`: Model registry integration
- `settings.py`: Configuration management
- `data.py`: Data utilities
- `validation.py`: Input validation
- `utils.py`: Helper functions

### Tests (`tests/`)

- `test_smoke_imports.py`: Import checks
- `test_validation.py`: Data validation tests
- Add new tests for new features

### Infrastructure (`infra/`)

- `docker/`: Docker configuration
- `k8s/`: Kubernetes manifests
- `.github/workflows/`: CI/CD pipelines

## Making Changes

### Adding New Features

1. Create feature branch
2. Write tests first (TDD)
3. Implement feature
4. Update documentation
5. Run all checks: `make lint test`
6. Submit PR

### Adding Dependencies

```bash
# Add to pyproject.toml [project] dependencies
pip install --upgrade pip setuptools
pip install <package>

# Regenerate lock file if using poetry
poetry lock
```

### Adding Configuration

1. Update `configs/config.yaml` with new keys
2. Update `src/mlops_enterprise/settings.py`
3. Document in DEPLOYMENT.md
4. Add tests

## Testing

### Unit Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from mlops_enterprise.api import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
```

### Integration Tests

```python
# Mark with pytest marker
@pytest.mark.integration
def test_predict_e2e():
    """End-to-end prediction test"""
    response = client.post("/predict", json={
        "rows": [{"feature1": 1.0, "feature2": 2.0}]
    })
    assert response.status_code == 200
```

### Running Integration Tests

```bash
# Only integration tests
pytest -m integration

# Skip integration tests
pytest -m "not integration"
```

## Documentation

### Code Documentation

Use docstrings for all public functions:

```python
def predict(request: PredictRequest) -> Dict[str, Any]:
    """
    Generate predictions for input data.
    
    Args:
        request: PredictRequest containing feature rows
        
    Returns:
        Dictionary with predictions and metadata
        
    Raises:
        ValueError: If model is not ready
    """
```

### File Documentation

Add docstring at top of files:

```python
"""
Module for model prediction and serving.

This module provides the FastAPI application and prediction endpoints
for the enterprise MLOps platform.
"""
```

## Docker Development

### Building Images

```bash
# Build with specific tag
docker build -t mlops:dev -f infra/docker/Dockerfile .

# Build for production
docker build -t mlops:latest -f infra/docker/Dockerfile .
```

### Docker Compose Development

```bash
cd infra/docker

# Start services with live code reload
docker-compose up -d --build

# View specific service logs
docker-compose logs -f api

# Execute command in container
docker-compose exec api pytest

# Rebuild specific service
docker-compose up -d --build api
```

## Debugging

### Local Development

```bash
# Run API with debug logging
PYTHONUNBUFFERED=1 uvicorn mlops_enterprise.api:app --reload

# Python debugging
import pdb; pdb.set_trace()  # or breakpoint()
```

### Docker Debugging

```bash
# Access container shell
docker-compose exec api bash

# View environment
docker-compose exec api env

# Python interactive
docker-compose exec api python
```

## Performance Optimization

### Profiling

```bash
# CPU profiling
python -m cProfile -s cumtime -m pytest tests/

# Memory profiling
pip install memory-profiler
python -m memory_profiler script.py
```

### Load Testing

```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/locustfile.py
```

## Release Process

### Version Bumping

Follow semantic versioning (MAJOR.MINOR.PATCH):

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Commit: `chore: bump version to X.Y.Z`
4. Tag: `git tag vX.Y.Z`
5. Push: `git push origin main && git push origin --tags`

### Creating Releases

- GitHub Actions automatically builds and pushes images
- Release notes generated from commits
- Docker images tagged with version

## CI/CD Pipeline

### GitHub Actions Workflows

1. **CI on PR**: Lint, test, security scan
2. **Build on Push**: Build Docker image
3. **Deploy on Tag**: Deploy to production
4. **Security Weekly**: Dependency and vulnerability scan

### Local CI Simulation

```bash
# Run local GitHub Actions
act -j code-quality
act -j unit-tests
```

## Troubleshooting Development

### Virtual Environment Issues

```bash
# Recreate environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Dependency Conflicts

```bash
# Check installed versions
pip list

# Update pip tools
pip install --upgrade pip setuptools wheel

# Try fresh install
pip install --force-reinstall -e .
```

### Docker Issues

```bash
# Clean up containers and volumes
docker-compose down -v

# Remove dangling images
docker image prune -f

# Rebuild from scratch
docker-compose up -d --build --force-recreate
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions](https://docs.github.com/en/actions)

## Questions?

1. Check existing issues
2. Review documentation
3. Create new issue with details
4. Ask in discussions

## Code of Conduct

- Be respectful and inclusive
- Constructive feedback only
- Assume good intent
- Report violations to maintainers

---

Happy contributing! 🚀
