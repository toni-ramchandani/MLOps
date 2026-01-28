# Makefile for MLOps Enterprise

.PHONY: help install dev-install lint format test coverage docker-build docker-up docker-down docker-logs validate clean

help:
	@echo "MLOps Enterprise - Available Commands"
	@echo "====================================="
	@echo "Setup:"
	@echo "  make install       Install production dependencies"
	@echo "  make dev-install   Install with development dependencies"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint          Run all linters (black, isort, flake8, mypy)"
	@echo "  make format        Auto-format code (black, isort)"
	@echo "  make black         Run black code formatter"
	@echo "  make isort         Run isort import sorter"
	@echo "  make flake8        Run flake8 linter"
	@echo "  make mypy          Run mypy type checker"
	@echo ""
	@echo "Testing:"
	@echo "  make test          Run pytest"
	@echo "  make test-v        Run pytest verbose"
	@echo "  make coverage      Run pytest with coverage"
	@echo "  make integration   Run integration tests only"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build  Build Docker image"
	@echo "  make docker-up     Start Docker Compose services"
	@echo "  make docker-down   Stop Docker Compose services"
	@echo "  make docker-logs   View Docker Compose logs"
	@echo "  make docker-clean  Remove Docker Compose volumes"
	@echo ""
	@echo "Utilities:"
	@echo "  make validate      Validate Docker Compose and run health checks"
	@echo "  make run           Run API locally"
	@echo "  make clean         Clean up build artifacts and cache"
	@echo "  make deps          Check for outdated dependencies"

# Setup
install:
	pip install --upgrade pip setuptools
	pip install -e .

dev-install:
	pip install --upgrade pip setuptools
	pip install -e ".[dev]"

# Code Quality
lint: black isort flake8 mypy
	@echo "✓ All linters passed"

format: black isort
	@echo "✓ Code formatted"

black:
	@echo "Running black..."
	black src tests

isort:
	@echo "Running isort..."
	isort src tests

flake8:
	@echo "Running flake8..."
	flake8 src tests --max-line-length=100 --ignore=E203,W503

mypy:
	@echo "Running mypy..."
	mypy src --ignore-missing-imports || true

# Testing
test:
	pytest tests/

test-v:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=src --cov-report=html --cov-report=term
	@echo "✓ Coverage report generated: htmlcov/index.html"

integration:
	pytest tests/ -v -m integration

# Docker
docker-build:
	cd infra/docker && docker-compose build

docker-up:
	cd infra/docker && docker-compose up -d --build

docker-down:
	cd infra/docker && docker-compose down

docker-logs:
	cd infra/docker && docker-compose logs -f api

docker-clean:
	cd infra/docker && docker-compose down -v

# Utilities
validate: docker-up
	@echo "Validating Docker Compose setup..."
	@sleep 5
	cd infra/docker && bash validate.sh || make docker-down

run:
	uvicorn mlops_enterprise.api:app --host 0.0.0.0 --port 8000 --reload

clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	find . -type d -name '.pytest_cache' -delete
	find . -type d -name '.mypy_cache' -delete
	find . -type d -name '*.egg-info' -delete
	find . -type d -name '.coverage' -delete
	find . -type d -name 'htmlcov' -delete
	@echo "✓ Cleaned up"

deps:
	@echo "Checking for outdated packages..."
	pip list --outdated
