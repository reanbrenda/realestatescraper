# Real Estate Scraper API - Development Makefile
# Provides common commands for development, testing, and deployment

.PHONY: help install start stop restart logs clean test migrate makemigrations createsuperuser shell collectstatic build push pull

# Default target
help:
	@echo "Real Estate Scraper API - Development Commands"
	@echo "=============================================="
	@echo ""
	@echo "Development:"
	@echo "  install          Install dependencies"
	@echo "  start            Start all services"
	@echo "  stop             Stop all services"
	@echo "  restart          Restart all services"
	@echo "  logs             View service logs"
	@echo "  shell            Open Django shell"
	@echo ""
	@echo "Database:"
	@echo "  migrate          Run database migrations"
	@echo "  makemigrations   Create new migrations"
	@echo "  createsuperuser  Create admin user"
	@echo ""
	@echo "Testing:"
	@echo "  test             Run Django tests"
	@echo "  test-coverage    Run tests with coverage"
	@echo ""
	@echo "Maintenance:"
	@echo "  collectstatic    Collect static files"
	@echo "  clean            Clean up temporary files"
	@echo ""
	@echo "Docker:"
	@echo "  build            Build Docker images"
	@echo "  push             Push images to registry"
	@echo "  pull             Pull images from registry"
	@echo ""
	@echo "Production:"
	@echo "  deploy           Deploy to production"
	@echo "  backup           Backup database"
	@echo "  restore          Restore database"

# Development commands
install:
	@echo "Installing dependencies..."
	docker compose exec django pip install -r requirements.txt

start:
	@echo "Starting services..."
	docker compose up -d

stop:
	@echo "Stopping services..."
	docker compose down

restart:
	@echo "Restarting services..."
	docker compose restart

logs:
	@echo "Viewing service logs..."
	docker compose logs -f

shell:
	@echo "Opening Django shell..."
	docker compose exec django python manage.py shell

# Database commands
migrate:
	@echo "Running database migrations..."
	docker compose exec django python manage.py migrate

makemigrations:
	@echo "Creating new migrations..."
	docker compose exec django python manage.py makemigrations

createsuperuser:
	@echo "Creating superuser..."
	docker compose exec django python manage.py createsuperuser

# Testing commands
test:
	@echo "Running Django tests..."
	docker compose exec django python manage.py test

test-coverage:
	@echo "Running tests with coverage..."
	docker compose exec django coverage run --source='.' manage.py test
	docker compose exec django coverage report
	docker compose exec django coverage html

# Maintenance commands
collectstatic:
	@echo "Collecting static files..."
	docker compose exec django python manage.py collectstatic --noinput

clean:
	@echo "Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name ".DS_Store" -delete
	@echo "Cleanup complete!"

# Docker commands
build:
	@echo "Building Docker images..."
	docker compose build --no-cache

push:
	@echo "Pushing images to registry..."
	docker compose push

pull:
	@echo "Pulling images from registry..."
	docker compose pull

# Production commands
deploy:
	@echo "Deploying to production..."
	@echo "This command should be customized for your production environment"

backup:
	@echo "Backing up database..."
	docker compose exec db pg_dump -U postgres real_estate > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore:
	@echo "Restoring database..."
	@echo "Usage: make restore FILE=backup_file.sql"
	@if [ -z "$(FILE)" ]; then echo "Please specify FILE parameter"; exit 1; fi
	docker compose exec -T db psql -U postgres real_estate < $(FILE)

# Health check
health:
	@echo "Checking service health..."
	docker compose ps
	@echo ""
	@echo "Testing API endpoints..."
	@curl -s -o /dev/null -w "API Status: %{http_code}\n" http://localhost:8000/api/ || echo "API not responding"

# Development setup
setup:
	@echo "Setting up development environment..."
	@if [ ! -f .env ]; then cp env.example .env; echo "Created .env file from template"; fi
	@echo "Starting services..."
	docker compose up -d
	@echo "Waiting for database..."
	@sleep 10
	@echo "Running migrations..."
	docker compose exec django python manage.py migrate
	@echo "Setup complete! Access the API at http://localhost:8000/api/"

# Quick development cycle
dev:
	@echo "Starting development environment..."
	docker compose up -d
	@echo "Development environment ready!"
	@echo "API: http://localhost:8000/api/"
	@echo "Admin: http://localhost:8000/admin/"
	@echo "Docs: http://localhost:8000/api/docs/"
	@echo ""
	@echo "Use 'make logs' to view logs"
	@echo "Use 'make stop' to stop services"
