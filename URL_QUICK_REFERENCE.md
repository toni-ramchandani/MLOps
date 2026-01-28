# 🗺️ URL & Configuration Quick Reference Card

## 📍 Where Each URL is Defined

```
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE ENDPOINTS                          │
├─────────────────────┬──────────────┬───────────────────────────┤
│ Service             │ URL/Port     │ Config File               │
├─────────────────────┼──────────────┼───────────────────────────┤
│ API                 │ :8000        │ docker-compose.yml:18     │
│ MLflow              │ :5000        │ docker-compose.yml:31     │
│ Prometheus          │ :9090        │ docker-compose.yml:76     │
│ Grafana             │ :3000        │ docker-compose.yml:92     │
│ PostgreSQL          │ :5432        │ docker-compose.yml:52     │
└─────────────────────┴──────────────┴───────────────────────────┘
```

## 📋 Configuration Files Map

```
infra/docker/
├── docker-compose.yml    ← Service ports & environment
│                           Port: 8000, 5000, 3000, 9090, 5432
│
├── .env.example          ← Environment variables
│                           MLFLOW_TRACKING_URI=http://mlflow:5000
│                           API_PORT=8000
│
└── prometheus.yml        ← Metrics scraping
                           Targets: api:8000, mlflow:5000

configs/
└── config.yaml           ← Application configuration
                           mlflow.tracking_uri: "sqlite:///mlflow.db"

src/mlops_enterprise/
├── settings.py           ← URL resolution logic
│                           Priority: ENV > config.yaml > default
│
└── api.py                ← API endpoints
                           /health, /predict, /metrics, /docs
```

## 🔧 Quick Edit Guide

### Edit Ports
📄 File: `infra/docker/docker-compose.yml`
```yaml
api:
  ports:
    - "8000:8000"        ← Change first number to new host port
```

### Edit MLflow URL
📄 File: `infra/docker/.env`
```env
MLFLOW_TRACKING_URI=http://mlflow:5000    ← Change this
```

### Edit Database Connection
📄 File: `configs/config.yaml`
```yaml
mlflow:
  tracking_uri: "postgresql://user:pass@host:5432/mlflow"
```

## 🌐 Access Patterns

### From Host Machine
```bash
curl http://localhost:8000/health
curl http://localhost:5000
open http://localhost:3000
```

### From Inside Docker Container
```bash
curl http://api:8000/health
curl http://mlflow:5000
curl http://prometheus:9090
```

## 📊 Environment Variable Resolution

```
MLflow URI is resolved in this order:

1. MLFLOW_TRACKING_URI (environment variable)
   └─ Set in: docker-compose.yml or .env
   
2. config.yaml (config file)
   └─ File: configs/config.yaml
   
3. Default fallback
   └─ sqlite:///mlflow.db
```

## 🔍 Search Commands

Find all URLs in codebase:
```bash
grep -r "localhost\|mlflow\|http" infra/docker/ configs/ src/
grep -r "8000\|5000\|3000\|9090" . --include="*.yml" --include="*.yaml"
```

## 📝 Common Modifications

### Change API Port 8000 → 9000
```yaml
# docker-compose.yml
ports:
  - "9000:8000"        # Change this
  
# validate.sh
API_URL="http://localhost:9000"

# prometheus.yml
targets: ['api:9000']
```

### Use Remote MLflow Server
```env
# .env
MLFLOW_TRACKING_URI=http://mlflow.company.com:5000
```

### Enable SSL/TLS
```yaml
# docker-compose.yml
environment:
  - MLFLOW_TRACKING_URI=https://mlflow.company.com:5000
```

## ✅ Verification Steps

```bash
# 1. Check ports are accessible
netstat -tulpn | grep -E "8000|5000|3000"

# 2. Test API
curl -v http://localhost:8000/health

# 3. Check Docker network
docker network inspect mlops-network

# 4. View environment
docker-compose exec api env | grep MLFLOW

# 5. Run full validation
./infra/docker/validate.sh
```

## 🚨 Troubleshooting URLs

| Problem | Solution |
|---------|----------|
| `Connection refused` | Check if services are running: `docker-compose ps` |
| `Name or service not known` | Check container network: `docker network inspect mlops-network` |
| `MLflow not found` | Verify `MLFLOW_TRACKING_URI` env var in docker-compose.yml |
| `Port already in use` | Change port mapping: `- "9000:8000"` |
| `Authentication failed` | Check credentials in `.env` file |

## 📞 Related Files

- [DEPLOYMENT.md](DEPLOYMENT.md) - Full deployment guide
- [docker-compose.yml](infra/docker/docker-compose.yml) - Service definitions
- [.env.example](infra/docker/.env.example) - Environment variables
- [settings.py](src/mlops_enterprise/settings.py) - Python config
- [validate.sh](infra/docker/validate.sh) - Health checks

---

**Need to modify URLs? Edit the files listed above!** 🔧
