# API Key Setup Guide - Separate from Claude Code

## Why Separate Authentication?

You're using **Claude Code** (this AI assistant) for development, and **Claude Agent SDK** as a feature in your product for end users. These need separate API keys to avoid confusion and allow for different key sources.

## Authentication Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Claude Code (Development Tool)                         │
│  - Uses your personal Claude Code authentication        │
│  - Already configured                                   │
│  - NOT used by your application                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Claude Agent SDK (Your Product Feature)                │
│  - Managed via backend/config/api_keys.json             │
│  - Separate from Claude Code                            │
│  - Supports 3 key sources:                              │
│    1. Personal (for development/testing)                │
│    2. Company (for production)                          │
│    3. User-provided (BYOK - Bring Your Own Key)         │
└─────────────────────────────────────────────────────────┘
```

---

## Setup Steps

### Step 1: Get a Claude API Key for Your Product

1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign in (use your Anthropic account)
3. Click **"API Keys"** in the left sidebar
4. Click **"Create Key"**
5. Give it a name like: `"Workflow Composer - Development"`
6. Copy the key (starts with `sk-ant-api03-...`)

**Important:** This is a **different** key than what Claude Code uses.

### Step 2: Create the api_keys.json File

```bash
# Navigate to backend/config
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend/config

# Copy the example file
cp api_keys.json.example api_keys.json
```

### Step 3: Add Your API Key

Open `api_keys.json` in your editor:

```bash
# Using VS Code
code api_keys.json

# Or any editor
open api_keys.json
```

**Edit the file** to add your key:

```json
{
  "comment": "This file stores API keys for the Workflow Composer product",
  "comment2": "This is SEPARATE from Claude Code authentication",

  "claude_agent_sdk": {
    "provider": "anthropic",
    "api_key": "sk-ant-api03-YOUR_ACTUAL_KEY_HERE",  ← Paste your key here
    "model": "claude-sonnet-4-5-20250929",
    "description": "API key for AI-powered workflow generation (end-user feature)"
  },

  "key_source": "personal",

  "usage_limits": {
    "max_requests_per_minute": 60,
    "max_tokens_per_request": 4096,
    "enable_rate_limiting": true
  }
}
```

**Save the file.**

### Step 4: Verify Configuration

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend

# Test that the key is loaded
python3 -c "from config.key_manager import key_manager; print('Status:', key_manager.get_status())"
```

Expected output:
```python
Status: {
  'configured': True,  ← Should be True
  'key_source': 'personal',
  'config_file_exists': True,
  'config_file_path': '/Users/nan.w/.../backend/config/api_keys.json',
  'model': 'claude-sonnet-4-5-20250929',
  'byok_enabled': False,
  'key_format_valid': True  ← Should be True
}
```

### Step 5: Start the Server

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend
python app.py
```

You should see:
```
🔑 Using personal API key from config file
============================================================
Healthcare Workflow Composer API
============================================================
Starting server on 0.0.0.0:8000
```

---

## Key Sources Explained

The system supports **3 different key sources**. Edit `api_keys.json` to configure:

### 1. Personal Key (For Development)

**When to use:** Testing and development

```json
{
  "claude_agent_sdk": {
    "api_key": "sk-ant-api03-YOUR_PERSONAL_KEY"
  },
  "key_source": "personal"  ← Set this
}
```

Console output:
```
🔑 Using personal API key from config file
```

### 2. Company Key (For Production)

**When to use:** Production deployment with company-owned API key

```json
{
  "claude_agent_sdk": {
    "api_key": "sk-ant-api03-YOUR_COMPANY_KEY"
  },
  "key_source": "company"  ← Set this
}
```

Console output:
```
🔑 Using company API key from config file
```

### 3. User-Provided Keys (BYOK - Bring Your Own Key)

**When to use:** Let your end users provide their own Claude API keys

```json
{
  "key_source": "user_provided"  ← Set this
}
```

Then users pass their key via API:

```javascript
// Frontend sends user's API key with WebSocket message
ws.send(JSON.stringify({
  type: 'chat_message',
  message: 'Create a workflow...',
  user_api_key: 'sk-ant-api03-USER_PROVIDED_KEY'  ← User's key
}));
```

Console output:
```
🔑 Using user-provided API key (BYOK)
```

---

## File Structure

```
backend/
└── config/
    ├── api_keys.json.example    # Template file (checked into Git)
    ├── api_keys.json            # Your actual keys (NOT in Git)
    ├── key_manager.py           # Key management logic
    └── settings.py              # App settings (no API keys)
```

**Important:**
- ✅ `api_keys.json.example` is checked into Git (safe, no real keys)
- ❌ `api_keys.json` is in `.gitignore` (NEVER commit this)
- ✅ `.env` file is also in `.gitignore` (for other settings, not AI keys)

---

## Security Best Practices

### ✅ DO:

1. **Keep `api_keys.json` out of Git**
   ```bash
   # Verify it's ignored
   git status backend/config/api_keys.json
   # Should say: "untracked" or not appear
   ```

2. **Use different keys for dev/production**
   - Development: Personal key
   - Production: Company key or BYOK

3. **Rotate keys regularly**
   - Create new keys monthly
   - Revoke old keys after switching

4. **Set usage limits** in `api_keys.json`:
   ```json
   "usage_limits": {
     "max_requests_per_minute": 60,
     "max_tokens_per_request": 4096
   }
   ```

### ❌ DON'T:

1. **Never commit `api_keys.json` to Git**
2. **Never share keys in Slack/email**
3. **Never use production keys in development**
4. **Never hardcode keys in source files**

---

## Troubleshooting

### Problem: "No Claude Agent SDK API key configured"

**Cause:** `api_keys.json` doesn't exist or key is empty

**Fix:**
```bash
# Check if file exists
ls -la backend/config/api_keys.json

# If not, copy from example
cp backend/config/api_keys.json.example backend/config/api_keys.json

# Edit and add your key
code backend/config/api_keys.json
```

### Problem: "Invalid API key format"

**Cause:** Key doesn't start with `sk-ant-` or is too short

**Fix:**
- Anthropic keys must start with `sk-ant-`
- Length should be 50+ characters
- No spaces or quotes around the key in JSON

**Bad:**
```json
"api_key": "  sk-ant-api03-...  "  ← Extra spaces
"api_key": "'sk-ant-api03-...'"  ← Quotes inside string
```

**Good:**
```json
"api_key": "sk-ant-api03-..."  ← Just the key
```

### Problem: "401 Unauthorized" when testing

**Cause:** API key is invalid or expired

**Fix:**
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Generate a new API key
3. Update `api_keys.json`
4. Restart server: `python app.py`

### Problem: Server uses Claude Code's authentication

**Cause:** Old code is still using environment variables

**Fix:**
Check that agents import `key_manager`:

```python
# In backend/agents/*.py - should see:
from backend.config.key_manager import key_manager

# Should NOT see:
from backend.config.settings import settings
api_key = settings.claude_api_key  ← Old way
```

If you see the old way, the files were not updated correctly.

---

## Verifying Separation

Run this test to confirm Claude Code and Claude Agent SDK use different auth:

```bash
cd /Users/nan.w/Documents/GitHub/patient-chat-workspace/backend

# Check which key the product will use
python3 << 'EOF'
from config.key_manager import key_manager

key = key_manager.get_claude_api_key()
if key:
    print(f"✅ Product will use key: {key[:15]}...")
    print(f"   Source: {key_manager.get_key_source()}")
else:
    print("❌ No key configured")
EOF
```

Expected:
```
🔑 Using personal API key from config file
✅ Product will use key: sk-ant-api03-Ab...
   Source: KeySource.PERSONAL
```

---

## Future: Transitioning to Company Key

When ready for production:

### 1. Get Company API Key

Request from your company's Anthropic account

### 2. Update api_keys.json

```json
{
  "claude_agent_sdk": {
    "api_key": "sk-ant-api03-COMPANY_KEY_HERE"
  },
  "key_source": "company"  ← Change this
}
```

### 3. Deploy to Production

The same code works - just different configuration!

---

## Future: Supporting User Keys (BYOK)

To let users provide their own keys:

### 1. Enable BYOK in api_keys.json

```json
{
  "key_source": "user_provided"
}
```

### 2. Update Frontend

Add API key input to UI:

```html
<input type="password" id="userApiKey" placeholder="Your Claude API Key (optional)">
```

### 3. Send with WebSocket

```javascript
const userKey = document.getElementById('userApiKey').value;

ws.send(JSON.stringify({
  type: 'chat_message',
  message: 'Create workflow...',
  user_api_key: userKey  ← Pass user's key
}));
```

The backend already supports this!

---

## Summary

✅ **Claude Code** (development tool) - Uses its own authentication
✅ **Claude Agent SDK** (your product) - Uses `api_keys.json`
✅ **Completely separate** - No conflicts or confusion
✅ **Future-ready** - Supports personal, company, and user-provided keys

**Next step:** [Follow QUICKSTART.md to run the application](QUICKSTART.md)
