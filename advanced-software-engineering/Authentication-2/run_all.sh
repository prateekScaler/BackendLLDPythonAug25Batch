#!/bin/bash

# Script to run all authentication demo servers simultaneously

set -e

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Store PIDs for cleanup
PIDS=()

cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping all servers...${NC}"
    for pid in "${PIDS[@]}"; do
        kill $pid 2>/dev/null
    done
    exit 0
}

trap cleanup SIGINT SIGTERM

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}   Authentication Demos Setup & Run    ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check for Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo -e "${RED}Error: Python not found. Please install Python 3.${NC}"
    exit 1
fi

echo -e "${GREEN}Using Python:${NC} $($PYTHON --version)"
echo ""

# Function to setup a demo
setup_demo() {
    local demo_name=$1
    local demo_dir=$2

    echo -e "${YELLOW}Setting up $demo_name...${NC}"

    cd "$demo_dir"

    # Install requirements if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "  Installing dependencies..."
        $PYTHON -m pip install -r requirements.txt -q
    fi

    # Run migrations
    echo "  Running migrations..."
    $PYTHON manage.py migrate --run-syncdb -v 0 2>/dev/null || $PYTHON manage.py migrate -v 0

    echo -e "${GREEN}  $demo_name ready!${NC}"
}

# Setup all demos
echo -e "${YELLOW}Installing dependencies and running migrations...${NC}"
echo ""

setup_demo "session_demo" "$SCRIPT_DIR/session_demo"
setup_demo "jwt_demo" "$SCRIPT_DIR/jwt_demo"
setup_demo "oauth2_demo" "$SCRIPT_DIR/oauth2_demo"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}        Starting All Servers           ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Start session_demo on port 8001
echo -e "${YELLOW}Starting session_demo on port 8001...${NC}"
cd "$SCRIPT_DIR/session_demo" && $PYTHON manage.py runserver 2>&1 | sed 's/^/[session_demo] /' &
PIDS+=($!)

# Start jwt_demo on port 8002
echo -e "${YELLOW}Starting jwt_demo on port 8002...${NC}"
cd "$SCRIPT_DIR/jwt_demo" && $PYTHON manage.py runserver 2>&1 | sed 's/^/[jwt_demo] /' &
PIDS+=($!)

# Start oauth2_demo on port 8003
echo -e "${YELLOW}Starting oauth2_demo on port 8003...${NC}"
cd "$SCRIPT_DIR/oauth2_demo" && $PYTHON manage.py runserver 2>&1 | sed 's/^/[oauth2_demo] /' &
PIDS+=($!)

sleep 2

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}        All Servers Running            ${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "  session_demo: http://localhost:8001"
echo "  jwt_demo:     http://localhost:8002"
echo "  oauth2_demo:  http://localhost:8003"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all servers${NC}"
echo ""

# Wait for all background processes
wait
