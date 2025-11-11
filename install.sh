#!/bin/bash
# Automated Installation Script for Healthcare Workflow Composer
# This script installs all dependencies and verifies the setup

set -e  # Exit on error

echo "=========================================="
echo "Healthcare Workflow Composer - Installer"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo "ℹ️  $1"
}

# Step 1: Check Python version
echo "Step 1: Checking Python version..."
PYTHON_CMD=""

# Try to find Python 3.10+
for cmd in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)

        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 10 ]; then
            PYTHON_CMD=$cmd
            print_success "Found $cmd (version $VERSION)"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    print_error "Python 3.10+ not found"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  brew install python@3.11"
    echo ""
    echo "Or download from: https://www.python.org/downloads/"
    exit 1
fi

# Step 2: Check Node.js
echo ""
echo "Step 2: Checking Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js not found"
    echo ""
    echo "Please install Node.js:"
    echo "  brew install node"
    echo ""
    echo "Or download from: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node --version)
print_success "Found Node.js $NODE_VERSION"

# Step 3: Check API key
echo ""
echo "Step 3: Checking API key configuration..."
API_KEYS_FILE="backend/config/api_keys.json"

if [ ! -f "$API_KEYS_FILE" ]; then
    print_warning "API keys file not found, creating from template..."
    cp backend/config/api_keys.json.example "$API_KEYS_FILE"
    print_info "Created $API_KEYS_FILE"
    print_warning "Please add your Claude API key to $API_KEYS_FILE before running the server"
else
    # Check if API key is configured
    API_KEY=$($PYTHON_CMD -c "import json; data=json.load(open('$API_KEYS_FILE')); print(data['claude_agent_sdk']['api_key'])" 2>/dev/null || echo "")

    if [ -z "$API_KEY" ] || [ "$API_KEY" == "" ]; then
        print_warning "API key is empty in $API_KEYS_FILE"
        print_info "Please add your Claude API key before running the server"
    elif [[ $API_KEY == sk-ant-* ]]; then
        print_success "API key configured (${API_KEY:0:15}...)"
    else
        print_warning "API key format looks incorrect (should start with sk-ant-)"
    fi
fi

# Step 4: Install Python dependencies
echo ""
echo "Step 4: Installing Python dependencies..."
echo "This may take a few minutes..."
echo ""

cd backend

# Upgrade pip first
print_info "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip --quiet

# Install Claude Agent SDK
print_info "Installing Claude Agent SDK..."
if $PYTHON_CMD -m pip install claude-agent-sdk --quiet; then
    print_success "Claude Agent SDK installed"
else
    print_error "Failed to install Claude Agent SDK"
    print_info "Trying alternative installation method..."
    if $PYTHON_CMD -m pip install git+https://github.com/anthropics/claude-agent-sdk-python.git --quiet; then
        print_success "Claude Agent SDK installed from GitHub"
    else
        print_error "Failed to install Claude Agent SDK. Please install manually."
        exit 1
    fi
fi

# Install other dependencies
print_info "Installing FastAPI and other dependencies..."
$PYTHON_CMD -m pip install fastapi uvicorn[standard] websockets pydantic pydantic-settings python-multipart python-dotenv orjson --quiet
print_success "All dependencies installed"

cd ..

# Step 5: Verify installation
echo ""
echo "Step 5: Verifying installation..."

# Test imports
if $PYTHON_CMD -c "import claude_agent_sdk; import fastapi; import uvicorn" 2>/dev/null; then
    print_success "All packages can be imported"
else
    print_error "Some packages failed to import"
    exit 1
fi

# Test key manager
if $PYTHON_CMD -c "from backend.config.key_manager import key_manager; key_manager.get_status()" >/dev/null 2>&1; then
    print_success "Key manager working"
else
    print_warning "Key manager test failed (this is OK if API key isn't configured yet)"
fi

# Step 6: Summary
echo ""
echo "=========================================="
echo "Installation Complete! 🎉"
echo "=========================================="
echo ""
print_success "Python: $PYTHON_CMD ($VERSION)"
print_success "Node.js: $NODE_VERSION"
print_success "All dependencies installed"
echo ""

# Check if API key is configured
API_KEY=$($PYTHON_CMD -c "import json; data=json.load(open('$API_KEYS_FILE')); print(data['claude_agent_sdk']['api_key'])" 2>/dev/null || echo "")

if [ -z "$API_KEY" ] || [ "$API_KEY" == "" ]; then
    echo "⚠️  Next Step: Add your Claude API key"
    echo ""
    echo "1. Get API key from: https://console.anthropic.com/"
    echo "2. Edit: $API_KEYS_FILE"
    echo "3. Add your key to the 'api_key' field"
    echo ""
else
    echo "✅ Ready to start!"
    echo ""
    echo "Start the backend server:"
    echo "  cd backend"
    echo "  $PYTHON_CMD app.py"
    echo ""
    echo "Start the frontend (in a new terminal):"
    echo "  python3 -m http.server 8000"
    echo ""
    echo "Open in browser:"
    echo "  http://localhost:8000/workflow-composer.html"
    echo ""
fi

echo "=========================================="
echo ""
echo "📚 Documentation:"
echo "  - Quick Start: QUICKSTART.md"
echo "  - API Key Setup: SETUP_API_KEY.md"
echo "  - Integration Guide: CLAUDE_AGENT_SDK_INTEGRATION.md"
echo ""
