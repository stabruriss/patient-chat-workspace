"""
Logging configuration for Claude Agent SDK integration
Logs all agent interactions, tool calls, and errors for debugging
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import json


def setup_logging(log_level=logging.DEBUG):
    """
    Configure comprehensive logging for the application

    Creates two log files:
    - logs/app.log: All logs (DEBUG and above)
    - logs/agent_interactions.log: Structured JSON logs of agent calls and tool usage
    """

    # Create logs directory
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    # Main application log
    app_log = log_dir / "app.log"
    agent_log = log_dir / "agent_interactions.log"

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers
    root_logger.handlers = []

    # Console handler (INFO and above)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)

    # File handler for all logs (DEBUG and above)
    file_handler = logging.FileHandler(app_log)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(file_handler)

    # Suppress noisy third-party loggers
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('websockets').setLevel(logging.INFO)

    logging.info(f"Logging initialized - App log: {app_log}")
    logging.info(f"Agent interaction log: {agent_log}")

    return str(agent_log)


class AgentInteractionLogger:
    """Structured logger for agent interactions and tool calls"""

    def __init__(self, log_file: str):
        self.log_file = Path(log_file)
        self.logger = logging.getLogger("agent_interactions")

    def log_interaction(self, interaction_type: str, data: dict):
        """
        Log an agent interaction as structured JSON

        Args:
            interaction_type: Type of interaction (agent_call, tool_call, error, etc.)
            data: Dictionary of interaction data
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": interaction_type,
            **data
        }

        # Write to JSON log file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

        # Also log to standard logger
        self.logger.info(f"{interaction_type}: {json.dumps(data, indent=2)}")

    def log_agent_call(self, agent_name: str, prompt: str, options: dict):
        """Log an agent query call"""
        self.log_interaction("agent_call", {
            "agent": agent_name,
            "prompt_length": len(prompt),
            "prompt_preview": prompt[:200] + "..." if len(prompt) > 200 else prompt,
            "options": options
        })

    def log_agent_response(self, agent_name: str, response: str, token_count: int = None):
        """Log an agent response"""
        self.log_interaction("agent_response", {
            "agent": agent_name,
            "response_length": len(response),
            "response_preview": response[:200] + "..." if len(response) > 200 else response,
            "token_count": token_count
        })

    def log_tool_call(self, tool_name: str, parameters: dict, result: dict):
        """Log a tool call and its result"""
        self.log_interaction("tool_call", {
            "tool": tool_name,
            "parameters": parameters,
            "result": result
        })

    def log_error(self, error_type: str, error_message: str, context: dict = None):
        """Log an error with context"""
        self.log_interaction("error", {
            "error_type": error_type,
            "error_message": error_message,
            "context": context or {}
        })

    def log_websocket_message(self, direction: str, message_type: str, data: dict):
        """Log WebSocket messages"""
        self.log_interaction("websocket", {
            "direction": direction,  # "sent" or "received"
            "message_type": message_type,
            "data": data
        })


# Global instance
_agent_logger = None


def get_agent_logger() -> AgentInteractionLogger:
    """Get the global agent interaction logger"""
    global _agent_logger
    if _agent_logger is None:
        log_dir = Path(__file__).parent.parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)
        agent_log = log_dir / "agent_interactions.log"
        _agent_logger = AgentInteractionLogger(str(agent_log))
    return _agent_logger
