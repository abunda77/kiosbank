#!/usr/bin/env python3
"""
Environment Configuration Loader
Loads configuration from .env file
"""

import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: Optional[str] = None) -> dict:
    """
    Load environment variables from .env file
    
    Args:
        env_path: Path to .env file. If None, looks for .env in current directory
        
    Returns:
        Dictionary of environment variables
    """
    if env_path is None:
        # Look for .env in project root (parent of app folder)
        env_path = Path(__file__).parent.parent / '.env'
    else:
        env_path = Path(env_path)
    
    if not env_path.exists():
        raise FileNotFoundError(
            f"❌ .env file not found at: {env_path}\n"
            f"Please copy .env.example to .env and fill in your credentials:\n"
            f"  cp .env.example .env\n"
            f"  # Then edit .env with your actual values"
        )
    
    env_vars = {}
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                env_vars[key] = value
                # Also set in os.environ for compatibility
                os.environ[key] = value
    
    return env_vars


def get_env(key: str, default: Optional[str] = None, required: bool = False) -> str:
    """
    Get environment variable value
    
    Args:
        key: Environment variable name
        default: Default value if not found
        required: If True, raises error if not found
        
    Returns:
        Environment variable value
    """
    value = os.environ.get(key, default)
    
    if required and value is None:
        raise ValueError(
            f"❌ Required environment variable '{key}' not found!\n"
            f"Please set it in your .env file."
        )
    
    return value


def get_env_bool(key: str, default: bool = False) -> bool:
    """
    Get environment variable as boolean
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Boolean value
    """
    value = os.environ.get(key, str(default))
    return value.lower() in ('true', '1', 'yes', 'on')


def get_env_int(key: str, default: int = 0) -> int:
    """
    Get environment variable as integer
    
    Args:
        key: Environment variable name
        default: Default value if not found
        
    Returns:
        Integer value
    """
    value = os.environ.get(key, str(default))
    try:
        return int(value)
    except ValueError:
        return default


# Auto-load .env when module is imported
try:
    load_env_file()
except FileNotFoundError as e:
    print(f"⚠️  Warning: {e}")
