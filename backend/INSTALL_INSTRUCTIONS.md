# Installation Instructions

## ✅ Your API Key is Configured!

Your Claude API key has been successfully added to `config/api_keys.json`.

## Prerequisites

Before installing Python dependencies, you need:

1. **Python 3.10+** ✅ (You have this)
2. **Node.js** ⚠️ (Required by Claude Agent SDK)
3. **Claude Code CLI** (Will be installed automatically)

## Step-by-Step Installation

### 1. Check if Node.js is Installed

```bash
node --version
npm --version
```

**If you see version numbers:** ✅ Node.js is installed, proceed to step 3

**If you see "command not found":** Install Node.js first (step 2)

### 2. Install Node.js (if needed)

**On macOS (recommended):**
```bash
# Using Homebrew
brew install node

# Or download from: https://nodejs.org/
```

**Verify installation:**
```bash
node --version  # Should show v18.x.x or higher
npm --version   # Should show 9.x.x or higher
```

### 3. Upgrade pip (recommended)

```bash
python3 -m pip install --upgrade pip
```

### 4. Install Claude Agent SDK

The Claude Agent SDK has specific requirements. Install it first:

```bash
pip3 install claude-agent-sdk
```

**Note:** This will automatically install Claude Code CLI via npm if not present.

### 5. Install Other Dependencies

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend
pip3 install fastapi uvicorn[standard] websockets pydantic pydantic-settings python-multipart python-dotenv orjson
```

### 6. Verify Installation

```bash
python3 -c "import claude_agent_sdk; print('✅ Claude Agent SDK installed successfully')"
```

Expected output:
```
✅ Claude Agent SDK installed successfully
```

### 7. Test Key Manager

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace
python3 -c "from backend.config.key_manager import key_manager; print('✅ Key configured:', key_manager.is_configured())"
```

Expected output:
```
🔑 Using personal API key from config file
✅ Key configured: True
```

### 8. Start the Backend Server

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend
python3 app.py
```

Expected output:
```
🔑 Using personal API key from config file
============================================================
Healthcare Workflow Composer API
============================================================
Starting server on 0.0.0.0:8000
WebSocket endpoint: ws://0.0.0.0:8000/ws/workflow-chat
Health check: http://0.0.0.0:8000/api/health
============================================================
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Troubleshooting

### Issue: "Could not find claude-agent-sdk"

**Solution 1: Install directly from GitHub**
```bash
pip3 install git+https://github.com/anthropics/claude-agent-sdk-python.git
```

**Solution 2: Use alternative package name**
```bash
# Try the older name (deprecated but might work)
pip3 install claude-code-sdk
```

Then update imports in code from `claude_agent_sdk` to `claude_code_sdk`.

### Issue: Node.js not found

**Check if installed:**
```bash
which node
which npm
```

**Install via Homebrew:**
```bash
brew install node
```

**Or download installer:**
https://nodejs.org/en/download/

### Issue: Permission denied

**Use user installation:**
```bash
pip3 install --user claude-agent-sdk
pip3 install --user -r requirements.txt
```

### Issue: Import errors

**Set PYTHONPATH:**
```bash
export PYTHONPATH=/Users/nan.w/Documents/GitHub/patient-chat-workspace:$PYTHONPATH
python3 backend/app.py
```

## Quick Start After Installation

```bash
# Terminal 1: Backend
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend
python3 app.py

# Terminal 2: Frontend
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace
python3 -m http.server 8000

# Open browser
open http://localhost:8000/workflow-composer.html
```

## Next Steps

Once the backend starts successfully:

1. Open `http://localhost:8000/workflow-composer.html`
2. Click "Patient Workflow"
3. Use the AI chat on the right
4. Type: "Create a workflow that sends a message when a lab report is available"
5. Watch blocks appear automatically! ✨

## Need Help?

- See [QUICKSTART.md](../QUICKSTART.md) for full guide
- See [SETUP_API_KEY.md](../SETUP_API_KEY.md) for API key details
- See [API_KEY_SETUP_SUMMARY.md](../API_KEY_SETUP_SUMMARY.md) for quick reference
