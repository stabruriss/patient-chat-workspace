# Healthcare Workflow Composer - Backend

AI-powered workflow generation and runtime evaluation using Claude Agent SDK.

## Overview

This backend provides:
1. **Real-time workflow generation** via WebSocket chat interface
2. **Natural language condition evaluation** at runtime
3. **AI-driven loop control** with natural language rules
4. **Healthcare-specific context understanding** based on your data model

## Architecture

```
backend/
├── app.py                      # FastAPI server with WebSocket support
├── agents/                     # AI agents for different tasks
│   ├── workflow_generator.py  # Chat-to-workflow generation
│   ├── condition_evaluator.py # Runtime condition evaluation
│   └── loop_controller.py      # Loop continue/break decisions
├── tools/                      # Custom MCP tools
│   ├── workflow_tools.py       # Workflow manipulation tools
│   ├── healthcare_tools.py     # Healthcare context tools
│   └── execution_tools.py      # Runtime execution tools
├── models/                     # Data models
│   ├── healthcare_objects.py   # Based on obj-status.md
│   └── workflow_context.py     # Workflow runtime state
└── config/
    └── settings.py             # Configuration management
```

## Prerequisites

- **Python 3.10+**
- **Claude API Key** from [claude.ai/console](https://console.anthropic.com/)
- **Node.js** (for Claude Agent SDK dependencies)

## Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Claude API key:

```env
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-5-20250929
PORT=8000
DEBUG=True
```

### 3. Verify Installation

```bash
python -c "import claude_agent_sdk; print('Claude Agent SDK installed successfully')"
```

## Running the Server

### Development Mode

```bash
cd backend
python app.py
```

The server will start on `http://localhost:8000` with:
- WebSocket endpoint: `ws://localhost:8000/ws/workflow-chat`
- Health check: `http://localhost:8000/api/health`
- API docs: `http://localhost:8000/docs`

### Production Mode

```bash
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### WebSocket

#### `/ws/workflow-chat`

Real-time workflow generation chat.

**Client → Server Messages:**

```json
{
  "type": "chat_message",
  "message": "Create a workflow that sends a message when a lab report is available",
  "workflow_type": "patient",
  "existing_blocks": []
}
```

**Server → Client Messages:**

```json
// Processing started
{"type": "processing_started", "message": "Generating workflow..."}

// Streaming AI response
{"type": "chat_message", "content": "I'll help you create...", "done": false}

// Block created
{"type": "workflow_block_created", "block": {...}, "done": false}

// Generation complete
{"type": "generation_complete", "done": true}

// Error
{"type": "error", "error": "Error message", "done": true}
```

### REST Endpoints

#### `POST /api/evaluate-condition`

Evaluate a condition block at runtime.

**Request:**

```json
{
  "condition_description": "If patient response indicates confusion or distress",
  "workflow_context": {
    "patient_message": "I don't understand what this means",
    "patient_id": "patient-001"
  },
  "referenced_block_ids": ["block-123"],
  "instance_id": "wf-inst-001"
}
```

**Response:**

```json
{
  "decision": "true",
  "reasoning": "Patient message indicates confusion, which matches the condition criteria",
  "confidence": 0.9,
  "timestamp": "2025-10-20T12:00:00Z"
}
```

#### `POST /api/evaluate-loop`

Decide loop continuation at runtime.

**Request:**

```json
{
  "continue_rule": "Continue if patient hasn't confirmed understanding",
  "break_rule": "Break if patient says 'I understand' or 'got it'",
  "escalation_rule": "Escalate if patient seems frustrated",
  "workflow_context": {
    "patient_message": "I got it, thanks"
  },
  "referenced_block_ids": [],
  "iteration_count": 2,
  "instance_id": "wf-inst-001"
}
```

**Response:**

```json
{
  "action": "break",
  "reasoning": "Patient explicitly confirmed understanding with 'I got it'",
  "confidence": 0.95,
  "timestamp": "2025-10-20T12:00:00Z"
}
```

#### `GET /api/block-types?workflow_type=patient`

Get available block types for a workflow type.

**Response:**

```json
{
  "triggers": ["trigger-report", "trigger-order", ...],
  "actions": ["action-send-message", ...],
  "logic": ["condition", "loop", "approval", ...]
}
```

## How It Works

### 1. Workflow Generation Flow

```
User: "Create a workflow that sends a message when a lab report is available"
  ↓
[WebSocket] → workflow_generator agent
  ↓
Agent uses workflow_tools to create blocks:
  - create_workflow_block("trigger-report", {...})
  - create_workflow_block("action-send-message", {...})
  - connect_blocks(trigger_id, action_id)
  ↓
[WebSocket] ← Stream responses to frontend
  ↓
Frontend renders blocks on canvas
```

### 2. Condition Evaluation Flow (Runtime)

```
Workflow execution reaches condition block
  ↓
POST /api/evaluate-condition
  ↓
condition_evaluator agent analyzes:
  - Natural language condition description
  - Current workflow context
  - Referenced block outputs (@@syntax)
  ↓
Returns: {decision: "true"|"false"|"escalate", reasoning: "..."}
  ↓
Workflow execution follows appropriate path
```

### 3. Loop Control Flow (Runtime)

```
Workflow execution in loop
  ↓
POST /api/evaluate-loop
  ↓
loop_controller agent evaluates:
  - continue_rule (natural language)
  - break_rule (natural language)
  - Current iteration context
  ↓
Returns: {action: "continue"|"break"|"escalate", reasoning: "..."}
  ↓
Workflow execution continues or exits loop
```

## Custom MCP Tools

The agents have access to custom tools for:

### Workflow Tools
- `create_workflow_block` - Create new workflow blocks
- `connect_blocks` - Link blocks together
- `validate_workflow_structure` - Check workflow validity
- `suggest_next_blocks` - AI suggestions for next steps

### Healthcare Tools
- `get_patient_status` - Fetch patient healthcare object status
- `get_healthcare_object` - Retrieve specific healthcare objects
- `interpret_healthcare_context` - Understand medical context
- `get_available_healthcare_statuses` - Valid statuses per object type

### Execution Tools
- `parse_block_references` - Extract @@block-id references
- `evaluate_condition` - Provide context for condition decisions
- `decide_loop_action` - Provide context for loop decisions
- `trigger_escalation` - Escalate to human review
- `log_agent_decision` - Audit trail logging

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_API_KEY` | Claude API key (required) | - |
| `CLAUDE_MODEL` | Claude model to use | `claude-sonnet-4-5-20250929` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `DEBUG` | Debug mode | `True` |
| `CORS_ORIGINS` | Allowed CORS origins | `http://localhost:8000,...` |

### Settings Module

See [config/settings.py](config/settings.py) for all configuration options.

## Development

### Adding New Custom Tools

1. Create tool function in `tools/` directory:

```python
from claude_agent_sdk import tool

@tool
async def my_custom_tool(param: str) -> dict:
    """Tool description for the agent"""
    # Implementation
    return {"success": True, "result": "..."}
```

2. Add to MCP server:

```python
from claude_agent_sdk import create_sdk_mcp_server

my_mcp_server = create_sdk_mcp_server(
    "my-tools",
    [my_custom_tool]
)
```

3. Register in agent:

```python
client = ClaudeSDKClient(
    mcp_servers=[my_mcp_server],
    allowed_tools=["mcp__my-tools__*"]
)
```

### Testing

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test condition evaluation
curl -X POST http://localhost:8000/api/evaluate-condition \
  -H "Content-Type: application/json" \
  -d '{
    "condition_description": "If patient mentions pain",
    "workflow_context": {"patient_message": "I have chest pain"},
    "referenced_block_ids": [],
    "instance_id": "test-001"
  }'
```

## Troubleshooting

### WebSocket Connection Issues

**Problem:** Frontend can't connect to WebSocket

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check browser console for connection errors
3. Ensure CORS origins include your frontend URL
4. Try reconnecting - automatic reconnection is built-in

### Claude API Errors

**Problem:** `401 Unauthorized` or API key errors

**Solution:**
1. Verify API key in `.env` file
2. Check API key is valid at [claude.ai/console](https://console.anthropic.com/)
3. Ensure no extra spaces or quotes in `.env`

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'backend'`

**Solution:**
```bash
# Run from project root, not backend directory
cd /path/to/patient-chat-workspace
python -m backend.app
```

Or add to PYTHONPATH:
```bash
export PYTHONPATH=/path/to/patient-chat-workspace:$PYTHONPATH
python backend/app.py
```

## Security Considerations

### HIPAA Compliance

- All agent decisions are logged for audit trails
- Patient data should be encrypted in transit (use HTTPS in production)
- Add database encryption at rest
- Implement proper authentication/authorization
- Regular security audits recommended

### API Key Security

- Never commit `.env` file to version control
- Use secrets management in production (AWS Secrets Manager, etc.)
- Rotate API keys regularly
- Monitor API usage for anomalies

## Next Steps

1. **Add Database** - Replace in-memory storage with PostgreSQL/MongoDB
2. **Add Authentication** - Implement JWT or OAuth2
3. **Production Deployment** - Deploy to AWS/GCP/Azure
4. **Monitoring** - Add Prometheus/Grafana for observability
5. **Testing** - Add unit and integration tests

## Support

For issues or questions:
- Check [Claude Agent SDK docs](https://docs.claude.com/en/api/agent-sdk/overview)
- Review [FastAPI documentation](https://fastapi.tiangolo.com/)
- Check application logs: `tail -f logs/audit.log`
