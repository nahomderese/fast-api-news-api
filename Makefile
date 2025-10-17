.PHONY: help install run test docker-build docker-run clean lint format

help:
	@echo "SWEN AI-Enriched News Pipeline - Available Commands"
	@echo "=================================================="
	@echo "install        - Install dependencies"
	@echo "dev            - Start development server (uses mise)"
	@echo "docker         - Start services with docker-compose (uses mise)"
	@echo "db-init        - Initialize database (uses mise)"
	@echo "test           - Run tests (uses mise)"
	@echo "docker-build   - Build Docker image"
	@echo "docker-run     - Run Docker container"
	@echo "clean          - Clean up temporary files"
	@echo "lint           - Run linters"
	@echo "format         - Format code"
	@echo ""
	@echo "Note: This project uses mise for environment management."
	@echo "Run 'mise install' first to set up the environment."

install:
	pip install -r requirements.txt

dev:
	@echo "Starting development server with mise..."
	mise run dev

docker:
	@echo "Starting services with docker-compose via mise..."
	mise run docker

db-init:
	@echo "Initializing database with mise..."
	mise run db-init

test:
	@echo "Running tests with mise..."
	mise run test

docker-build:
	docker build -t swen-ai-pipeline:latest .

docker-run:
	docker run -p 8000:8000 --name swen-api swen-ai-pipeline:latest

docker-compose:
	docker-compose up --build

docker-stop:
	docker-compose down

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf build/ dist/ *.egg-info

lint:
	@echo "Running linters..."
	@python -m flake8 swen_ai_pipeline/ --max-line-length=100 --ignore=E501 2>/dev/null || echo "flake8 not installed"
	@python -m pylint swen_ai_pipeline/ 2>/dev/null || echo "pylint not installed"

format:
	@echo "Formatting code..."
	@black swen_ai_pipeline/ 2>/dev/null || echo "black not installed"
	@isort swen_ai_pipeline/ 2>/dev/null || echo "isort not installed"

dev:
	pip install -e .
	pip install black flake8 pylint isort pytest pytest-asyncio

k8s-deploy:
	kubectl apply -f k8s/configmap.yaml
	kubectl apply -f k8s/deployment.yaml

k8s-delete:
	kubectl delete -f k8s/deployment.yaml
	kubectl delete -f k8s/configmap.yaml

