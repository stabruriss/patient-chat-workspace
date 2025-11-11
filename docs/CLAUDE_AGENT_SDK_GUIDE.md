# Claude Agent SDK in Your Project - Complete Guide

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Healthcare App                       │
│                                                               │
│  Frontend (Browser)                                          │
│  ├── workflow-composer.html                                  │
│  └── WebSocket Client ─────────────────────┐                │
│                                              │                │
└──────────────────────────────────────────────┼────────────────┘
                                               │
                                               │ ws://localhost:8000
                                               ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend (Python FastAPI)                        │
│                                                               │
│  ┌─────────────────────────────────────────────┐            │
│  │  WebSocket Handler (app.py)                 │            │
│  │  - Receives user messages                   │            │
│  │  - Streams responses back                   │            │
│  └──────────────┬──────────────────────────────┘            │
│                 │                                             │
│                 ▼                                             │
│  ┌─────────────────────────────────────────────┐            │
│  │  3 AI Agents                                │            │
│  │  ├── workflow_generator.py                  │            │
│  │  ├── condition_evaluator.py                 │            │
│  │  └── loop_controller.py                     │            │
│  └──────────────┬──────────────────────────────┘            │
│                 │                                             │
│                 ▼                                             │
│  ┌─────────────────────────────────────────────┐            │
│  │  Claude Agent SDK                           │            │
│  │  - query() function                         │            │
│  │  - ClaudeAgentOptions                       │            │
│  │  - Streaming support                        │            │
│  └──────────────┬──────────────────────────────┘            │
│                 │                                             │
└─────────────────┼─────────────────────────────────────────────┘
                  │
                  │ ANTHROPIC_API_KEY (env var)
                  ▼
         ┌────────────────────┐
         │  Anthropic API     │
         │  Claude Sonnet 4.5 │
         └────────────────────┘
```

---

## 🔧 How Claude Agent SDK Works in Your Project

### 1. **API Key Management (Separate from Claude Code)**

**File:** `backend/config/key_manager.py`

```python
# Your app uses a SEPARATE API key from Claude Code
api_key = key_manager.get_claude_api_key()

# Sets it as environment variable
os.environ['ANTHROPIC_API_KEY'] = api_key

# Claude SDK reads from environment automatically
```

**Key Sources (configurable in `backend/config/api_keys.json`):**
- `"personal"` - Your personal API key (development)
- `"company"` - Company API key (production)
- `"user_provided"` - User brings their own key (BYOK)

### 2. **The `query()` Function - Core of SDK**

**How it works:**

```python
from claude_agent_sdk import query, ClaudeAgentOptions

# Stream responses from Claude
async for message in query(
    prompt="User's question here",
    options=ClaudeAgentOptions(
        system_prompt="You are a healthcare expert...",
        model="claude-sonnet-4-5-20250929",
        include_partial_messages=True  # Enables streaming
    )
):
    # Extract text from streamed response
    for block in message.content:
        if hasattr(block, 'text'):
            text = block.text
```

**Key Parameters:**
- `prompt` - User's input/question
- `options` - Configuration object
- Returns async iterator of messages

### 3. **Three Agent Types in Your Project**

#### **A. Workflow Generator Agent** (`workflow_generator.py`)

**Purpose:** Chat interface for describing workflows

**Flow:**
```
User: "Create a workflow that sends a message when a lab report is available"
  ↓
query(
  prompt="Create a workflow...",
  system_prompt="You are a healthcare workflow expert..."
)
  ↓
AI: "I'll help you create a patient workflow with:
     1. Trigger: Report Available
     2. Action: Send Secure Message..."
```

**Streaming:** Yes - streams text to frontend in real-time

**Used by:** WebSocket endpoint `/ws/workflow-chat`

#### **B. Condition Evaluator Agent** (`condition_evaluator.py`)

**Purpose:** Evaluate natural language conditions at runtime

**Flow:**
```
Condition: "If patient response indicates confusion or distress"
Context: {"patient_message": "I'm dizzy and my chest hurts"}
  ↓
query(
  prompt="Evaluate: If patient response indicates confusion..."
)
  ↓
AI Returns JSON: {
  "decision": "true",
  "reasoning": "Patient mentions chest pain - urgent concern",
  "confidence": 0.95
}
```

**Streaming:** No - single response

**Used by:** REST endpoint `POST /api/evaluate-condition`

#### **C. Loop Controller Agent** (`loop_controller.py`)

**Purpose:** Decide loop continuation based on rules

**Flow:**
```
Continue Rule: "Continue if patient hasn't confirmed understanding"
Break Rule: "Break if patient says 'I understand'"
Context: {"patient_message": "I got it, thanks!", "iteration": 3}
  ↓
query(prompt="Evaluate loop...")
  ↓
AI Returns JSON: {
  "action": "break",
  "reasoning": "Patient confirmed understanding",
  "confidence": 0.95
}
```

**Streaming:** No - single response

**Used by:** REST endpoint `POST /api/evaluate-loop`

---

## 🛠️ Development & Tuning Guide

### **1. Tuning System Prompts**

**Location:** Each agent's `_build_system_prompt()` method

**Workflow Generator Example:**

```python
# File: backend/agents/workflow_generator.py

def _build_system_prompt(self, workflow_type: str, existing_blocks):
    return f"""You are a healthcare workflow automation expert.

Current Context:
- Workflow Type: {workflow_type.upper()}

Your capabilities:
1. Understand healthcare terminology
2. Suggest appropriate workflow blocks
3. Explain connections between blocks

Available Block Types:
- Triggers: patient-profile, order, report, encounter-note
- Actions: send-message, create-task, send-email
- Logic: condition, loop, approval

Instructions:
1. When user describes a workflow, break it into steps
2. Describe blocks clearly
3. Explain healthcare rationale
4. Ask clarifying questions if needed

Tone: Professional, concise, healthcare-focused"""
```

**Tuning Tips:**
- Add healthcare-specific examples
- Include do's and don'ts
- Reference your `obj-status.md` data model
- Add domain knowledge (HIPAA, clinical workflows)

### **2. Tuning User Prompts**

**Location:** Each agent's `_build_prompt()` method

**Condition Evaluator Example:**

```python
def _build_evaluation_prompt(self, request):
    return f"""Evaluate this healthcare workflow condition:

Condition Description:
{request.condition_description}

Current Workflow Context:
{json.dumps(request.workflow_context, indent=2)}

Healthcare Object Statuses:
- Order Status: {request.workflow_context.get('order_status')}
- Report Status: {request.workflow_context.get('report_status')}

Patient Safety Considerations:
- If uncertain, choose "escalate"
- If mentions chest pain, urgent symptoms → prioritize safety

Respond with ONLY this JSON format:
{{
    "decision": "true" | "false" | "escalate",
    "reasoning": "Explanation referencing specific context",
    "confidence": 0.0-1.0
}}

Example:
Condition: "If patient mentions pain"
Context: {{"patient_message": "My chest hurts"}}
Response: {{"decision": "true", "reasoning": "Patient explicitly mentions chest pain", "confidence": 0.95}}
"""
```

**Tuning Tips:**
- Include examples in the prompt
- Specify exact JSON format
- Add domain constraints (patient safety)
- Reference specific context fields

### **3. Adjusting Model Parameters**

**Location:** `ClaudeAgentOptions` in each agent

```python
async for message in query(
    prompt=full_prompt,
    options=ClaudeAgentOptions(
        system_prompt=system_prompt,
        model="claude-sonnet-4-5-20250929",  # Model selection
        include_partial_messages=True,        # Streaming
        max_turns=5,                          # Limit conversation
        # Add more options as needed
    )
)
```

**Available Options:**
- `model` - Which Claude model to use
- `include_partial_messages` - Enable streaming
- `max_turns` - Limit conversation length
- `system_prompt` - System instructions
- `allowed_tools` - Tools agent can use (advanced)
- `permission_mode` - Control tool permissions

### **4. Testing & Debugging**

#### **A. Test Individual Agents**

```python
# File: backend/test_agent.py
import asyncio
from agents.workflow_generator import workflow_generator

async def test():
    async for response in workflow_generator.generate_workflow_stream(
        user_message="Create a simple notification workflow",
        workflow_type="patient",
        existing_blocks=[]
    ):
        print(response)

asyncio.run(test())
```

Run:
```bash
PYTHONPATH=. python3.11 backend/test_agent.py
```

#### **B. Test Condition Evaluation**

```bash
curl -X POST http://localhost:8000/api/evaluate-condition \
  -H "Content-Type: application/json" \
  -d '{
    "condition_description": "If patient mentions urgent symptoms",
    "workflow_context": {
      "patient_message": "I have severe chest pain",
      "patient_id": "patient-001"
    },
    "referenced_block_ids": [],
    "instance_id": "test-001"
  }'
```

#### **C. Monitor Backend Logs**

```bash
# Watch the backend output
tail -f /path/to/backend/output.log

# Or check the running process output
# Shows API calls, errors, agent responses
```

#### **D. Browser Console Debugging**

```javascript
// In browser console (F12)

// Check WebSocket connection
console.log(ws.readyState); // 1 = OPEN

// Monitor WebSocket messages
ws.addEventListener('message', (event) => {
    console.log('Received:', JSON.parse(event.data));
});

// Test sending message
ws.send(JSON.stringify({
    type: 'chat_message',
    message: 'Test message',
    workflow_type: 'patient',
    existing_blocks: []
}));
```

### **5. Adding Custom Tools (Advanced)**

**Note:** Current implementation uses simplified `query()`. For full MCP tool support:

```python
# Future enhancement: backend/tools/custom_workflow_tools.py
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool
async def create_workflow_block(block_type: str, config: dict) -> dict:
    """Create a new workflow block"""
    # Your implementation
    return {"success": True, "block_id": "block-123"}

# Create MCP server
workflow_tools = create_sdk_mcp_server(
    "workflow-tools",
    [create_workflow_block]
)

# Use in agent
async for message in query(
    prompt=prompt,
    options=ClaudeAgentOptions(
        mcp_servers={"workflow-tools": workflow_tools},
        allowed_tools=["mcp__workflow-tools__create_workflow_block"]
    )
)
```

---

## 🎯 Common Development Tasks

### **Task 1: Make AI More Healthcare-Specific**

**Edit:** `backend/agents/workflow_generator.py`

```python
def _build_system_prompt(self, workflow_type, existing_blocks):
    base_prompt = """You are a HIPAA-compliant healthcare workflow expert.

Healthcare Domain Knowledge:
- Understand HL7, FHIR standards
- Know common clinical workflows
- Recognize urgent medical terminology
- Respect patient privacy requirements

When creating workflows:
1. Consider patient safety first
2. Ensure HIPAA compliance
3. Include appropriate escalation paths
4. Use healthcare-standard terminology

Available Healthcare Objects (from obj-status.md):
- Patient Profile: created, updated
- Order: created, shipped, payment_complete, lab_shipped
- Report: available, shared
- Encounter Note: shared, updated
... (add all your statuses)
"""
```

### **Task 2: Add Conversation Memory**

**Current:** Each message is independent

**Enhancement:**

```python
# In workflow_generator.py

def _build_prompt(self, user_message, workflow_type, existing_blocks):
    # Include conversation history
    context = ""
    if self.conversation_history:
        context = "Previous conversation:\n"
        for msg in self.conversation_history[-6:]:  # Last 3 exchanges
            role = "User" if msg["role"] == "user" else "AI"
            context += f"{role}: {msg['content']}\n"
        context += "\n"

    return f"""{context}Current request: {user_message}

Remember our previous discussion and build on it."""
```

### **Task 3: Add Validation/Guardrails**

```python
# Add to agents
def _validate_response(self, response_text: str) -> bool:
    """Ensure AI response meets requirements"""

    # Check for prohibited content
    prohibited = ["delete patient", "remove all", "drop database"]
    if any(term in response_text.lower() for term in prohibited):
        return False

    # Check for required healthcare disclaimers
    if "medication" in response_text.lower():
        if "consult physician" not in response_text.lower():
            return False

    return True
```

### **Task 4: Improve JSON Parsing Reliability**

```python
# In condition_evaluator.py

def _parse_decision(self, response_text: str) -> Dict[str, Any]:
    """More robust JSON extraction"""
    try:
        # Try multiple strategies

        # Strategy 1: Find JSON block
        import re
        json_match = re.search(r'\{[^{}]*"decision"[^{}]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())

        # Strategy 2: Extract code block
        code_block = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
        if code_block:
            return json.loads(code_block.group(1))

        # Strategy 3: Use AI to fix JSON
        # ... (advanced: use another AI call to extract/fix JSON)

    except Exception as e:
        print(f"Parse error: {e}")
        return {"decision": "escalate", "reasoning": "Parse failed"}
```

---

## 📊 Performance Tuning

### **1. Optimize Streaming**

```python
# For faster perceived response time
options=ClaudeAgentOptions(
    include_partial_messages=True,  # Stream tokens as they arrive
    model="claude-sonnet-4-5-20250929"  # Faster than Opus
)
```

### **2. Cache System Prompts (Future)**

```python
# Claude SDK supports prompt caching
# Reduces API calls for repeated system prompts
# (Check latest SDK docs for implementation)
```

### **3. Limit Response Length**

```python
system_prompt = """...

Response Guidelines:
- Keep responses under 200 words
- Be concise and direct
- Prioritize actionable information
"""
```

---

## 🔍 Monitoring & Logging

### **Add Comprehensive Logging**

```python
# In each agent
import logging

logger = logging.getLogger(__name__)

async def evaluate_condition(self, request):
    logger.info(f"Evaluating condition: {request.condition_description}")
    logger.debug(f"Context: {request.workflow_context}")

    try:
        result = await self._query_claude(...)
        logger.info(f"Decision: {result.decision}, Confidence: {result.confidence}")
        return result
    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        raise
```

### **Configure Logging**

```python
# backend/app.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backend/logs/app.log'),
        logging.StreamHandler()
    ]
)
```

---

## 🚀 Quick Reference Commands

```bash
# Start development servers
PYTHONPATH=. python3.11 backend/app.py  # Backend
python3 -m http.server 8080              # Frontend

# Test condition evaluation
curl -X POST http://localhost:8000/api/evaluate-condition \
  -H "Content-Type: application/json" \
  -d @test_condition.json

# Test loop evaluation
curl -X POST http://localhost:8000/api/evaluate-loop \
  -H "Content-Type: application/json" \
  -d @test_loop.json

# Check API key configuration
python3.11 -c "from backend.config.key_manager import key_manager; print(key_manager.get_status())"

# View backend logs
tail -f backend/logs/app.log
```

---

## 📚 Key Files for Development

| File | Purpose | Tune This For |
|------|---------|---------------|
| `workflow_generator.py` | Chat interface | Better conversations, workflow suggestions |
| `condition_evaluator.py` | Runtime decisions | More accurate condition logic |
| `loop_controller.py` | Loop control | Better loop termination |
| `key_manager.py` | API key handling | BYOK, company keys |
| `api_keys.json` | Key storage | Switch between key sources |
| `app.py` | API endpoints | Add new endpoints, middleware |

---

## 🎓 Best Practices

1. **Always test prompts in isolation** before integrating
2. **Use specific examples** in system prompts
3. **Add validation** for AI responses
4. **Log everything** for debugging
5. **Handle errors gracefully** - escalate when uncertain
6. **Iterate on prompts** based on real user feedback
7. **Monitor token usage** for cost optimization
8. **Keep system prompts focused** - one responsibility per agent

---

## 📖 Related Documentation

- [QUICKSTA            RT.md](../QUICKSTART.md) - Getting started guide
- [SETUP_API_KEY.md](../SETUP_API_KEY.md) - API key configuration
- [CLAUDE_AGENT_SDK_INTEGRATION.md](../CLAUDE_AGENT_SDK_INTEGRATION.md) - Full integration details
- [backend/README.md](../backend/README.md) - Backend API reference

---

**Your Claude Agent SDK integration is production-ready for development! Focus on tuning the prompts to match your specific healthcare workflows.** 🎉                                    
