.PHONY: help install install-dev run run-prod build docker-build docker-up docker-down docker-logs test lint format clean

# Default Python interpreter
PYTHON := python3

help:
	@echo "Criminal Identification System - Development Tasks"
	@echo ""
	@echo "Available commands:"
	@echo "  make install           - Install production dependencies"
	@echo "  make install-dev       - Install development dependencies"
	@echo "  make run               - Run development server"
	@echo "  make run-prod          - Run production server"
	@echo "  make build             - Build application"
	@echo "  make docker-build      - Build Docker image"
	@echo "  make docker-up         - Start containers with Docker Compose"
	@echo "  make docker-down       - Stop containers with Docker Compose"
	@echo "  make docker-logs       - View Docker container logs"
	@echo "  make docker-clean      - Remove all Docker containers and images"
	@echo "  make test              - Run tests"
	@echo "  make lint              - Run code linter"
	@echo "  make format            - Format code with black"
	@echo "  make clean             - Clean up temporary files"

install:
	$(PYTHON) -m pip install -r backend/requirements.txt
	@echo "✓ Dependencies installed"

install-dev:
	$(PYTHON) -m pip install -r backend/requirements.txt
	$(PYTHON) -m pip install pytest pytest-cov black flake8 mypy
	@echo "✓ Development dependencies installed"

run:
	$(PYTHON) -m uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000

run-prod:
	$(PYTHON) -m gunicorn --workers=4 --worker-class=uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 backend.app:app

build:
	$(PYTHON) -m pip install -e .
	@echo "✓ Application built"

docker-build:
	docker build -t ifrs:latest .
	@echo "✓ Docker image built: ifrs:latest"

docker-up:
	docker-compose up -d
	@echo "✓ Containers started"
	@echo ""
	@echo "Access the application:"
	@echo "  Frontend: http://localhost"
	@echo "  API: http://localhost:8000"
	@echo "  Docs: http://localhost:8000/api/docs"

docker-down:
	docker-compose down
	@echo "✓ Containers stopped"

docker-logs:
	docker-compose logs -f

docker-clean: docker-down
	docker rmi ifrs:latest
	@echo "✓ Docker cleanup complete"

test:
	$(PYTHON) -m pytest tests/ -v --cov=backend

lint:
	flake8 backend/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 backend/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:
	black backend/ frontend/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	@echo "✓ Cleanup complete"

# Environment setup
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ .env file created from template"; \
	else \
		echo "ℹ .env file already exists"; \
	fi

# Virtual environment setup
venv:
	$(PYTHON) -m venv .venv
	@echo "✓ Virtual environment created"
	@echo ""
	@echo "Activate with:"
	@echo "  source .venv/bin/activate  (Linux/Mac)"
	@echo "  .\.venv\Scripts\activate   (Windows)"
