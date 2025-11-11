# Claude Agent SDK Integration - Healthcare Workflow Composer

## Overview

This project integrates **Claude Agent SDK** into the Healthcare Workflow Composer to enable:

1. **🤖 AI-Powered Workflow Generation** - Natural language chat interface converts descriptions into workflow blocks
2. **🧠 Intelligent Condition Evaluation** - Runtime evaluation of natural language conditions using workflow context
3. **🔄 Smart Loop Control** - AI-driven loop decisions based on natural language rules
4. **📋 @@ Block References** - Reference previous workflow block outputs in natural language

## Quick Start

### 1. Frontend (Workflow Composer)

```bash
# Start the workflow composer
npm run start
# Opens at http://localhost:8000
```

### 2. Backend (AI Agent Server)

```bash
# Setup backend
cd backend
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY

# Start server
python app.py
# Runs at http://localhost:8000 (WebSocket: ws://localhost:8000/ws/workflow-chat)
```

### 3. Test the Integration

1. Open [workflow-composer.html](http://localhost:8000/workflow-composer.html)
2. Click "Patient Workflow" or "Practice Workflow"
3. Use the chat interface on the right:
   - Type: "Create a workflow that sends a message when a lab report is available"
   - Watch as AI generates blocks in real-time
   - Blocks appear on the canvas automatically

## Key Features

### Feature 1: Chat-to-Workflow Generation

**User Experience:**
```
User: "When a lab report becomes available, send the patient a secure message
       and create a task for the provider to review"

AI: [Streaming response]
    "I'll create a patient workflow with:
    1. Trigger: Report Available
    2. Action: Send Secure Message (to patient)
    3. Action: Create Task (assigned to provider)"

    ✓ Created trigger-report block
    ✓ Created action-send-message block
    ✓ Created action-create-task block
    ✓ Connected blocks

[Blocks appear on canvas in real-time]
```

**How It Works:**
- Frontend sends user message via WebSocket
- `workflow_generator` agent parses intent
- Agent uses custom MCP tools to create blocks
- Blocks stream back to frontend
- Canvas updates in real-time

### Feature 2: Natural Language Condition Blocks

**Configuration:**
```javascript
// In condition block modal
Condition Description:
"If patient response indicates confusion, urgent concern, or request for help"
```

**Runtime Evaluation:**
```javascript
// During workflow execution
const result = await fetch('/api/evaluate-condition', {
  method: 'POST',
  body: JSON.stringify({
    condition_description: "If patient response indicates confusion or urgent concern",
    workflow_context: {
      patient_message: "I'm feeling dizzy and my chest hurts",
      patient_id: "patient-001",
      previous_messages: [...]
    },
    referenced_block_ids: ["patient-message-block"],
    instance_id: "wf-inst-123"
  })
});

// Response:
{
  "decision": "true",
  "reasoning": "Patient mentions chest pain which indicates an urgent concern requiring immediate attention",
  "confidence": 0.95
}
```

### Feature 3: AI-Driven Loop Control

**Configuration:**
```javascript
// In loop block modal
Continue Rule:
"Continue if patient hasn't confirmed understanding or has follow-up questions"

Break Rule:
"Break if patient says 'I understand', 'got it', 'thanks' or confirms comprehension"

Escalation Rule:
"Escalate if patient seems frustrated or mentions the same confusion more than twice"
```

**Runtime Evaluation:**
```javascript
// During workflow execution (iteration 3)
const result = await fetch('/api/evaluate-loop', {
  method: 'POST',
  body: JSON.stringify({
    continue_rule: "Continue if patient hasn't confirmed understanding",
    break_rule: "Break if patient says 'I understand' or 'got it'",
    escalation_rule: "Escalate if patient seems frustrated",
    workflow_context: {
      patient_message: "I understand now, thank you!",
      iteration_history: [...]
    },
    iteration_count: 3,
    instance_id: "wf-inst-123"
  })
});

// Response:
{
  "action": "break",
  "reasoning": "Patient explicitly confirmed understanding with 'I understand now'. Break rule is satisfied.",
  "confidence": 0.95
}
```

### Feature 4: @@ Block References

**Usage in Natural Language:**

```javascript
// Condition block description
"If @@patient-response indicates they need clarification about @@lab-results"

// Loop continue rule
"Continue if @@task-status shows incomplete and @@patient-response is pending"
```

**Runtime Processing:**
1. Parser extracts `@@patient-response` and `@@lab-results`
2. System fetches outputs from those blocks
3. Context injected into AI evaluation
4. Decision made with full context

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Browser)                       │
│                                                               │
│  ┌────────────────┐         ┌──────────────────┐            │
│  │ Workflow Canvas│◄────────┤  Chat Interface  │            │
│  │  (Notion-style)│         │   (WebSocket)    │            │
│  └────────────────┘         └──────────────────┘            │
│         ▲                           │                         │
└─────────┼───────────────────────────┼─────────────────────────┘
          │                           │
          │ Render Blocks             │ Send Message
          │                           ▼
┌─────────┴───────────────────────────────────────────────────┐
│                  Backend (Python + FastAPI)                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              WebSocket Handler                        │   │
│  │  - Receives user messages                            │   │
│  │  - Streams AI responses                              │   │
│  │  - Sends generated blocks                            │   │
│  └──────────────────┬───────────────────────────────────┘   │
│                     │                                         │
│  ┌──────────────────▼───────────────────────────────────┐   │
│  │         Workflow Generator Agent                      │   │
│  │  - Powered by Claude Sonnet 4.5                      │   │
│  │  - Uses custom MCP tools                             │   │
│  │  - Streams responses                                 │   │
│  └──────────────────┬───────────────────────────────────┘   │
│                     │                                         │
│  ┌──────────────────▼───────────────────────────────────┐   │
│  │           Custom MCP Tools                            │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ Workflow Tools                              │     │   │
│  │  │  - create_workflow_block                    │     │   │
│  │  │  - connect_blocks                           │     │   │
│  │  │  - validate_workflow_structure              │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ Healthcare Tools                            │     │   │
│  │  │  - get_patient_status                       │     │   │
│  │  │  - get_healthcare_object                    │     │   │
│  │  │  - interpret_healthcare_context             │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  │  ┌─────────────────────────────────────────────┐     │   │
│  │  │ Execution Tools                             │     │   │
│  │  │  - parse_block_references (@@syntax)        │     │   │
│  │  │  - evaluate_condition                       │     │   │
│  │  │  - decide_loop_action                       │     │   │
│  │  └─────────────────────────────────────────────┘     │   │
│  └───────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │     Runtime Evaluation Agents (REST API)             │   │
│  │                                                       │   │
│  │  ┌───────────────────────────────────────────┐      │   │
│  │  │  Condition Evaluator                      │      │   │
│  │  │  POST /api/evaluate-condition             │      │   │
│  │  │  - Evaluates natural language conditions  │      │   │
│  │  │  - Returns true/false/escalate            │      │   │
│  │  └───────────────────────────────────────────┘      │   │
│  │                                                       │   │
│  │  ┌───────────────────────────────────────────┐      │   │
│  │  │  Loop Controller                          │      │   │
│  │  │  POST /api/evaluate-loop                  │      │   │
│  │  │  - Decides continue/break/escalate        │      │   │
│  │  │  - Prevents infinite loops                │      │   │
│  │  └───────────────────────────────────────────┘      │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
```

## Implementation Details

### WebSocket Communication Protocol

**Message Types (Client → Server):**
```json
{
  "type": "chat_message",
  "message": "User's natural language request",
  "workflow_type": "patient" | "practice",
  "existing_blocks": [...]
}

{
  "type": "reset_conversation"
}

{
  "type": "ping"
}
```

**Message Types (Server → Client):**
```json
{"type": "processing_started", "message": "..."}
{"type": "chat_message", "content": "...", "done": false}
{"type": "workflow_block_created", "block": {...}, "done": false}
{"type": "generation_complete", "done": true}
{"type": "error", "error": "...", "done": true}
{"type": "pong", "timestamp": "..."}
```

### Data Models

**Workflow Block Structure:**
```javascript
{
  "id": "block-abc123",
  "type": "condition",
  "data": {
    "prompt": "If patient response indicates confusion",
    "configured": true
  },
  "parentIds": ["block-xyz789"],
  "childIds": [],
  "supportsMultipleInputs": true,
  "children": {
    "paths": []
  }
}
```

**Healthcare Object Structure (from obj-status.md):**
```python
{
  "object_id": "report-001",
  "object_type": "report",
  "patient_id": "patient-001",
  "current_status": "report_available",
  "status_history": [
    {"status": "report_available", "timestamp": "2025-01-18T09:00:00Z"}
  ]
}
```

## Configuration

### Frontend Configuration

Edit [workflow-composer.html](workflow-composer.html#L1373):

```javascript
const WS_URL = 'ws://localhost:8000/ws/workflow-chat';  // WebSocket URL
```

### Backend Configuration

Edit [backend/.env](backend/.env.example):

```env
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-5-20250929
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:8000,http://localhost:8080
```

## Examples

### Example 1: Simple Patient Notification

**User Input:**
```
"When a lab report is available, send the patient a secure message"
```

**Generated Workflow:**
```
┌─────────────────────┐
│  Trigger: Report    │
│     Available       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Action: Send       │
│  Secure Message     │
│  (to: patient)      │
└─────────────────────┘
```

### Example 2: Conditional Workflow with AI Decision

**User Input:**
```
"When a patient responds to a message, check if they need help.
If they do, create an urgent task. If not, send a confirmation."
```

**Generated Workflow:**
```
┌─────────────────────┐
│  Trigger: Patient   │
│  Message Received   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Condition: "If     │
│  patient needs      │
│  help"              │ ◄── AI evaluates this at runtime
└──────┬──────────────┘
       │
       ├─ TRUE ──► ┌──────────────────┐
       │           │ Action: Create    │
       │           │ Urgent Task       │
       │           └──────────────────┘
       │
       └─ FALSE ─► ┌──────────────────┐
                   │ Action: Send      │
                   │ Confirmation      │
                   └──────────────────┘
```

**Runtime Condition Evaluation:**
```json
// Patient message: "I'm confused about the instructions"
// AI Decision:
{
  "decision": "true",
  "reasoning": "Patient explicitly states confusion, indicating need for help"
}

// Patient message: "Thanks, all clear!"
// AI Decision:
{
  "decision": "false",
  "reasoning": "Patient confirms understanding, no help needed"
}
```

### Example 3: Smart Loop with AI Control

**User Input:**
```
"Keep asking the patient if they understand the care instructions
until they confirm understanding"
```

**Generated Workflow:**
```
┌─────────────────────┐
│  Trigger: Care      │
│  Instructions Sent  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Loop: AI-driven    │
│                     │
│  Continue: "If      │◄── AI decides each iteration
│  patient hasn't     │
│  confirmed"         │
│                     │
│  Break: "If patient │
│  says 'understand'" │
└──────────┬──────────┘
           │
           ▼
      ┌────────────┐
      │  Send      │
      │  Message:  │
      │  "Do you   │
      │  understand?"
      └────────────┘
           │
           ▼
      ┌────────────┐
      │  Wait for  │
      │  Response  │
      └────────────┘
```

**Runtime Loop Evaluation:**
```json
// Iteration 1: Patient: "What does that mean?"
{
  "action": "continue",
  "reasoning": "Patient asks clarifying question, hasn't confirmed understanding"
}

// Iteration 2: Patient: "Still not clear"
{
  "action": "continue",
  "reasoning": "Patient explicitly states lack of understanding"
}

// Iteration 3: Patient: "Got it, thanks!"
{
  "action": "break",
  "reasoning": "Patient confirms understanding with 'Got it'"
}
```

## Testing

### Test WebSocket Connection

```javascript
// Browser console
const ws = new WebSocket('ws://localhost:8000/ws/workflow-chat');
ws.onopen = () => console.log('Connected');
ws.onmessage = (e) => console.log('Message:', JSON.parse(e.data));
ws.send(JSON.stringify({
  type: 'chat_message',
  message: 'Create a simple workflow',
  workflow_type: 'patient',
  existing_blocks: []
}));
```

### Test Condition Evaluation

```bash
curl -X POST http://localhost:8000/api/evaluate-condition \
  -H "Content-Type: application/json" \
  -d '{
    "condition_description": "If patient mentions pain",
    "workflow_context": {
      "patient_message": "I have a headache"
    },
    "referenced_block_ids": [],
    "instance_id": "test-123"
  }'
```

### Test Loop Control

```bash
curl -X POST http://localhost:8000/api/evaluate-loop \
  -H "Content-Type: application/json" \
  -d '{
    "continue_rule": "Continue if no confirmation",
    "break_rule": "Break if patient confirms",
    "workflow_context": {
      "patient_message": "Yes, I understand"
    },
    "iteration_count": 2,
    "instance_id": "test-123"
  }'
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in backend/.env
- [ ] Use HTTPS for WebSocket (wss://)
- [ ] Configure proper CORS origins
- [ ] Add authentication/authorization
- [ ] Set up database (PostgreSQL/MongoDB)
- [ ] Configure logging and monitoring
- [ ] Set up secrets management
- [ ] Enable rate limiting
- [ ] Configure backup strategy
- [ ] Set up error alerting

### Docker Deployment (Optional)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
    volumes:
      - ./backend:/app
```

## Troubleshooting

### Issue: WebSocket won't connect

**Symptoms:** Frontend shows "AI assistant not connected"

**Solutions:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check browser console for CORS errors
3. Ensure WebSocket URL is correct in workflow-composer.html
4. Check firewall isn't blocking port 8000

### Issue: Agent not generating workflow blocks

**Symptoms:** Chat works but no blocks appear

**Solutions:**
1. Check Claude API key is valid
2. Review backend logs for errors: `tail -f backend/logs/*.log`
3. Verify agent has access to workflow tools
4. Check console for JavaScript errors

### Issue: Condition evaluation returns "escalate" always

**Symptoms:** All conditions escalate to human review

**Solutions:**
1. Make condition descriptions more specific
2. Provide more context in workflow_context
3. Check if Claude API is responding slowly
4. Review agent logs for reasoning

## Roadmap

### Phase 1: Core Features ✅
- [x] WebSocket chat interface
- [x] Workflow generation from natural language
- [x] Condition evaluation with natural language
- [x] Loop control with AI decisions
- [x] @@ block reference parsing

### Phase 2: Enhancements (Next)
- [ ] Workflow templates in AI chat
- [ ] Visual diff preview before applying changes
- [ ] Multi-turn conversation context
- [ ] Workflow versioning
- [ ] Undo/redo for AI changes

### Phase 3: Advanced Features (Future)
- [ ] Multi-agent collaboration
- [ ] Real-time workflow simulation
- [ ] AI-suggested optimizations
- [ ] Natural language workflow queries
- [ ] Voice input for workflow generation

## Resources

- [Claude Agent SDK Documentation](https://docs.claude.com/en/api/agent-sdk/overview)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [WebSocket Protocol](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [Backend README](backend/README.md)

## License

[Your License Here]

## Contributors

[Your Name/Team]

---

**Built with ❤️ using Claude Agent SDK**
