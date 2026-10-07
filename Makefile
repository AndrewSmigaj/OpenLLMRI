# Concept MRI - Development Makefile

.PHONY: help setup download-model run-api run-ui dev stop health fmt typecheck lint clean test test-backend test-frontend

help:
	@echo "Available commands:"
	@echo "  setup          - Set up development environment (.venv + npm)"
	@echo "  download-model - Download gpt-oss-20b model weights (~40GB)"
	@echo "  run-api        - Start FastAPI backend"
	@echo "  run-ui         - Start React frontend"
	@echo "  dev            - Instructions for running both servers"
	@echo "  stop           - Kill all running servers"
	@echo "  health         - Check backend health status"
	@echo "  test           - Run every test suite (test-backend + test-frontend)"
	@echo "  test-backend   - Run the backend tests (pytest)"
	@echo "  test-frontend  - Run the frontend checks (lint, type check, build)"
	@echo "  fmt            - Format code with black"
	@echo "  typecheck      - Run mypy type checking"
	@echo "  lint           - Run ruff linting"
	@echo "  clean          - Clean cache and temp files"

setup:
	@echo "Creating Python virtual environment (Python 3.10.12)..."
	python3.10 -m venv .venv
	@echo "Installing the exact locked Python dependencies..."
	.venv/bin/pip install -r backend/requirements.lock.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "Creating data directories..."
	mkdir -p data/lake data/experiments data/models
	@echo ""
	@echo "Setup complete!"
	@echo "Next: run 'make download-model' to download gpt-oss-20b (~40GB)"

download-model:
	@echo "Downloading gpt-oss-20b model (~40GB, this will take a while)..."
	.venv/bin/pip install -q huggingface_hub[cli]
	huggingface-cli download openai/gpt-oss-20b --local-dir data/models/gpt-oss-20b
	@echo "Model downloaded to data/models/gpt-oss-20b/"

run-api:
	@echo "Starting FastAPI backend (model takes several minutes to load)..."
	cd backend/src && ../../.venv/bin/python -m uvicorn api.main:app --host 0.0.0.0 --port 8000

run-ui:
	@echo "Starting React frontend..."
	cd frontend && npm run dev

dev:
	@echo "Run these commands in separate terminals:"
	@echo "  Terminal 1: make run-api"
	@echo "  Terminal 2: make run-ui"
	@echo ""
	@echo "Or use Claude Code: open 'claude' and ask it to start the servers."

# fuser kills by port, which is reliable on WSL2; pkill is not.
stop:
	@echo "Stopping all servers..."
	-fuser -k 8000/tcp 5173/tcp
	@sleep 1
	@echo "Verifying clean shutdown..."
	@fuser 8000/tcp 5173/tcp >/dev/null 2>&1 && echo "Port 8000 or 5173 is still in use." || echo "All servers stopped."

health:
	@curl -s --max-time 5 http://localhost:8000/health 2>/dev/null | .venv/bin/python -m json.tool || echo "Backend not responding"

test: test-backend test-frontend

test-backend:
	@if [ -d backend/tests ]; then \
		echo "Running backend tests..."; \
		cd backend && ../.venv/bin/python -m pytest tests/ -v; \
	else \
		echo "No backend tests yet (backend/tests/ does not exist)."; \
	fi

test-frontend:
	@echo "Running frontend checks (lint, type check, build)..."
	cd frontend && npm run lint && npm run build

fmt:
	@echo "Formatting Python code..."
	.venv/bin/black backend/src --line-length 100
	.venv/bin/ruff check backend/src --fix

typecheck:
	@echo "Running type checks..."
	.venv/bin/mypy backend/src --strict

lint:
	@echo "Running linter..."
	.venv/bin/ruff check backend/src

clean:
	@echo "Cleaning cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"
