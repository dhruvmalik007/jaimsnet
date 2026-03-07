import os
import subprocess
from rich.console import Console
from pydo import Client
from rich.console import Console

console = Console()

def get_doctl_token() -> str:
    """Attempt to get DO token from environment or doctl config."""
    if "DIGITALOCEAN_TOKEN" in os.environ:
        return os.environ["DIGITALOCEAN_TOKEN"]
    
    # Check doctl config
    config_path = os.path.expanduser("~/Library/Application Support/doctl/config.yaml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                for line in f:
                    if "ldc-account-weown:" in line:
                        parts = line.strip().split("ldc-account-weown:")
                        if len(parts) > 1 and parts[1].strip():
                            return parts[1].strip()
        except Exception:
            pass
            
    return ""

def verify_auth(token: str) -> bool:
    """Verify the token is valid by hitting DO API"""
    if not token:
        return False
        
    try:
        client = Client(token=token)
        client.account.get()
        return True
    except Exception:
        return False
