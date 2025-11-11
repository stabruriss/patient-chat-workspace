# API Key Setup - Quick Summary

## TL;DR - How to Add Your Key

```bash
# 1. Get API key from https://console.anthropic.com/

# 2. Create the config file
cd backend/config
cp api_keys.json.example api_keys.json

# 3. Edit the file and add your key
open api_keys.json
# Paste your key in the "api_key" field

# 4. Start the server
cd ..
python app.py
```

---

## What's Different from Claude Code?

**Claude Code** (the AI assistant you're using right now):
- Uses its own authentication
- Already configured
- Used for development
- **NOT** used by your application

**Claude Agent SDK** (your product feature):
- Configured via `backend/config/api_keys.json`
- **Separate** from Claude Code
- Used by your end users to generate workflows
- Supports 3 key sources: personal, company, or user-provided (BYOK)

---

## File to Edit

**Location:** `/Users/nan.w/Documents/GitHub/patient-chat-workspace/backend/config/api_keys.json`

**Content:**
```json
{
  "claude_agent_sdk": {
    "api_key": "sk-ant-api03-YOUR_KEY_HERE",  ← Put your key here
    "model": "claude-sonnet-4-5-20250929"
  },
  "key_source": "personal"
}
```

**Important:**
- ✅ No quotes around the key (JSON handles that)
- ✅ No spaces before/after the key
- ✅ Must start with `sk-ant-`
- ❌ This file is git-ignored (never committed)

---

## Quick Test

```bash
cd backend

# Check if configured
python3 -c "from config.key_manager import key_manager; print('Configured:', key_manager.is_configured())"

# Should print:
# 🔑 Using personal API key from config file
# Configured: True
```

---

## Visual Guide

### WRONG ❌

```json
"api_key": ""  ← Empty, won't work
"api_key": " sk-ant-api03-... "  ← Extra spaces
"api_key": "\'sk-ant-api03-...'"  ← Extra quotes
"api_key": "my-claude-code-key"  ← Wrong key type
```

### RIGHT ✅

```json
"api_key": "sk-ant-api03-AbCdEf1234567890..."  ← Clean, starts with sk-ant-
```

---

## Complete Setup Flow

```
1. Get Claude API Key
   ↓
   Go to console.anthropic.com → API Keys → Create Key

2. Copy api_keys.json.example
   ↓
   cp backend/config/api_keys.json.example backend/config/api_keys.json

3. Add Your Key
   ↓
   Edit api_keys.json and paste key in "api_key" field

4. Verify
   ↓
   python3 -c "from config.key_manager import key_manager; print(key_manager.is_configured())"

5. Start Server
   ↓
   python backend/app.py

6. Test in Browser
   ↓
   Open workflow-composer.html → Use chat interface
```

---

## Troubleshooting One-Liners

### "No key configured"
```bash
# Check if file exists
ls backend/config/api_keys.json || echo "File missing - copy from .example"
```

### "Invalid key format"
```bash
# View current key (first 15 chars only)
python3 -c "import json; k=json.load(open('backend/config/api_keys.json')); print(k['claude_agent_sdk']['api_key'][:15])"
# Should show: sk-ant-api03-...
```

### "Still not working"
```bash
# Full diagnostic
cd backend
python3 << 'EOF'
from config.key_manager import key_manager
import json

status = key_manager.get_status()
for key, value in status.items():
    print(f"{key}: {value}")
EOF
```

---

## For Detailed Documentation

- **Full Setup Guide:** [SETUP_API_KEY.md](SETUP_API_KEY.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Integration Guide:** [CLAUDE_AGENT_SDK_INTEGRATION.md](CLAUDE_AGENT_SDK_INTEGRATION.md)

---

## Security Reminder

✅ `api_keys.json` is in `.gitignore` - safe to add keys
✅ Separate from Claude Code authentication
✅ Can use different keys for dev/production
✅ Supports user-provided keys (BYOK) in the future

❌ Never commit `api_keys.json` to Git
❌ Never share keys in Slack/email
❌ Don't use production keys for development

---

**You're all set! The key management system is completely separate from Claude Code.** 🎉
