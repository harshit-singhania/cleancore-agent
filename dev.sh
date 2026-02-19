#!/bin/bash
#
# CleanCore Agent - Development Server Manager
# Usage: ./dev.sh [start|stop|restart|status|logs] [--backend-only|--frontend-only]
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
BACKEND_PORT=8000
FRONTEND_PORT=5173
BACKEND_PID_FILE=".dev/backend.pid"
FRONTEND_PID_FILE=".dev/frontend.pid"
BACKEND_LOG=".dev/backend.log"
FRONTEND_LOG=".dev/frontend.log"

# Create .dev directory for logs and PIDs
mkdir -p .dev

# Helper functions
print_header() {
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${CYAN}  🚀 CleanCore Agent - Dev Server Manager${NC}"
    echo -e "${BOLD}${CYAN}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Get PID from file
get_pid() {
    local pid_file=$1
    if [ -f "$pid_file" ]; then
        cat "$pid_file"
    else
        echo ""
    fi
}

# Check if process is running
is_running() {
    local pid=$1
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Start backend server
start_backend() {
    local existing_pid=$(get_pid "$BACKEND_PID_FILE")
    
    if is_running "$existing_pid"; then
        print_warning "Backend is already running (PID: $existing_pid)"
        return 0
    fi
    
    if check_port $BACKEND_PORT; then
        print_error "Port $BACKEND_PORT is already in use"
        return 1
    fi
    
    print_info "Starting backend server on port $BACKEND_PORT..."
    
    cd "$BACKEND_DIR"
    
    # Activate venv and start uvicorn
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    else
        print_error "Virtual environment not found. Run: cd backend && python3 -m venv venv"
        cd ..
        return 1
    fi
    
    # Start uvicorn in background with logging
    nohup uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT --reload > "../$BACKEND_LOG" 2>&1 &
    local pid=$!
    cd ..
    
    echo $pid > "$BACKEND_PID_FILE"
    
    # Wait a moment and check if started successfully
    sleep 2
    
    if is_running "$pid"; then
        print_success "Backend started successfully (PID: $pid)"
        print_info "API URL: http://localhost:$BACKEND_PORT"
        print_info "Docs:    http://localhost:$BACKEND_PORT/docs"
        return 0
    else
        print_error "Backend failed to start. Check logs: $BACKEND_LOG"
        rm -f "$BACKEND_PID_FILE"
        return 1
    fi
}

# Start frontend server
start_frontend() {
    local existing_pid=$(get_pid "$FRONTEND_PID_FILE")
    
    if is_running "$existing_pid"; then
        print_warning "Frontend is already running (PID: $existing_pid)"
        return 0
    fi
    
    if check_port $FRONTEND_PORT; then
        print_error "Port $FRONTEND_PORT is already in use"
        return 1
    fi
    
    print_info "Starting frontend dev server on port $FRONTEND_PORT..."
    
    cd "$FRONTEND_DIR"
    
    if [ ! -d "node_modules" ]; then
        print_error "Node modules not found. Run: cd frontend && npm install"
        cd ..
        return 1
    fi
    
    # Start vite dev server in background
    nohup npm run dev > "../$FRONTEND_LOG" 2>&1 &
    local pid=$!
    cd ..
    
    echo $pid > "$FRONTEND_PID_FILE"
    
    # Wait a moment and check if started successfully
    sleep 3
    
    if is_running "$pid"; then
        print_success "Frontend started successfully (PID: $pid)"
        print_info "App URL: http://localhost:$FRONTEND_PORT"
        return 0
    else
        print_error "Frontend failed to start. Check logs: $FRONTEND_LOG"
        rm -f "$FRONTEND_PID_FILE"
        return 1
    fi
}

# Stop backend server
stop_backend() {
    local pid=$(get_pid "$BACKEND_PID_FILE")
    
    if [ -z "$pid" ]; then
        print_warning "Backend PID file not found"
        # Try to find and kill any process on the backend port
        local pids=$(lsof -Pi :$BACKEND_PORT -sTCP:LISTEN -t 2>/dev/null || true)
        if [ -n "$pids" ]; then
            print_info "Killing process(es) on port $BACKEND_PORT: $pids"
            echo "$pids" | xargs kill -9 2>/dev/null || true
        fi
        return 0
    fi
    
    if is_running "$pid"; then
        print_info "Stopping backend (PID: $pid)..."
        kill "$pid" 2>/dev/null || true
        sleep 1
        
        # Force kill if still running
        if is_running "$pid"; then
            kill -9 "$pid" 2>/dev/null || true
        fi
        
        print_success "Backend stopped"
    else
        print_warning "Backend was not running (stale PID file)"
    fi
    
    rm -f "$BACKEND_PID_FILE"
}

# Stop frontend server
stop_frontend() {
    local pid=$(get_pid "$FRONTEND_PID_FILE")
    
    if [ -z "$pid" ]; then
        print_warning "Frontend PID file not found"
        # Try to find and kill any process on the frontend port
        local pids=$(lsof -Pi :$FRONTEND_PORT -sTCP:LISTEN -t 2>/dev/null || true)
        if [ -n "$pids" ]; then
            print_info "Killing process(es) on port $FRONTEND_PORT: $pids"
            echo "$pids" | xargs kill -9 2>/dev/null || true
        fi
        return 0
    fi
    
    if is_running "$pid"; then
        print_info "Stopping frontend (PID: $pid)..."
        kill "$pid" 2>/dev/null || true
        sleep 1
        
        # Force kill if still running
        if is_running "$pid"; then
            kill -9 "$pid" 2>/dev/null || true
        fi
        
        print_success "Frontend stopped"
    else
        print_warning "Frontend was not running (stale PID file)"
    fi
    
    rm -f "$FRONTEND_PID_FILE"
}

# Show status
show_status() {
    echo -e "${BOLD}Server Status:${NC}"
    echo ""
    
    # Backend status
    local backend_pid=$(get_pid "$BACKEND_PID_FILE")
    if is_running "$backend_pid"; then
        echo -e "  ${GREEN}●${NC} Backend    ${GREEN}running${NC} (PID: $backend_pid, Port: $BACKEND_PORT)"
    else
        if check_port $BACKEND_PORT; then
            echo -e "  ${YELLOW}●${NC} Backend    ${YELLOW}running (untracked)${NC} (Port: $BACKEND_PORT)"
        else
            echo -e "  ${RED}●${NC} Backend    ${RED}stopped${NC}"
        fi
    fi
    
    # Frontend status
    local frontend_pid=$(get_pid "$FRONTEND_PID_FILE")
    if is_running "$frontend_pid"; then
        echo -e "  ${GREEN}●${NC} Frontend   ${GREEN}running${NC} (PID: $frontend_pid, Port: $FRONTEND_PORT)"
    else
        if check_port $FRONTEND_PORT; then
            echo -e "  ${YELLOW}●${NC} Frontend   ${YELLOW}running (untracked)${NC} (Port: $FRONTEND_PORT)"
        else
            echo -e "  ${RED}●${NC} Frontend   ${RED}stopped${NC}"
        fi
    fi
    
    echo ""
    
    if is_running "$backend_pid" || is_running "$frontend_pid"; then
        print_info "Quick URLs:"
        if is_running "$backend_pid"; then
            echo "  Backend API:  http://localhost:$BACKEND_PORT"
            echo "  API Docs:     http://localhost:$BACKEND_PORT/docs"
        fi
        if is_running "$frontend_pid"; then
            echo "  Frontend App: http://localhost:$FRONTEND_PORT"
        fi
    fi
}

# Show logs
show_logs() {
    local target=${1:-all}
    local lines=${2:-50}
    
    if [ "$target" == "backend" ] || [ "$target" == "all" ]; then
        if [ -f "$BACKEND_LOG" ]; then
            echo -e "${BOLD}${CYAN}=== Backend Logs (last $lines lines) ===${NC}"
            tail -n "$lines" "$BACKEND_LOG" 2>/dev/null || echo "No logs available"
            echo ""
        fi
    fi
    
    if [ "$target" == "frontend" ] || [ "$target" == "all" ]; then
        if [ -f "$FRONTEND_LOG" ]; then
            echo -e "${BOLD}${CYAN}=== Frontend Logs (last $lines lines) ===${NC}"
            tail -n "$lines" "$FRONTEND_LOG" 2>/dev/null || echo "No logs available"
        fi
    fi
}

# Follow logs
follow_logs() {
    local target=${1:-all}
    
    echo -e "${BOLD}${CYAN}Following logs (Ctrl+C to exit)...${NC}"
    echo ""
    
    if [ "$target" == "backend" ]; then
        tail -f "$BACKEND_LOG" 2>/dev/null || echo "Backend log not found"
    elif [ "$target" == "frontend" ]; then
        tail -f "$FRONTEND_LOG" 2>/dev/null || echo "Frontend log not found"
    else
        # Follow both with labels
        tail -f "$BACKEND_LOG" "$FRONTEND_LOG" 2>/dev/null || echo "Logs not found"
    fi
}

# Clean up log files and PID files
clean_dev() {
    print_info "Cleaning up dev files..."
    stop_backend
    stop_frontend
    rm -f "$BACKEND_LOG" "$FRONTEND_LOG"
    rm -f "$BACKEND_PID_FILE" "$FRONTEND_PID_FILE"
    print_success "Cleanup complete"
}

# Open browser
open_browser() {
    local url=$1
    print_info "Opening $url..."
    
    if command -v open >/dev/null 2>&1; then
        open "$url"  # macOS
    elif command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$url"  # Linux
    elif command -v start >/dev/null 2>&1; then
        start "$url"  # Windows
    else
        print_warning "Could not detect browser opener. Please open manually: $url"
    fi
}

# Show help
show_help() {
    print_header
    echo -e "${BOLD}Usage:${NC} ./dev.sh [command] [options]"
    echo ""
    echo -e "${BOLD}Commands:${NC}"
    echo "  start        Start development servers"
    echo "  stop         Stop development servers"
    echo "  restart      Restart development servers"
    echo "  status       Show server status"
    echo "  logs         Show recent logs"
    echo "  follow       Follow logs in real-time"
    echo "  clean        Stop servers and clean up log/PID files"
    echo "  open         Open browser to the frontend app"
    echo "  help         Show this help message"
    echo ""
    echo -e "${BOLD}Options:${NC}"
    echo "  --backend-only    Only operate on backend server"
    echo "  --frontend-only   Only operate on frontend server"
    echo "  -n, --lines NUM   Number of log lines to show (default: 50)"
    echo ""
    echo -e "${BOLD}Examples:${NC}"
    echo "  ./dev.sh start                    # Start both servers"
    echo "  ./dev.sh start --backend-only     # Start only backend"
    echo "  ./dev.sh logs -n 100              # Show last 100 log lines"
    echo "  ./dev.sh follow --backend-only    # Follow backend logs"
    echo "  ./dev.sh open                     # Open frontend in browser"
    echo ""
}

# Main script logic
main() {
    local command=${1:-help}
    local backend_only=false
    local frontend_only=false
    local lines=50
    
    # Parse arguments
    shift || true
    while [[ $# -gt 0 ]]; do
        case $1 in
            --backend-only)
                backend_only=true
                shift
                ;;
            --frontend-only)
                frontend_only=true
                shift
                ;;
            -n|--lines)
                lines="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    
    # Determine which servers to operate on
    local run_backend=true
    local run_frontend=true
    
    if [ "$backend_only" = true ]; then
        run_frontend=false
    elif [ "$frontend_only" = true ]; then
        run_backend=false
    fi
    
    # Execute command
    case $command in
        start)
            print_header
            
            if [ "$run_backend" = true ]; then
                start_backend
                echo ""
            fi
            
            if [ "$run_frontend" = true ]; then
                start_frontend
                echo ""
            fi
            
            print_info "Press Ctrl+C to stop following (servers keep running)"
            echo ""
            show_status
            ;;
            
        stop)
            print_header
            
            if [ "$run_backend" = true ]; then
                stop_backend
            fi
            
            if [ "$run_frontend" = true ]; then
                stop_frontend
            fi
            
            echo ""
            show_status
            ;;
            
        restart)
            print_header
            
            if [ "$run_backend" = true ]; then
                stop_backend
                sleep 1
                start_backend
                echo ""
            fi
            
            if [ "$run_frontend" = true ]; then
                stop_frontend
                sleep 1
                start_frontend
            fi
            ;;
            
        status)
            print_header
            show_status
            ;;
            
        logs)
            local target="all"
            if [ "$backend_only" = true ]; then
                target="backend"
            elif [ "$frontend_only" = true ]; then
                target="frontend"
            fi
            show_logs "$target" "$lines"
            ;;
            
        follow)
            local target="all"
            if [ "$backend_only" = true ]; then
                target="backend"
            elif [ "$frontend_only" = true ]; then
                target="frontend"
            fi
            follow_logs "$target"
            ;;
            
        clean)
            print_header
            clean_dev
            ;;
            
        open)
            open_browser "http://localhost:$FRONTEND_PORT"
            ;;
            
        help|--help|-h)
            show_help
            ;;
            
        *)
            print_error "Unknown command: $command"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
