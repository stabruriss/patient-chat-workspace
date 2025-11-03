"""
API Key Manager for Workflow Composer
Handles API keys separately from Claude Code authentication

Supports three key sources:
1. Personal keys (stored in api_keys.json)
2. Company keys (stored in api_keys.json, for production)
3. User-provided keys (passed at runtime by end users - BYOK)
"""
import json
import os
from typing import Optional, Dict, Any
from pathlib import Path
from enum import Enum


class KeySource(str, Enum):
    PERSONAL = "personal"
    COMPANY = "company"
    USER_PROVIDED = "user_provided"


class APIKeyManager:
    """Manages API keys for Claude Agent SDK (separate from Claude Code)"""

    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.keys_file = self.config_dir / "api_keys.json"
        self.keys_example_file = self.config_dir / "api_keys.json.example"
        self._keys_config: Optional[Dict[str, Any]] = None
        self._user_provided_key: Optional[str] = None

    def _load_keys_config(self) -> Dict[str, Any]:
        """Load API keys configuration from file"""
        if self._keys_config is not None:
            return self._keys_config

        if not self.keys_file.exists():
            print(f"⚠️  API keys file not found: {self.keys_file}")
            print(f"📝 Copy {self.keys_example_file.name} to {self.keys_file.name}")
            print(f"   and add your Claude Agent SDK API key (separate from Claude Code)")
            return self._get_default_config()

        try:
            with open(self.keys_file, 'r') as f:
                self._keys_config = json.load(f)
                return self._keys_config
        except Exception as e:
            print(f"❌ Error loading API keys: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration when file doesn't exist"""
        return {
            "claude_agent_sdk": {
                "api_key": "",
                "model": "claude-sonnet-4-5-20250929"
            },
            "key_source": "personal"
        }

    def get_claude_api_key(self, user_provided_key: Optional[str] = None) -> Optional[str]:
        """
        Get Claude API key based on configured source

        Priority order:
        1. User-provided key (if BYOK is enabled)
        2. Company key (if configured)
        3. Personal key (default)

        Args:
            user_provided_key: Optional API key provided by end user (BYOK)

        Returns:
            API key string or None if not configured
        """
        config = self._load_keys_config()
        key_source = config.get("key_source", "personal")

        # Priority 1: User-provided key (BYOK)
        if user_provided_key:
            print("🔑 Using user-provided API key (BYOK)")
            return user_provided_key

        # Priority 2: Check key source from config
        if key_source == "user_provided":
            print("⚠️  Key source is 'user_provided' but no key was provided")
            return None

        # Priority 3: Company or personal key from config file
        claude_config = config.get("claude_agent_sdk", {})
        api_key = claude_config.get("api_key", "")

        if not api_key:
            print("⚠️  No Claude Agent SDK API key configured")
            print(f"📝 Add your key to: {self.keys_file}")
            print("   This is SEPARATE from your Claude Code authentication")
            return None

        source_label = "company" if key_source == "company" else "personal"
        print(f"🔑 Using {source_label} API key from config file")
        return api_key

    def get_claude_model(self) -> str:
        """Get configured Claude model"""
        config = self._load_keys_config()
        return config.get("claude_agent_sdk", {}).get("model", "claude-sonnet-4-5-20250929")

    def set_user_provided_key(self, api_key: str):
        """
        Set a user-provided API key for the current session (BYOK)
        This is stored in memory only, not persisted to disk

        Args:
            api_key: The user's API key
        """
        self._user_provided_key = api_key
        print("🔑 User-provided API key set for this session")

    def get_key_source(self) -> KeySource:
        """Get the configured key source"""
        config = self._load_keys_config()
        source = config.get("key_source", "personal")
        return KeySource(source)

    def validate_key_format(self, api_key: str) -> bool:
        """
        Validate that an API key has the correct format

        Args:
            api_key: API key to validate

        Returns:
            True if format is valid, False otherwise
        """
        if not api_key:
            return False

        # Anthropic keys start with 'sk-ant-'
        if not api_key.startswith('sk-ant-'):
            print(f"⚠️  Invalid API key format. Anthropic keys should start with 'sk-ant-'")
            return False

        # Basic length check (Anthropic keys are typically quite long)
        if len(api_key) < 50:
            print(f"⚠️  API key seems too short")
            return False

        return True

    def get_usage_limits(self) -> Dict[str, Any]:
        """Get configured usage limits"""
        config = self._load_keys_config()
        return config.get("usage_limits", {
            "max_requests_per_minute": 60,
            "max_tokens_per_request": 4096,
            "enable_rate_limiting": True
        })

    def is_configured(self) -> bool:
        """Check if API key is configured and valid"""
        api_key = self.get_claude_api_key()
        return api_key is not None and self.validate_key_format(api_key)

    def get_status(self) -> Dict[str, Any]:
        """Get status of API key configuration"""
        config = self._load_keys_config()
        api_key = config.get("claude_agent_sdk", {}).get("api_key", "")

        return {
            "configured": bool(api_key),
            "key_source": config.get("key_source", "personal"),
            "config_file_exists": self.keys_file.exists(),
            "config_file_path": str(self.keys_file),
            "model": self.get_claude_model(),
            "byok_enabled": config.get("key_source") == "user_provided",
            "key_format_valid": self.validate_key_format(api_key) if api_key else False
        }


# Global instance
key_manager = APIKeyManager()


# Convenience functions
def get_api_key(user_provided_key: Optional[str] = None) -> Optional[str]:
    """Get Claude API key (convenience function)"""
    return key_manager.get_claude_api_key(user_provided_key)


def get_model() -> str:
    """Get Claude model (convenience function)"""
    return key_manager.get_claude_model()


def is_configured() -> bool:
    """Check if API key is configured (convenience function)"""
    return key_manager.is_configured()
