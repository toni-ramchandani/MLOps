# MLOps Enterprise Starter

[![CI/CD Pipeline](https://github.com/toni-ramchandani/MLOps/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/toni-ramchandani/MLOps/actions/workflows/ci-cd.yml)
[![Security Scan](https://github.com/toni-ramchandani/MLOps/actions/workflows/security-scan.yml/badge.svg)](https://github.com/toni-ramchandani/MLOps/actions/workflows/security-scan.yml)
[![codecov](https://codecov.io/gh/toni-ramchandani/MLOps/branch/main/graph/badge.svg)](https://codecov.io/gh/toni-ramchandani/MLOps)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Enterprise-grade, open-source MLOps platform with production-ready infrastructure, monitoring, and CI/CD pipelines.

## 🚀 Features

### Core Platform
- **FastAPI**: Modern, async Python web framework
- **MLflow**: Model tracking, registry, and serving
- **PostgreSQL**: Persistent database for models and metadata
- **Prometheus & Grafana**: Comprehensive monitoring and dashboards

### DevOps & Infrastructure
- **Docker Compose**: Local development and testing
- **Kubernetes**: Production deployment manifests
- **GitHub Actions**: Automated CI/CD pipelines
- **Security**: Trivy scanning, dependency checks, SBOM generation

### Development
- **Code Quality**: Black, isort, flake8, mypy
- **Testing**: pytest with coverage reporting
- **Documentation**: Comprehensive guides and API docs
- **Contributing**: Guidelines and templates

## 📋 Prerequisites

- **Python**: 3.10+
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Git**: 2.30+

## ⚡ Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/toni-ramchandani/MLOps.git
cd MLOps

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
```

### 2. Start Services

```bash
cd infra/docker
docker-compose up -d --build
```

### 3. Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| API | http://localhost:8000 | ML Model API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| MLflow | http://localhost:5000 | Model Registry |
| Prometheus | http://localhost:9090 | Metrics |
| Grafana | http://localhost:3000 | Dashboards |

### 4. Test API

```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"rows": [{"feature1": 1.0, "feature2": 2.0}]}'
```

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive deployment guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development and contribution guidelines
- **[API Docs](http://localhost:8000/docs)** - Interactive API documentation
- **[Configuration](configs/config.yaml)** - Application configuration

## 🏗️ Project Structure

```
.
├── .github/
│   ├── workflows/              # GitHub Actions CI/CD
│   │   ├── ci-cd.yml           # Main pipeline
│   │   ├── security-scan.yml   # Security checks
│   │   └── deploy.yml          # Deployment workflow
│   └── ISSUE_TEMPLATE/         # Issue templates
├── infra/
│   ├── docker/                 # Docker configuration
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── prometheus.yml
│   │   └── validate.sh
│   └── k8s/                    # Kubernetes manifests
│       └── deployment.yaml
├── src/mlops_enterprise/
│   ├── api.py                  # FastAPI application
│   ├── train.py                # Training pipeline
│   ├── monitoring.py           # Metrics
│   ├── registry.py             # Model registry
│   ├── settings.py             # Configuration
│   └── ...
├── tests/                       # Test suite
├── configs/                     # Configuration files
├── Makefile                     # Development commands
├── pyproject.toml              # Python project config
├── DEPLOYMENT.md               # Deployment guide
└── CONTRIBUTING.md             # Contributing guide
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run all checks
make lint test
```

### Common Commands

```bash
make help              # Show all available commands
make lint              # Run code quality checks
make test              # Run tests
make coverage          # Generate coverage report
make docker-up         # Start Docker services
make docker-down       # Stop Docker services
make validate          # Validate entire setup
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Check code
flake8 src tests
mypy src --ignore-missing-imports
```

### Testing

```bash
# Run tests
pytest -v

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/test_api.py -v
```

## 🐳 Docker

### Local Development

```bash
cd infra/docker

# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f api

# Run commands in container
docker-compose exec api pytest

# Stop services
docker-compose down
```

### Building Images

```bash
# Build image
docker build -t mlops:dev -f infra/docker/Dockerfile .

# Push to registry
docker tag mlops:dev ghcr.io/toni-ramchandani/mlops:dev
docker push ghcr.io/toni-ramchandani/mlops:dev
```

## ☸️ Kubernetes

Deploy to Kubernetes cluster:

```bash
# Apply manifests
kubectl apply -f infra/k8s/

# Check deployment
kubectl get pods -n mlops
kubectl logs -f deployment/mlops-api -n mlops

# Scale deployment
kubectl scale deployment mlops-api -n mlops --replicas=5
```

## 🔄 CI/CD Pipelines

GitHub Actions workflows:

### CI/CD Pipeline (`ci-cd.yml`)
- ✅ Code quality checks (Black, isort, flake8, mypy)
- ✅ Unit tests with coverage
- ✅ Security scanning (bandit, safety)
- ✅ Docker build & push
- ✅ Integration tests
- ✅ Artifact uploads

### Security Scan (`security-scan.yml`)
- ✅ Weekly dependency checks
- ✅ Trivy filesystem scanning
- ✅ SARIF vulnerability reporting

### Deploy (`deploy.yml`)
- ✅ Automatic image build & push on main
- ✅ Version tagging
- ✅ Deployment notifications

## 📊 Monitoring

### Prometheus Metrics

Access metrics at http://localhost:9000/metrics

Key metrics:
- `predict_requests_total` - Total prediction requests
- `predict_latency_seconds` - Prediction latency histogram

### Grafana Dashboards

1. Access http://localhost:3000 (admin/admin)
2. Add Prometheus data source: http://prometheus:9090
3. Create/import dashboards

### Health Checks

```bash
# API health
curl http://localhost:8000/health

# Database health
docker-compose exec postgres pg_isready -U mlops_user

# MLflow health
curl http://localhost:5000
```

## 🔐 Security

- Non-root Docker user
- Security scanning in CI/CD
- Dependency vulnerability checks
- Network isolation with Docker networks
- Secrets management best practices

See [DEPLOYMENT.md](DEPLOYMENT.md#security-best-practices) for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development setup
- Code standards
- Testing requirements
- Pull request process
- Commit guidelines

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help

1. Check [existing issues](https://github.com/toni-ramchandani/MLOps/issues)
2. Read [documentation](DEPLOYMENT.md)
3. Create a [bug report](https://github.com/toni-ramchandani/MLOps/issues/new?template=bug_report.yml)
4. Reach out in discussions

### Troubleshooting

See [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting) for common issues.

## 🎯 Roadmap

- [ ] Multi-model serving
- [ ] Advanced monitoring (DataDog, ELK)
- [ ] Feature store integration
- [ ] A/B testing framework
- [ ] AutoML pipeline
- [ ] Batch prediction service

## 🙏 Acknowledgments

Built with:
- [FastAPI](https://fastapi.tiangolo.com/)
- [MLflow](https://mlflow.org/)
- [Prometheus](https://prometheus.io/)
- [Docker](https://www.docker.com/)
- [Kubernetes](https://kubernetes.io/)

---

**Made with ❤️ by the MLOps team**

[⬆ back to top](#mlops-enterprise-starter)
