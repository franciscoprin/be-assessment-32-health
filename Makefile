# Define the service name and command to exec
SERVICE_NAME = claim-process
CONTAINER_SHELL = /bin/bash  # Use /bin/sh if bash is not available

# .PHONY target to prevent make from confusing these with filenames
.PHONY: up down ssh logs build rebuild test help

# Start the containers
up:
	@echo "Starting the containers in detached mode."
	docker-compose up -d


# Stop the containers
down:
	@echo "Stopping the containers and removing any running instances."
	docker-compose down


# Enter the container's shell
ssh:
	@echo "Connecting to the container's shell."
	docker-compose exec $(SERVICE_NAME) $(CONTAINER_SHELL)

# Tail the logs of the container
logs:
	@echo "Displaying logs for the container, follow with -f for continuous output."
	docker-compose logs -f $(SERVICE_NAME)

# Build the container without starting it
build:
	@echo "Building the Docker image without starting the containers."
	docker-compose build

# Rebuild the containers and start them
rebuild:
	@echo "Rebuilding the Docker images and starting the containers."
	docker-compose up -d --build

# Run tests using pytest inside the container
test:
	@echo "Running tests using pytest inside the container."
	docker-compose run --rm $(SERVICE_NAME) pytest -s $(file)

# Show available commands and explanations
help:
	@echo "Available commands:"
	@echo "  up       - Start the containers (detached mode)."
	@echo "  down     - Stop and remove the containers."
	@echo "  ssh      - Enter the container's shell for interactive commands."
	@echo "  logs     - Tail the logs of the container (use -f for continuous output)."
	@echo "  build    - Build the container image without starting the service."
	@echo "  rebuild  - Rebuild the containers and restart them."
	@echo "  test     - Run pytest inside the container (you can specify a test file using 'file')."
