# MLOps Enterprise Demo Guide

A quick walkthrough of the MLOps stack running locally with Docker Compose.

## Prerequisites

- Docker & Docker Compose installed
- Git repository cloned

## Quick Start

### 1. Start the Stack

```bash
cd infra/docker
docker-compose up -d --build
```

Wait ~30 seconds for all services to be healthy:

```bash
docker-compose ps
```

### 2. Access the Services

| Service | URL | Purpose |
|---------|-----|---------|
| **API** | http://localhost:8000 | FastAPI backend |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **MLflow** | http://localhost:5000 | Experiment tracking |
| **Prometheus** | http://localhost:9090 | Metrics collection |
| **Grafana** | http://localhost:3000 | Dashboards (admin/admin) |
| **Dashboard** | Open `dashboard.html` in browser | Landing page with all links |

---

## Demo Workflow

### Step 1: Check API Health

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### Step 2: View API Documentation

Open http://localhost:8000/docs in your browser. Try the `/predict` endpoint:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
```

### Step 3: Track an Experiment in MLflow

```bash
python3 -c "
import mlflow

mlflow.set_tracking_uri('http://localhost:5000')
mlflow.set_experiment('demo-experiment')

with mlflow.start_run():
    mlflow.log_param('learning_rate', 0.01)
    mlflow.log_metric('accuracy', 0.95)
    mlflow.log_metric('loss', 0.12)
    print('Experiment logged!')
"
```

Visit http://localhost:5000 to see your experiment.

### Step 4: Monitor Metrics

1. Go to http://localhost:9090 (Prometheus)
2. Query example: `http_requests_total`
3. Go to http://localhost:3000 (Grafana)
   - Login: `admin` / `admin`
   - Explore metrics dashboards

---

## Common Commands

### View Logs

```bash
cd infra/docker
docker-compose logs -f api          # API logs
docker-compose logs -f mlflow       # MLflow logs
docker-compose logs -f prometheus   # Prometheus logs
```

### Run Tests

```bash
cd /workspaces/MLOps
pytest tests/ -v
```

### Stop the Stack

```bash
cd infra/docker
docker-compose down
```

### Clean Everything (including volumes)

```bash
cd infra/docker
docker-compose down -v
```

---

## Troubleshooting

### Containers not starting?
```bash
docker-compose logs
```

### API not responding?
```bash
curl -v http://localhost:8000/health
```

### MLflow unreachable?
Check PostgreSQL: `docker-compose ps | grep postgres`

### High memory usage?
Reduce Prometheus retention: Edit `prometheus.yml` or use `--storage.tsdb.retention.time=7d`

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│         Docker Compose Network (mlops-net)      │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────┐  ┌──────────────┐             │
│  │   FastAPI   │  │    MLflow    │             │
│  │  API (8000) │  │  (5000)      │             │
│  └─────────────┘  └──────────────┘             │
│         │                │                      │
│         └────────┬───────┘                      │
│                  │                              │
│          ┌───────▼────────┐                    │
│          │  PostgreSQL    │                    │
│          │   (5432)       │                    │
│          └────────────────┘                    │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐   │
│  │  Prometheus      │  │   Grafana        │   │
│  │   (9090)         │  │   (3000)         │   │
│  └──────────────────┘  └──────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘

Persistent Volumes:
 - mlflow_db: MLflow artifacts
 - postgres_data: PostgreSQL data
 - prometheus_data: Time-series metrics
 - grafana_data: Grafana dashboards
```

---

## Next Steps

- **Deploy to Kubernetes**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **CI/CD Pipeline**: Runs on every push (`.github/workflows/`)
- **Monitoring**: Set up custom Grafana dashboards
- **Model Registry**: Use MLflow Model Registry for versioning

---

**Questions?** See [README_ENTERPRISE.md](README_ENTERPRISE.md) or check logs with `docker-compose logs`.
