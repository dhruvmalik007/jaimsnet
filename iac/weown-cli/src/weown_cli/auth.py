import os
import subprocess
from typing import Optional
from rich.console import Console
from pydo import Client
from rich.console import Console

import json
from pathlib import Path

console = Console()

CREDENTIALS_FILE = Path("~/.weown-cli/credentials.json").expanduser()

def get_local_token() -> Optional[str]:
    """Retrieve the DO token from the local credentials file."""
    if CREDENTIALS_FILE.exists():
        try:
            data = json.loads(CREDENTIALS_FILE.read_text())
            return data.get("do_token")
        except json.JSONDecodeError:
            pass
    return None

def save_local_token(token: str):
    """Save the DO token to the local credentials file securely."""
    CREDENTIALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_FILE.write_text(json.dumps({"do_token": token}))
    CREDENTIALS_FILE.chmod(0o600)  # User read/write only

def delete_local_token():
    """Delete the local credentials file."""
    if CREDENTIALS_FILE.exists():
        CREDENTIALS_FILE.unlink()

def get_token() -> str:
    """Attempt to get DO token from local storage, then environment, then doctl config."""
    local_token = get_local_token()
    if local_token:
        return local_token

    if "DIGITALOCEAN_TOKEN" in os.environ:
        return os.environ["DIGITALOCEAN_TOKEN"]
    
    # Check doctl config as fallback
    config_path = os.path.expanduser("~/Library/Application Support/doctl/config.yaml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                for line in f:
                    # Check for generic access-token or context-specific tokens
                    if "access-token:" in line:
                        parts = line.strip().split(":")
                        if len(parts) > 1:
                            token = parts[1].strip()
                            if token:
                                return token
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

def get_infisical_client() -> Optional[object]:
    """
    Initialize Infisical SDK with Machine Identity.
    Requires INFISICAL_CLIENT_ID and INFISICAL_CLIENT_SECRET env vars.
    """
    client_id = os.environ.get("INFISICAL_CLIENT_ID")
    client_secret = os.environ.get("INFISICAL_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        return None
        
    try:
        from infisical_sdk import InfisicalSDKClient
        
        client = InfisicalSDKClient(
            host="https://app.infisical.com",
            cache_ttl=300
        )
        
        client.auth.universal_auth.login(
            client_id=client_id,
            client_secret=client_secret
        )
        return client
    except Exception as e:
        console.print(f"[yellow]Failed to authenticate with Infisical: {e}[/yellow]")
        return None
