import typer
from typing import Optional
import questionary
import json
import os
import subprocess
import hashlib
from pathlib import Path
from pydo import Client
from rich.console import Console
from rich.console import Console
from rich.panel import Panel

from weown_cli.auth import get_token, verify_auth, get_infisical_client, save_local_token, delete_local_token
from weown_cli.state import StateIsolationEngine
from weown_cli.gateway import gateway_app

class EpilogTyper(typer.Typer):
    def __init__(self, *args, epilog: Optional[str] = None, **kwargs):
        self._epilog = epilog
        super().__init__(*args, **kwargs)

    def info(self, *args, **kwargs):
        info = super().info(*args, **kwargs)
        if self._epilog:
            info.epilog = self._epilog
        return info

app = EpilogTyper(
    help=(
        "jAIMSNet – AI Management Node Manager.\n\n"
        "This CLI provides commands for deploying, tracking, and destroying "
        "WeOwn AI Lite instances securely within isolated User workspaces."
    ),
    epilog=(
        "Examples:\n"
        "  weown-cli login                     Authenticate securely without doctl\n"
        "  weown-cli deploy                    Launch an interactive Lite deployment wizard\n"
        "  weown-cli gateway infra             Provision DOKS + PG core infrastructure\n"
        "  weown-cli gateway deploy            Deploy LiteLLM + Redis + Langfuse on K8s\n"
        "  weown-cli gateway status            Show pod health of all gateway workloads\n"
        "  weown-cli gateway destroy           Tear down the gateway stack\n"
        "  weown-cli list                      Show all active & inactive Lite nodes\n"
        "  weown-cli logs acme-01              Tail the startup logs for a node\n"
        "  weown-cli destroy node              Permanently decommission a Lite node\n"
    )
)
console = Console()
engine = StateIsolationEngine()

advanced_app = typer.Typer(help="Advanced OpenTofu operations (force-unlock, graph, login, logout).")
app.add_typer(advanced_app, name="advanced")

state_app = typer.Typer(help="Advanced OpenTofu state management operations.")
app.add_typer(state_app, name="state")

app.add_typer(gateway_app, name="gateway")

# The canonical source for our IaC templates
IAC_SOURCE_DIR = Path(__file__).resolve().parent.parent.parent.parent / "opentofu" / "environments" / "lite"

def get_valid_token():
    token = get_token()
    if verify_auth(token):
        return token
        
    console.print("[yellow]Could not find a valid DigitalOcean token in local credentials, env, or doctl.[/yellow]")
    token = questionary.password("Please enter your DigitalOcean Personal Access Token:").ask()
    if not verify_auth(token):
        console.print("[red]❌ Invalid Token![/red]")
        raise typer.Exit(1)
        
    save_token = questionary.confirm("Would you like to securely save this token locally for future use?").ask()
    if save_token:
        save_local_token(token)
        console.print("[green]Token saved securely.[/green]")
        
    return token

BANNER = r"""[bold cyan]
   _    _  ___ __  __ ___ _  _     _   
  (_)  / \|_ _|  \/  / __| \| |___| |_ 
  | | / _ \| || |\/| \__ \ .` / -_)  _|
 _/ |/_/ \_\___|_|  |_|___/_|\_\___|\__|
|__/                                     
[/bold cyan]
[bold white]jAIMSNet AI Gateway Setup[/bold white]
"""

# --- AUTH COMMANDS ---

@app.command()
def login(token: str = typer.Option(None, prompt=True, hide_input=True, help="DigitalOcean Personal Access Token")):
    """Authenticate securely with DigitalOcean locally, replacing doctl usage."""
    console.print("Verifying DigitalOcean token...")
    if verify_auth(token):
        save_local_token(token)
        console.print("[bold green]✅ Authentication successful! Token saved securely.[/bold green]")
    else:
        console.print("[bold red]❌ Invalid DigitalOcean token![/bold red]")
        raise typer.Exit(1)

@app.command()
def logout():
    """Remove locally securely stored DigitalOcean token."""
    delete_local_token()
    console.print("[bold green]✅ Logged out successfully.[/bold green]")

@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def exec(ctx: typer.Context):
    """Execute a local command (e.g. 'tofu plan') injecting the secure DigitalOcean token."""
    token = get_valid_token()
    env = os.environ.copy()
    env["DIGITALOCEAN_TOKEN"] = token
    env["DIGITALOCEAN_TOKEN"] = token
    
    cmd = ctx.args
    if not cmd:
        console.print("[red]No command provided to execute. Try: weown-cli exec tofu plan[/red]")
        raise typer.Exit(1)
        
    try:
        subprocess.run(cmd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Command failed with exit code {e.returncode}[/bold red]")
        raise typer.Exit(e.returncode)
    except FileNotFoundError:
        console.print(f"[bold red]Command not found: {cmd[0]}[/bold red]")
        raise typer.Exit(1)

@app.command()
def deploy():
    """Deploy a new WeOwn AI Lite instance."""
    console.print(Panel.fit(BANNER, border_style="cyan", title="[bold]Deployment Wizard[/bold]"))

    
    token = get_valid_token()
    
    deployment_name = questionary.text(
        "Deployment Name (e.g. prod-lite-1):", 
        default="lite-instance"
    ).ask()
    
    if deployment_name is None:
        console.print("\n[red]Cancelled by user[/red]")
        raise typer.Exit()
    
    client = Client(token=token)
    
    console.print("[dim]Fetching available Droplet sizes for atl1...[/dim]")
    try:
        sizes_resp = client.sizes.list()
        sizes = sizes_resp.get("sizes", [])
        
        region_sizes = []
        for s in sizes:
            # Filter for region nyc3 and minimum resources (e.g. >= 2GB RAM, >= 1 vCPU)
            if "atl1" in s.get("regions", []) and s.get("memory", 0) >= 2048 and s.get("vcpus", 0) >= 1:
                region_sizes.append(f"{s['slug']} (${s['price_monthly']}/mo - {s['vcpus']} vCPUs, {s['memory']}MB RAM)")
                
        if not region_sizes:
            console.print("[red]No available sizes found in region.[/red]")
            raise typer.Exit(1)
            
        droplet_size_choice = questionary.select(
            "Droplet Size (monthly cost):",
            choices=region_sizes
        ).ask()
        
        if droplet_size_choice is None:
            console.print("\n[red]Cancelled by user[/red]")
            raise typer.Exit()
        
        # Extract just the slug
        droplet_size = droplet_size_choice.split(" ")[0]
        
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Failed to fetch droplet sizes: {e}[/red]")
        raise typer.Exit(1)
    
    # Query DO API for SSH keys
    console.print("[dim]Fetching your DigitalOcean SSH keys...[/dim]")
    try:
        keys_resp = client.ssh_keys.list()
        key_names = [k["name"] for k in keys_resp.get("ssh_keys", [])]
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Failed to fetch SSH keys: {e}[/red]")
        key_names = []
        
    if not key_names:
        console.print("[red]No SSH keys found in your DigitalOcean account. Please upload one via DO panel first.[/red]")
        raise typer.Exit(1)
        
    ssh_key_name = questionary.select(
        "Select the SSH key to authorize for this Droplet:",
        choices=key_names
    ).ask()
    
    if ssh_key_name is None:
        console.print("\n[red]Cancelled by user[/red]")
        raise typer.Exit()
    
    # Query DO API for managed domains
    console.print("[dim]Fetching managed DigitalOcean domains...[/dim]")
    try:
        domains_resp = client.domains.list()
        domain_names = [d["name"] for d in domains_resp.get("domains", [])]
    except Exception as e:
        console.print(f"[yellow]Could not list domains: {e}[/yellow]")
        domain_names = []
        
    domain_choice = ""
    if domain_names:
        domain_choice = questionary.select(
            "Select a Custom Domain to route to this instance via Let's Encrypt HTTPS (Optional):",
            choices=["None (Use Raw IP)"] + domain_names
        ).ask()
        
        if domain_choice is None:
            console.print("\n[red]Cancelled by user[/red]")
            raise typer.Exit()
            
        if domain_choice == "None (Use Raw IP)":
            domain_choice = ""
    else:
        console.print("[dim]No DigitalOcean-managed domains found. Will deploy to raw IP.[/dim]")
    
    # Prompt for Gateway Config
    console.print("\n[bold]jAIMS Gateway Configuration[/bold]")
    litellm_base_url = questionary.text(
        "LiteLLM Gateway Base URL:",
        default="https://litellm.jAIMS.app"
    ).ask()
    
    if litellm_base_url is None:
        console.print("\n[red]Cancelled by user[/red]")
        raise typer.Exit()
        
    # Attempt to fetch API Key from Infisical securely
    infisical_client = get_infisical_client()
    litellm_api_key = ""
    
    if infisical_client:
        console.print("[dim] securely fetching LiteLLM API Key from Infisical Cloud...[/dim]")
        try:
            # Note: Hardcoded project_id should ideally be an env var. We use project_slug or let user supply INFISICAL_PROJECT_ID
            project_id = os.environ.get("INFISICAL_PROJECT_ID")
            
            if not project_id:
                console.print("[yellow]INFISICAL_PROJECT_ID environment variable not set. Falling back to manual prompt.[/yellow]")
            else:
                secret = infisical_client.secrets.get_secret_by_name(
                    secret_name="LITELLM_MASTER_KEY",
                    project_id=project_id,
                    environment_slug="production",
                    secret_path="/gateway/litellm"
                )
                litellm_api_key = secret.secret_value
                console.print("[green]✅ LiteLLM API Key fetched from Infisical![/green]")
        except Exception as e:
            console.print(f"[yellow]Failed to fetch from Infisical ({e}). Falling back to manual prompt.[/yellow]")
            
    if not litellm_api_key:
        litellm_api_key = questionary.password(
            "LiteLLM Gateway API Key for this instance (Failed to fetch from Infisical):"
        ).ask()
        
        if litellm_api_key is None:
            console.print("\n[red]Cancelled by user[/red]")
            raise typer.Exit()
    
    confirm = questionary.confirm("Are you ready to deploy? Charges will apply to your DO account.").ask()
    if confirm is None or not confirm:
        console.print("\n[yellow]Deployment cancelled.[/yellow]")
        raise typer.Exit()
        
    # Isolate State
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.copy_terraform_files(IAC_SOURCE_DIR, isolated_dir)
    
    # Write tfvars
    engine.write_tfvars(isolated_dir, {
        "ssh_key_name": ssh_key_name,
        "droplet_size": droplet_size,
        "customer_id": deployment_name,
        "domain_name": domain_choice,
        "litellm_base_url": litellm_base_url,
        "litellm_api_key": litellm_api_key
    })
    
    # Deploy
    env_vars = {"DIGITALOCEAN_TOKEN": token}
    
    try:
        if not (isolated_dir / ".terraform").exists():
            engine.run_tofu("init", isolated_dir, env_vars)
            
        engine.run_tofu("apply", isolated_dir, env_vars)
        
        outputs = engine.get_outputs(isolated_dir)
        ipv4 = outputs.get("ipv4_address", {}).get("value", "")
        url = outputs.get("anythingllm_url", {}).get("value", "")
        
        console.print(Panel(f"[bold green]✅ Deployment Successful![/bold green]\\n\\n"
                            f"**IP Address:** {ipv4}\\n"
                            f"**URL:** {url}\\n"
                            f"Use `weown-cli logs {deployment_name}` to track startup script."))
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Deployment failed![/bold red]")
        console.print(f"[red]{e.output}[/red]")
    except Exception as e:
        console.print(f"[bold red]Deployment failed![/bold red] - {str(e)}")
        
@app.command()
def logs(deployment_name: str = typer.Argument(..., help="Name of the deployment to track")):
    """Tail the cloud-init logs of an actively running deployment using local ssh key."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    
    if not isolated_dir.exists():
        console.print(f"[red]Could not find state for deployment: {deployment_name}[/red]")
        raise typer.Exit(1)
        
    outputs = engine.get_outputs(isolated_dir)
    ipv4 = outputs.get("ipv4_address", {}).get("value", "")
    
    if not ipv4:
        console.print("[red]Could not determine droplet IP from state. Is it destroyed?[/red]")
        raise typer.Exit(1)
        
    console.print(f"Connecting to {ipv4} to tail cloud-init logs...")
    
    # Try to auto-detect the ssh key name used for deployment
    default_key_path = ""
    tfvars_path = isolated_dir / "terraform.tfvars"
    if tfvars_path.exists():
        with open(tfvars_path, "r") as f:
            for line in f:
                if line.startswith("ssh_key_name"):
                    ssh_key_name = line.split("=")[1].strip().strip('"')
                    candidate = Path.home() / ".ssh" / ssh_key_name
                    if candidate.exists():
                        default_key_path = str(candidate)
                    break
    
    # Ask for local private key path to use
    key_path = questionary.text(
        "Absolute path to local private SSH key (leave blank to rely on ssh-agent):",
        default=default_key_path
    ).ask()

    if key_path is None:
        console.print("\n[red]Cancelled by user[/red]")
        raise typer.Exit()
    
    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=accept-new"]
    if key_path:
        ssh_cmd.extend(["-i", os.path.expanduser(key_path)])
    ssh_cmd.extend([f"root@{ipv4}", "tail -f /var/log/cloud-init-output.log"])
    
    subprocess.call(ssh_cmd)

@app.command()
def destroy(deployment_name: str = typer.Argument(..., help="Name of the deployment to destroy")):
    """Destroy a deployment."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    
    if not isolated_dir.exists():
        console.print(f"[red]Could not find state for deployment: {deployment_name}[/red]")
        raise typer.Exit(1)
        
    confirm = questionary.confirm(f"⚠️ Are you absolutely sure you want to permanently DESTROY {deployment_name}?").ask()
    if confirm is None or not confirm:
        console.print("\n[yellow]Destruction cancelled.[/yellow]")
        raise typer.Exit()
        
    env_vars = {"DIGITALOCEAN_TOKEN": token}
    try:
        engine.run_tofu("destroy", isolated_dir, env_vars)
        console.print(Panel(f"[bold green]✅ Infrastructure Destroyed![/bold green]"))
    except Exception as e:
        console.print("[bold red]Destruction failed![/bold red]")

@app.command()
def list():
    """List all local deployments."""
    token = get_valid_token()
    user_hash = hashlib.sha256(token.encode()).hexdigest()[:12]
    user_dir = engine.base_state_dir / user_hash
    
    if not user_dir.exists():
        console.print("No deployments found.")
        return
        
    active_deployments = []
    inactive_deployments = []
    
    for d in user_dir.iterdir():
        if d.is_dir():
            if engine.is_active_deployment(d):
                active_deployments.append(d.name)
            else:
                inactive_deployments.append(d.name)
                
    if not active_deployments and not inactive_deployments:
        console.print("No deployments found.")
        return
        
    if active_deployments:
        console.print(f"[bold green]Active Deployments ({len(active_deployments)}):[/bold green]")
        for d in active_deployments:
            console.print(f" - [green]{d}[/green]")
            
    if inactive_deployments:
        console.print(f"\n[bold dim]Inactive / Destroyed Deployments ({len(inactive_deployments)}):[/bold dim]")
        for d in inactive_deployments:
            console.print(f" - [dim]{d}[/dim]")

# --- ADVANCED COMMANDS ---

@advanced_app.command("force-unlock")
def advanced_force_unlock(
    deployment_name: str = typer.Argument(..., help="Name of the deployment"),
    lock_id: str = typer.Argument(..., help="The lock ID to force unlock")
):
    """Force unlock the OpenTofu state for a specific deployment."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.execute_generic_tofu(["force-unlock", "-force", lock_id], isolated_dir)

@advanced_app.command("graph")
def advanced_graph(
    deployment_name: str = typer.Argument(..., help="Name of the deployment"),
):
    """Output the dependency graph of the associated OpenTofu environment."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    # Stream the dot output natively to stdout for pipelining (e.g., `| dot -Tsvg > out.svg`)
    engine.execute_generic_tofu(["graph"], isolated_dir, stream_output=True)



# --- STATE COMMANDS ---

@state_app.command("list")
def state_list(deployment_name: str = typer.Argument(..., help="Name of the deployment")):
    """List resources in the OpenTofu state."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.execute_generic_tofu(["state", "list"], isolated_dir, stream_output=True)

@state_app.command("show")
def state_show(
    deployment_name: str = typer.Argument(..., help="Name of the deployment"),
    address: str = typer.Argument(..., help="Resource address to show")
):
    """Show detailed attributes of a single resource in the OpenTofu state."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.execute_generic_tofu(["state", "show", address], isolated_dir, stream_output=True)

@state_app.command("rm")
def state_rm(
    deployment_name: str = typer.Argument(..., help="Name of the deployment"),
    address: str = typer.Argument(..., help="Resource address to remove")
):
    """Remove a resource from the OpenTofu state without destroying it."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.execute_generic_tofu(["state", "rm", address], isolated_dir, stream_output=True)

@state_app.command("mv")
def state_mv(
    deployment_name: str = typer.Argument(..., help="Name of the deployment"),
    source: str = typer.Argument(..., help="Current resource address"),
    destination: str = typer.Argument(..., help="New resource address")
):
    """Move/rename an item in the OpenTofu state."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.execute_generic_tofu(["state", "mv", source, destination], isolated_dir, stream_output=True)

@state_app.command("pull")
def state_pull(deployment_name: str = typer.Argument(..., help="Name of the deployment")):
    """Pull current state and output to stdout."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    engine.execute_generic_tofu(["state", "pull"], isolated_dir, stream_output=True)

@state_app.command("push")
def state_push(
    deployment_name: str = typer.Argument(..., help="Name of the deployment"),
    path: str = typer.Argument(..., help="Path to the state file to push")
):
    """Push local state file to remote state."""
    token = get_valid_token()
    isolated_dir = engine.get_isolated_path(token, deployment_name)
    file_path = str(Path(path).expanduser().resolve())
    engine.execute_generic_tofu(["state", "push", file_path], isolated_dir, stream_output=True)

if __name__ == "__main__":
    app()
