# MLOps Enterprise Starter - Deployment Guide

## Overview

This is an enterprise-grade MLOps platform with:
- **API Service**: FastAPI-based prediction service
- **MLflow**: Model tracking and registry
- **PostgreSQL**: Persistent database backend
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards
- **CI/CD**: GitHub Actions automated workflows

## Prerequisites

- Docker & Docker Compose (v2.0+)
- Git
- Python 3.10+ (for local development)

## Quick Start

### 1. Local Development

```bash
# Install dependencies
pip install -e .

# Start services with docker-compose
cd infra/docker
docker-compose up -d --build

# API will be available at: http://localhost:8000
```

### 2. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| MLflow | http://localhost:5000 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin/admin |
| PostgreSQL | localhost:5432 | mlops_user/mlops_password |

### 3. Validate Deployment

```bash
# Run validation script
./infra/docker/validate.sh

# Or manually check
docker compose -f infra/docker/docker-compose.yml ps
curl http://localhost:8000/health
curl http://localhost:8000/metrics
```

## Project Structure

```
.
├── .github/workflows/          # GitHub Actions CI/CD
│   ├── ci-cd.yml              # Main pipeline
│   ├── security-scan.yml       # Security scanning
│   └── deploy.yml              # Deployment workflow
├── infra/
│   ├── docker/                 # Docker configuration
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml
│   │   ├── prometheus.yml
│   │   └── validate.sh
│   └── k8s/                    # Kubernetes manifests
├── src/mlops_enterprise/
│   ├── api.py                  # FastAPI application
│   ├── train.py                # Training pipeline
│   ├── monitoring.py           # Monitoring utilities
│   ├── registry.py             # Model registry
│   └── ...
├── tests/                       # Test suite
├── configs/                     # Configuration files
└── pyproject.toml              # Python project config
```

## GitHub Actions Workflows

### CI/CD Pipeline (`ci-cd.yml`)

Runs on every push/PR to main or develop:

1. **Code Quality**: Black, isort, flake8, mypy
2. **Unit Tests**: pytest with coverage
3. **Security**: bandit, safety
4. **Docker Build**: Build and push images
5. **Validation**: docker-compose config check
6. **Integration Tests**: Optional end-to-end tests

### Security Scanning (`security-scan.yml`)

Runs weekly and on-demand:

1. **Dependency Check**: pip-audit, pip-tools
2. **Trivy Scan**: Filesystem vulnerability scanning
3. **SARIF Upload**: GitHub Security integration

### Deployment (`deploy.yml`)

Runs on main branch push/tags:

1. Build Docker image
2. Push to registry
3. Deploy to production (customize for your environment)

## Configuration

### Environment Variables

Create `.env` from template:

```bash
cp infra/docker/.env.example infra/docker/.env
```

Key variables:
- `MLFLOW_TRACKING_URI`: MLflow tracking server URL
- `POSTGRES_USER`/`PASSWORD`: Database credentials
- `LOG_LEVEL`: Application logging level

### Docker Compose

Configuration in `infra/docker/docker-compose.yml`:

- **api**: FastAPI application
- **mlflow**: Model tracking server
- **postgres**: Database backend
- **prometheus**: Metrics collection
- **grafana**: Visualization dashboard

## Development Workflow

### Local Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest -v

# Check code quality
black --check src tests
flake8 src tests
```

### Running Services

```bash
cd infra/docker

# Start all services
docker-compose up -d --build

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Testing

```bash
# Unit tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Specific test file
pytest tests/test_validation.py -v
```

## Production Deployment

### Option 1: Docker Compose (Simple)

```bash
cd infra/docker
docker-compose -f docker-compose.yml up -d
```

### Option 2: Kubernetes (Scalable)

```bash
# Apply manifests
kubectl apply -f infra/k8s/

# Check deployment
kubectl get pods -n mlops
kubectl logs -f deployment/mlops-api -n mlops
```

### Option 3: Cloud Deployment

- **AWS ECS/Fargate**: Use docker-compose or custom task definitions
- **GCP Cloud Run**: Deploy API container
- **Azure ACI**: Container instances
- **Heroku**: buildpacks or Docker

## Monitoring & Observability

### Metrics

API exports Prometheus metrics at `/metrics`:

```bash
curl http://localhost:8000/metrics
```

Key metrics:
- `predict_requests_total`: Total prediction requests
- `predict_latency_seconds`: Prediction latency histogram

### Dashboards

Access Grafana at http://localhost:3000:

1. Add Prometheus data source (http://prometheus:9090)
2. Create dashboards to visualize metrics
3. Set up alerts for SLOs

### Logging

Logs stored in `infra/docker/logs/`:
- `api/`: Application logs
- `mlflow/`: MLflow server logs
- `postgres/`: Database logs
- `prometheus/`: Metrics logs

## Troubleshooting

### API not starting

```bash
# Check logs
docker-compose logs api

# Validate health
curl -v http://localhost:8000/health
```

### Database connection errors

```bash
# Verify PostgreSQL
docker-compose exec postgres psql -U mlops_user -d mlflow -c "SELECT 1;"

# Check network
docker network ls
```

### MLflow sync issues

```bash
# Check artifacts directory
docker-compose exec mlflow ls -la /mlflow/artifacts

# Verify database
docker-compose exec postgres psql -U mlops_user -d mlflow
```

## Security Best Practices

1. **Secrets Management**
   - Never commit `.env` with real credentials
   - Use GitHub Secrets for CI/CD
   - Rotate database passwords regularly

2. **Image Security**
   - Use minimal base images (python:3.12-slim)
   - Run as non-root user (mlops:mlops)
   - Scan images with Trivy

3. **Network Security**
   - Use internal network for service communication
   - Expose only necessary ports
   - Implement firewall rules

4. **Database Security**
   - Use strong passwords
   - Enable SSL/TLS for connections
   - Regular backups

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes (triggers CI)
4. Create pull request
5. Await automated checks & review

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MLflow Documentation](https://mlflow.org/docs/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Prometheus Metrics](https://prometheus.io/docs/practices/instrumentation/)

## License

MIT License - See LICENSE file

## Support

For issues and questions:
1. Check existing GitHub issues
2. Create detailed bug reports
3. Include logs and environment info
