# Quick Start - Healthcare Workflow Composer

## Your Setup Status

✅ **API Key:** Configured in `backend/config/api_keys.json`
✅ **Node.js:** Installed (v23.11.0)
✅ **Backend Code:** Ready
❌ **Python 3.10+:** Required (you have Python 3.9)

---

## Step 1: Install Python 3.11

```bash
# Install Python 3.11 using Homebrew
brew install python@3.11

# Verify installation
python3.11 --version
```

**Expected output:** `Python 3.11.x`

---

## Step 2: Run Automated Installer

Once Python 3.11 is installed, run:

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace
./install.sh
```

The installer will:
- ✅ Detect Python 3.10+
- ✅ Verify Node.js installation
- ✅ Check your API key configuration
- ✅ Install Claude Agent SDK
- ✅ Install all other dependencies
- ✅ Verify everything works

---

## Step 3: Start the Backend

```bash
cd backend
python3.11 app.py
```

Expected output:
```
🔑 Using personal API key from config file
============================================================
Healthcare Workflow Composer API
============================================================
Starting server on 0.0.0.0:8000
```

---

## Step 4: Start the Frontend

Open a **new terminal** window:

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace
python3 -m http.server 8000
```

---

## Step 5: Open in Browser

Navigate to: **http://localhost:8000/workflow-composer.html**

1. Click **"Patient Workflow"**
2. Use the AI chat on the right
3. Type: `"Create a workflow that sends a message when a lab report is available"`
4. Watch blocks appear automatically! ✨

---

## Troubleshooting

### Can't install Python 3.11?

**Alternative: Use pyenv**
```bash
# Install pyenv
brew install pyenv

# Install Python 3.11
pyenv install 3.11.7

# Use Python 3.11 for this project
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace
pyenv local 3.11.7

# Run installer
./install.sh
```

### Installation script fails?

**Manual installation:**
```bash
cd backend

# Install dependencies with Python 3.11
python3.11 -m pip install claude-agent-sdk
python3.11 -m pip install fastapi uvicorn[standard] websockets pydantic pydantic-settings python-multipart python-dotenv orjson

# Verify
python3.11 -c "import claude_agent_sdk; print('✅ Ready')"
```

### Backend won't start?

**Check PYTHONPATH:**
```bash
export PYTHONPATH=/Users/nan.w/Documents/GitHub/patient-chat-workspace:$PYTHONPATH
python3.11 backend/app.py
```

### API key not working?

**Verify configuration:**
```bash
cd backend
python3.11 -c "from config.key_manager import key_manager; print(key_manager.get_status())"
```

---

## What's Next?

Once everything is running:

### Try These Examples:

**Simple Workflow:**
```
"When a lab report is available, send the patient a message"
```

**Conditional Workflow:**
```
"If patient response indicates confusion, create an urgent task.
Otherwise, send a confirmation message."
```

**Loop Workflow:**
```
"Keep asking the patient about symptoms until they say they're done"
```

### Explore Features:

- 🤖 **AI Workflow Generation** - Natural language → workflow blocks
- 🧠 **Smart Conditions** - AI evaluates conditions at runtime
- 🔄 **Intelligent Loops** - AI-driven loop control
- 📋 **Block References** - Use `@@block-name` syntax

### Read Documentation:

- [QUICKSTART.md](QUICKSTART.md) - Complete quick start guide
- [SETUP_API_KEY.md](SETUP_API_KEY.md) - API key details
- [CLAUDE_AGENT_SDK_INTEGRATION.md](CLAUDE_AGENT_SDK_INTEGRATION.md) - Full integration guide
- [backend/README.md](backend/README.md) - Backend API reference

---

## Summary

```bash
# 1. Install Python 3.11
brew install python@3.11

# 2. Run installer
./install.sh

# 3. Start backend (Terminal 1)
cd backend && python3.11 app.py

# 4. Start frontend (Terminal 2)
python3 -m http.server 8000

# 5. Open browser
open http://localhost:8000/workflow-composer.html
```

**You're all set! 🎉**
