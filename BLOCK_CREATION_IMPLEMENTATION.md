# Block Creation from Chat - Implementation Summary

## What Was Implemented

The AI agent can now **create visual workflow blocks on the canvas** as it chats with you, instead of just describing them in text.

## Architecture

### 1. **Backend: MCP Tool for Block Creation**
**File:** `backend/tools/workflow_canvas_tool.py`

The `WorkflowCanvasTool` class provides two methods:
- `create_block()` - Create a single workflow block
- `create_multiple_blocks()` - Create multiple blocks at once

**Supported Block Types:**
- `send-message` - SMS/email/in-app messages
- `appointment` - Schedule appointments
- `task` - Assign tasks to team members
- `document` - Share documents
- `order` - Lab/medication orders
- `note` - Internal notes
- `wait` - Time or event-based waits
- `condition` - IF/THEN branching with AI evaluation
- `loop` - Repeating blocks with AI control
- `smart-review` - Human review with AI pre-analysis
- `ai-touch` - Automated AI decision-making

### 2. **Backend: Updated Workflow Generator Agent**
**File:** `backend/agents/workflow_generator.py`

**Key Changes:**
- Imports the `WorkflowCanvasTool` and tool descriptors
- Passes tools to Claude Agent SDK via `tools` parameter in `ClaudeAgentOptions`
- Handles `tool_use` content blocks from the AI response
- Executes tools and sends `block_created` messages to frontend
- Updated system prompt to instruct AI to **USE TOOLS** instead of just describing

**Critical Prompt Instructions:**
```
CRITICAL INSTRUCTIONS:
1. **USE TOOLS TO CREATE BLOCKS** - Don't just describe workflows, actually CREATE them!
2. As you explain each step, immediately create the corresponding block
3. Keep explanations BRIEF - focus on creating blocks, not writing essays
```

### 3. **Backend: Comprehensive Logging**
**File:** `backend/config/logging_config.py`

**Log Files Created:**
- `logs/app.log` - All application logs (DEBUG level)
- `logs/agent_interactions.log` - Structured JSON logs of agent calls, tool usage, errors

**What Gets Logged:**
- Every agent call with prompts and options
- Tool calls with parameters and results
- Agent responses with token counts
- WebSocket messages
- Errors with full context

### 4. **Frontend: Block Creation Handler**
**File:** `workflow-composer.html` (lines 1439-1448)

**Changes:**
- Updated WebSocket message handler to listen for `block_created` messages
- Added `addBlockToCanvas()` function that converts agent block format to frontend format
- Automatically renders workflow after each block is created
- Shows system message: `✓ Created {block_type} block`

**Block Conversion Logic:**
- Generates unique block IDs
- Calculates positions (stacks vertically)
- Converts agent config format to frontend data structure
- Handles `insertAfter` for precise placement
- Marks blocks as `configured: true` so they render properly

## How It Works

### Flow Diagram
```
User types: "Send them a reminder"
    ↓
Frontend → WebSocket → Backend
    ↓
workflow_generator agent receives message
    ↓
Claude Agent SDK query() with TOOLS enabled
    ↓
AI decides: "I should create a send-message block"
    ↓
AI calls: create_workflow_block(type='send-message', config={...})
    ↓
WorkflowCanvasTool.create_block() executes
    ↓
Returns: {success: true, block: {...}}
    ↓
Agent yields: {type: 'block_created', block: {...}}
    ↓
WebSocket → Frontend
    ↓
addBlockToCanvas() converts and adds block
    ↓
renderWorkflow() displays block on canvas
```

## Testing the Feature

### 1. **Start Servers**
```bash
# Frontend (if not already running)
python3 -m http.server 8080

# Backend (already running on port 8000)
PYTHONPATH=. python3.11 backend/app.py
```

### 2. **Open Application**
Navigate to: http://localhost:8080/workflow-composer.html

### 3. **Test Examples**

**Example 1: Simple Message Block**
```
User: "Send the patient a reminder about their appointment tomorrow"
Expected: AI creates a send-message block with reminder content
```

**Example 2: Multi-Step Workflow**
```
User: "Send them a reminder, wait 24 hours, then if they haven't responded, assign a task to the nurse"
Expected: AI creates 4 blocks: send-message, wait, condition, task
```

**Example 3: Smart Review**
```
User: "Have the AI review the patient's response and escalate to a doctor if needed"
Expected: AI creates a smart-review block with AI analysis enabled
```

## Debugging

### View Logs in Real-Time
```bash
# Watch application logs
tail -f logs/app.log

# Watch agent interactions (structured JSON)
tail -f logs/agent_interactions.log
```

### Log Entries to Look For

**Successful Tool Call:**
```json
{
  "timestamp": "2025-10-29T19:10:00.000Z",
  "type": "tool_call",
  "tool": "create_workflow_block",
  "parameters": {"block_type": "send-message", "config": {...}},
  "result": {"success": true, "block": {...}}
}
```

**Agent Call:**
```json
{
  "timestamp": "2025-10-29T19:10:00.000Z",
  "type": "agent_call",
  "agent": "workflow_generator",
  "prompt_preview": "User: Send them a reminder...",
  "options": {"workflow_type": "patient"}
}
```

**Error:**
```json
{
  "timestamp": "2025-10-29T19:10:00.000Z",
  "type": "error",
  "error_type": "tool_execution_error",
  "error_message": "Invalid block type",
  "context": {...}
}
```

### Common Issues

**Issue: AI describes blocks but doesn't create them**
- **Cause:** System prompt not strong enough
- **Fix:** Update system prompt in `workflow_generator.py` line 210-245
- **Check:** Look for "tool_call" entries in `logs/agent_interactions.log`

**Issue: Blocks not appearing on canvas**
- **Cause:** Frontend not receiving `block_created` messages
- **Fix:** Check browser console (F12) for WebSocket messages
- **Check:** Look for `[WebSocket] Received:` with type `block_created`

**Issue: Block format errors**
- **Cause:** Agent config doesn't match frontend expectations
- **Fix:** Update `addBlockToCanvas()` conversion logic in workflow-composer.html:1493-1541
- **Check:** Console log shows "Adding block from agent:" with proper structure

## Next Steps

### Potential Enhancements

1. **Multi-Step Agent Approach**
   - Separate planning agent and building agent
   - Get user approval before creating blocks
   - See docs/CLAUDE_AGENT_SDK_GUIDE.md for details

2. **Improved Block Positioning**
   - Use flowchart layout algorithm
   - Support branching conditions visually
   - Auto-connect blocks

3. **Block Configuration UI**
   - Show inline editor for created blocks
   - Allow quick edits from chat
   - Confirm block details before adding

4. **Conversation Memory**
   - Remember block IDs for modifications
   - Support "change the last block to X"
   - Track workflow state across conversation

## Files Modified

### New Files
- `backend/tools/workflow_canvas_tool.py` - MCP tool implementation
- `backend/config/logging_config.py` - Logging configuration
- `logs/app.log` - Application logs (git-ignored)
- `logs/agent_interactions.log` - Agent interaction logs (git-ignored)

### Modified Files
- `backend/agents/workflow_generator.py` - Added tool support
- `backend/tools/__init__.py` - Updated imports
- `backend/app.py` - Added logging initialization
- `workflow-composer.html` - Updated WebSocket handler and block creation logic

## Configuration

No additional configuration needed! The system uses existing:
- `backend/config/api_keys.json` - Claude API key
- `backend/config/settings.py` - Server settings

## Success Criteria

✅ AI can create blocks via tool calls
✅ Blocks appear on canvas in real-time
✅ System messages confirm block creation
✅ Logs capture all tool calls and results
✅ Frontend renders blocks correctly
✅ Conversation continues after block creation

## Status

**READY FOR TESTING** - All components implemented and backend running.

Try it now at: http://localhost:8080/workflow-composer.html
