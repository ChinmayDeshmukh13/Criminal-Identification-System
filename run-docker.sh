#!/bin/bash

# Criminal Identification System - Docker Build and Run Script for Linux/Mac
# This script builds and runs the application using Docker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "===================================="
echo "Criminal Identification System"
echo "Docker Build and Run Script"
echo "===================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}Docker and Docker Compose are installed${NC}"
echo ""

# Menu
show_menu() {
    echo "Select operation:"
    echo "1. Start application (docker-compose up)"
    echo "2. Stop application (docker-compose down)"
    echo "3. Build image (docker build)"
    echo "4. View logs (docker-compose logs)"
    echo "5. Restart services (docker-compose restart)"
    echo "6. Remove all and clean up"
    echo "7. Run tests"
    echo "8. Shell access to container"
    echo "9. Exit"
    echo ""
    read -p "Enter your choice (1-9): " choice
}

# Operations
start_app() {
    echo ""
    echo -e "${YELLOW}Starting Criminal Identification System with Docker Compose...${NC}"
    docker-compose up -d
    
    echo ""
    echo -e "${GREEN}Application started successfully!${NC}"
    echo ""
    echo "Access the application at:"
    echo "  - Frontend: http://localhost"
    echo "  - API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/api/docs (development only)"
    echo ""
    echo "View logs with: docker-compose logs -f"
    echo ""
}

stop_app() {
    echo ""
    echo -e "${YELLOW}Stopping Criminal Identification System...${NC}"
    docker-compose down
    echo -e "${GREEN}Application stopped${NC}"
    echo ""
}

build_image() {
    echo ""
    echo -e "${YELLOW}Building Docker image...${NC}"
    docker build -t ifrs:latest .
    
    echo -e "${GREEN}Image built successfully: ifrs:latest${NC}"
    echo ""
}

view_logs() {
    echo ""
    echo -e "${YELLOW}Showing logs (Press Ctrl+C to stop)...${NC}"
    docker-compose logs -f
    echo ""
}

restart_services() {
    echo ""
    echo -e "${YELLOW}Restarting services...${NC}"
    docker-compose restart
    echo -e "${GREEN}Services restarted${NC}"
    echo ""
}

cleanup() {
    echo ""
    echo -e "${RED}WARNING: This will remove all containers, images, and volumes!${NC}"
    read -p "Are you sure? (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        echo -e "${YELLOW}Cleaning up...${NC}"
        docker-compose down -v
        docker rmi ifrs:latest 2>/dev/null || true
        echo -e "${GREEN}Cleanup complete${NC}"
    else
        echo "Cleanup cancelled"
    fi
    echo ""
}

run_tests() {
    echo ""
    echo -e "${YELLOW}Running tests...${NC}"
    docker-compose exec api python -m pytest tests/ -v
    echo ""
}

shell_access() {
    echo ""
    echo -e "${YELLOW}Opening shell in container...${NC}"
    docker-compose exec api /bin/bash
    echo ""
}

# Main loop
while true; do
    show_menu
    
    case $choice in
        1)
            start_app
            ;;
        2)
            stop_app
            ;;
        3)
            build_image
            ;;
        4)
            view_logs
            ;;
        5)
            restart_services
            ;;
        6)
            cleanup
            ;;
        7)
            run_tests
            ;;
        8)
            shell_access
            ;;
        9)
            echo ""
            echo -e "${GREEN}Exiting...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            echo ""
            ;;
    esac
done
