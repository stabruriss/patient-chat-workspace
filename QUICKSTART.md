# Quick Start Guide - Claude Agent SDK Integration

Get the AI-powered workflow composer running in 5 minutes!

## Prerequisites

- Python 3.10+
- Node.js (for Claude Agent SDK)
- Claude API Key ([Get one here](https://console.anthropic.com/))

## Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Expected output:
```
Successfully installed claude-agent-sdk-0.1.0 fastapi-0.115.0 ...
```

## Step 2: Configure API Key

**IMPORTANT:** This API key is for your product (separate from Claude Code authentication).

```bash
# Navigate to backend config
cd config

# Copy the API keys template
cp api_keys.json.example api_keys.json

# Edit api_keys.json and add your Claude API key
# Get your key from: https://console.anthropic.com/
```

Your `api_keys.json` should look like:
```json
{
  "claude_agent_sdk": {
    "api_key": "sk-ant-api03-xxxxxxxxxxxxxxxxxxxxx",  ← Your key here
    "model": "claude-sonnet-4-5-20250929"
  },
  "key_source": "personal"
}
```

**Why separate from Claude Code?**
- Claude Code (this AI assistant) uses its own authentication
- Your product (Claude Agent SDK) uses `api_keys.json`
- This keeps development and product authentication separate

See [SETUP_API_KEY.md](SETUP_API_KEY.md) or [API_KEY_SETUP_SUMMARY.md](API_KEY_SETUP_SUMMARY.md) for detailed explanation.

## Step 3: Start the Backend

```bash
cd ..  # Back to backend directory
python app.py
```

You should see:
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

✅ **Backend is ready!**

## Step 4: Start the Frontend

Open a new terminal:

```bash
# From project root
npm run start
```

Or use Python's HTTP server:
```bash
python3 -m http.server 8000
```

## Step 5: Test the Integration

1. **Open workflow composer:**
   - Navigate to: http://localhost:8000/workflow-composer.html

2. **Select workflow type:**
   - Click "Patient Workflow" button

3. **Use AI chat (right side):**
   - Type: `Create a workflow that sends a message when a lab report is available`
   - Press Enter

4. **Watch the magic! ✨**
   - AI streams response in chat
   - Workflow blocks appear on canvas automatically
   - Blocks are connected and configured

## Example Interactions

### Simple Workflow
```
You: "When a lab report is available, send the patient a message"

AI: "I'll create a patient workflow with:
     1. Trigger: Report Available
     2. Action: Send Secure Message

     ✓ Created trigger-report block
     ✓ Created action-send-message block
     ✓ Connected blocks"
```

### Conditional Workflow
```
You: "When a patient responds, check if they need help.
      If yes, create an urgent task. If no, send confirmation."

AI: "I'll create a workflow with conditional logic:
     1. Trigger: Patient Message Received
     2. Condition: Check if patient needs help (AI-evaluated)
     3a. TRUE path: Create Urgent Task
     3b. FALSE path: Send Confirmation

     [Generates and connects blocks]"
```

### Loop Workflow
```
You: "Keep asking the patient about symptoms until they say they're done"

AI: "I'll create a loop workflow:
     1. Trigger: Initial assessment
     2. Loop: AI-controlled
        - Continue: If patient hasn't said "done" or "finished"
        - Break: If patient confirms completion
     3. Inside loop: Send question, wait for response

     [Generates workflow with loop logic]"
```

## Verify Everything Works

### 1. Check Backend Health

```bash
curl http://localhost:8000/api/health
```

Expected:
```json
{
  "status": "healthy",
  "claude_api_configured": true,
  "active_websocket_connections": 1,
  "timestamp": "2025-10-20T12:00:00"
}
```

### 2. Check API Key Configuration

```bash
cd backend
python3 -c "from config.key_manager import key_manager; print('Configured:', key_manager.is_configured())"
```

Expected:
```
🔑 Using personal API key from config file
Configured: True
```

### 3. Check WebSocket Connection

Open browser DevTools (F12) → Console:
```javascript
// Should see:
[WebSocket] Connected to workflow generation service
```

### 4. Test Condition Evaluation

```bash
curl -X POST http://localhost:8000/api/evaluate-condition \
  -H "Content-Type: application/json" \
  -d '{
    "condition_description": "If patient mentions pain",
    "workflow_context": {"patient_message": "I have chest pain"},
    "referenced_block_ids": [],
    "instance_id": "test-001"
  }'
```

Expected:
```json
{
  "decision": "true",
  "reasoning": "Patient mentions chest pain which indicates pain is present",
  "confidence": 0.95,
  "timestamp": "2025-10-20T12:00:00Z"
}
```

## Common Issues & Fixes

### ❌ "AI assistant not connected"

**Problem:** WebSocket connection failed

**Fix:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check browser console for errors
3. Restart backend if needed
4. Page auto-reconnects, or refresh browser

### ❌ "No Claude Agent SDK API key configured"

**Problem:** API keys file not found or key is empty

**Fix:**
```bash
# Check if file exists
ls backend/config/api_keys.json

# If not, copy from example
cd backend/config
cp api_keys.json.example api_keys.json

# Edit and add your key
open api_keys.json
```

### ❌ "Invalid API key format"

**Problem:** Key doesn't start with `sk-ant-api03-` or is incorrectly formatted

**Fix:**
1. Anthropic keys must start with `sk-ant-api03-`
2. No extra spaces or quotes in the JSON file
3. Key should be 50+ characters long

**Check your key format:**
```bash
cd backend
python3 -c "from config.key_manager import key_manager; print(key_manager.validate_key_format(key_manager.get_claude_api_key()))"
# Should print: True
```

### ❌ "401 Unauthorized" when AI responds

**Problem:** API key is invalid or expired

**Fix:**
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Generate a new API key
3. Update `backend/config/api_keys.json`
4. Restart server: `python app.py`

### ❌ "ModuleNotFoundError: No module named 'backend'"

**Problem:** Python can't find the backend module

**Fix:**
```bash
# Run from project root directory
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace
python backend/app.py

# Or set PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
python backend/app.py
```

### ❌ Blocks not appearing on canvas

**Problem:** WebSocket connected but blocks not rendering

**Fix:**
1. Check browser console for JavaScript errors
2. Open DevTools → Network → WS tab to see WebSocket messages
3. Verify messages have `"type": "workflow_block_created"`
4. Check backend logs for errors

## Next Steps

Now that everything is working:

1. **Explore Features:**
   - Try creating complex workflows with conditions
   - Test loop blocks with natural language rules
   - Use @@ syntax to reference blocks

2. **Read Documentation:**
   - [Full Integration Guide](CLAUDE_AGENT_SDK_INTEGRATION.md)
   - [API Key Setup Details](SETUP_API_KEY.md)
   - [Backend API Documentation](backend/README.md)
   - [CLAUDE.md](CLAUDE.md) - Project architecture

3. **Customize:**
   - Add your own custom MCP tools in `backend/tools/`
   - Modify agent prompts in `backend/agents/`
   - Adjust UI in `workflow-composer.html`

## Development Workflow

```bash
# Terminal 1: Backend (auto-reload enabled)
cd backend
python app.py

# Terminal 2: Frontend
npm run start

# Make changes and see them live!
```

## Getting Help

**Backend Issues:**
- Check logs in terminal running `python app.py`
- Test API: `curl http://localhost:8000/docs` (FastAPI interactive docs)
- Review agent responses in terminal

**Frontend Issues:**
- Browser DevTools → Console for errors
- Network tab → WS for WebSocket messages
- Verify workflow blocks array: `console.log(workflowBlocks)`

**Integration Issues:**
- Test WebSocket manually (see verification section)
- Check CORS settings in `backend/config/settings.py`
- Verify port 8000 isn't blocked by firewall

**API Key Issues:**
- See [API_KEY_SETUP_SUMMARY.md](API_KEY_SETUP_SUMMARY.md)
- See [SETUP_API_KEY.md](SETUP_API_KEY.md)

## Resources

- **Claude Agent SDK:** https://docs.claude.com/en/api/agent-sdk/overview
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **WebSocket Guide:** https://developer.mozilla.org/en-US/docs/Web/API/WebSocket

---

**🎉 You're all set! Start building AI-powered healthcare workflows!**

**Remember:** The API key in `api_keys.json` is for your product feature, completely separate from Claude Code authentication.
