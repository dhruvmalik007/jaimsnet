"""
gateway.py — weown-cli Gateway Deployment Module

Provides `weown-cli gateway` sub-commands for deploying, checking the status of,
and tearing down the core jAIMSnet shared gateway stack:

  • Redis         (gateway/redis/)          — response caching
  • LiteLLM       (gateway/litellm/)        — AI gateway proxy
  • Langfuse      (observability/langfuse/) — traces + evals
  • AnythingLLM   (gateway/anythingllm/)   — AI workspace UI
                    ↳ uses LiteLLM as its LLM provider
                    ↳ uses PostgreSQL as its database
                    ↳ uses Redis (gateway ns) for caching
                    ↳ sends traces to self-hosted Langfuse

All kubectl commands are run after saving the DOKS kubeconfig via `doctl`, so the
DigitalOcean token injected by `get_valid_token()` is all that is needed.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import List, Optional

import questionary
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

# ---------------------------------------------------------------------------
# Repo-root relative paths
# ---------------------------------------------------------------------------

# This file lives at: <repo>/iac/weown-cli/src/weown_cli/gateway.py
# So the repo root is 5 levels up.
_HERE = Path(__file__).resolve()
REPO_ROOT = _HERE.parents[4]  # jaimsnet/

GATEWAY_DIR = REPO_ROOT / "gateway"
OBSERVABILITY_DIR = REPO_ROOT / "observability"

# Ordered deployment manifests — applied in this exact sequence
DEPLOY_PLAN: List[tuple[str, List[Path]]] = [
    # 1. Namespaces (idempotent, must come first)
    ("Namespaces", [
        GATEWAY_DIR / "litellm" / "namespace.yaml",
        GATEWAY_DIR / "anythingllm" / "namespace.yaml",
        OBSERVABILITY_DIR / "langfuse" / "namespace.yaml",
    ]),
    # 2. Infisical secret sync CRDs
    ("Infisical Secret Syncs", [
        GATEWAY_DIR / "redis" / "infisical-secret.yaml",
        GATEWAY_DIR / "litellm" / "infisical-secret.yaml",
        GATEWAY_DIR / "anythingllm" / "infisical-secret.yaml",
        OBSERVABILITY_DIR / "langfuse" / "infisical-secret.yaml",
    ]),
    # 3. Redis — cache must be up before LiteLLM and AnythingLLM
    ("Redis Cache", [
        GATEWAY_DIR / "redis" / "pvc.yaml",
        GATEWAY_DIR / "redis" / "statefulset.yaml",
        GATEWAY_DIR / "redis" / "service.yaml",
    ]),
    # 4. Langfuse — observability before LiteLLM so callbacks can connect
    ("Langfuse Observability", [
        OBSERVABILITY_DIR / "langfuse" / "deployment.yaml",
        OBSERVABILITY_DIR / "langfuse" / "service.yaml",
        OBSERVABILITY_DIR / "langfuse" / "ingress.yaml",
    ]),
    # 5. LiteLLM gateway — after Redis + Langfuse, before AnythingLLM
    ("LiteLLM Gateway", [
        GATEWAY_DIR / "litellm" / "configmap.yaml",
        GATEWAY_DIR / "litellm" / "deployment.yaml",
        GATEWAY_DIR / "litellm" / "service.yaml",
        GATEWAY_DIR / "litellm" / "ingress.yaml",
    ]),
    # 6. AnythingLLM — last, depends on LiteLLM + Redis + Langfuse
    ("AnythingLLM UI", [
        GATEWAY_DIR / "anythingllm" / "pvc.yaml",
        GATEWAY_DIR / "anythingllm" / "deployment.yaml",
        GATEWAY_DIR / "anythingllm" / "service.yaml",
        GATEWAY_DIR / "anythingllm" / "ingress.yaml",
    ]),
]

# Namespaces and their key workloads for `gateway status`
STATUS_CHECKS: List[tuple[str, str]] = [
    ("gateway", "deployment/litellm"),
    ("gateway", "statefulset/redis"),
    ("observability", "deployment/langfuse"),
    ("anythingllm", "deployment/anythingllm"),
]

console = Console()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _run_kubectl(args: List[str], env: dict, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    """Run a kubectl command with the provided environment."""
    cmd = ["kubectl"] + args
    console.print(f"[dim]  → {' '.join(cmd)}[/dim]")
    return subprocess.run(
        cmd,
        env=env,
        check=check,
        capture_output=capture,
        text=True,
    )


def _save_kubeconfig(token: str, cluster_name: str) -> dict:
    """
    Save the DOKS kubeconfig via doctl, injecting DIGITALOCEAN_TOKEN.
    Returns the environment dict to pass to subsequent kubectl calls.
    """
    env = os.environ.copy()
    env["DIGITALOCEAN_TOKEN"] = token

    console.print(f"[dim]Saving kubeconfig for cluster: [bold]{cluster_name}[/bold]...[/dim]")
    try:
        subprocess.run(
            ["doctl", "kubernetes", "cluster", "kubeconfig", "save", cluster_name],
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        console.print("[green]✅ kubeconfig saved.[/green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Failed to save kubeconfig:[/bold red]\n{e.stderr}")
        raise typer.Exit(1)

    return env


def _apply_manifests(manifests: List[Path], env: dict):
    """Apply a list of manifest files, skipping missing ones with a warning."""
    for manifest in manifests:
        if not manifest.exists():
            console.print(f"  [yellow]⚠  Manifest not found, skipping: {manifest.relative_to(REPO_ROOT)}[/yellow]")
            continue
        try:
            _run_kubectl(["apply", "-f", str(manifest)], env)
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]  ❌ Failed to apply {manifest.name}[/bold red]")
            raise


def _delete_manifests(manifests: List[Path], env: dict):
    """Delete a list of manifest files, ignoring 'not found' errors."""
    for manifest in reversed(manifests):  # reverse order for safe teardown
        if not manifest.exists():
            continue
        try:
            _run_kubectl(["delete", "-f", str(manifest), "--ignore-not-found"], env)
        except subprocess.CalledProcessError:
            pass  # Best-effort deletion


# ---------------------------------------------------------------------------
# Typer gateway sub-app
# ---------------------------------------------------------------------------

gateway_app = typer.Typer(
    help=(
        "Deploy and manage the jAIMSnet shared gateway stack.\n\n"
        "Applies K8s manifests from gateway/ and observability/ directories "
        "directly onto the target DOKS cluster."
    )
)


@gateway_app.command("deploy")
def gateway_deploy(
    cluster: str = typer.Option(
        "jaimsnet-production-doks",
        "--cluster", "-c",
        help="DOKS cluster name (as shown in `doctl kubernetes cluster list`)",
        prompt="DOKS cluster name"
    ),
    skip_confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Deploy the full gateway stack: Redis → Langfuse → LiteLLM.

    Applies all K8s manifests from gateway/ and observability/langfuse/
    onto the specified DOKS cluster in the correct dependency order.
    """
    from weown_cli.auth import get_token, verify_auth, save_local_token
    import questionary

    # --- Auth ---
    def get_valid_token():
        token = get_token()
        if verify_auth(token):
            return token
        console.print("[yellow]No valid DigitalOcean token found.[/yellow]")
        token = questionary.password("Enter your DigitalOcean Personal Access Token:").ask()
        if not verify_auth(token):
            console.print("[bold red]❌ Invalid token.[/bold red]")
            raise typer.Exit(1)
        if questionary.confirm("Save token locally for future use?").ask():
            save_local_token(token)
        return token

    token = get_valid_token()

    # --- Summary ---
    console.print(Panel.fit(
        f"[bold]Gateway Deployment Plan[/bold]\n\n"
        f"  Cluster:    [cyan]{cluster}[/cyan]\n"
        f"  Repo Root:  [dim]{REPO_ROOT}[/dim]\n\n"
        "[bold]Phases:[/bold]\n" +
        "\n".join(f"  {i+1}. {name}" for i, (name, _) in enumerate(DEPLOY_PLAN)),
        border_style="cyan",
    ))

    if not skip_confirm:
        ok = questionary.confirm("Proceed with gateway deployment? (kubectl apply)").ask()
        if not ok:
            console.print("[yellow]Deployment cancelled.[/yellow]")
            raise typer.Exit()

    env = _save_kubeconfig(token, cluster)

    # --- Apply each phase ---
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console, transient=False) as progress:
        for phase_name, manifests in DEPLOY_PLAN:
            task = progress.add_task(f"[bold]{phase_name}[/bold]...", total=None)
            console.print(f"\n[bold white]── {phase_name} ──[/bold white]")
            _apply_manifests(manifests, env)
            progress.update(task, description=f"[green]✅ {phase_name}[/green]", completed=True, total=1)

    console.print(Panel(
        "[bold green]✅ Full gateway stack deployed successfully![/bold green]\n\n"
        "  [cyan]LiteLLM:[/cyan]      https://litellm.jAIMS.app\n"
        "  [cyan]Langfuse:[/cyan]     https://langfuse.jAIMS.app\n"
        "  [cyan]AnythingLLM:[/cyan]  https://anythingllm.jAIMS.app\n\n"
        "AnythingLLM → LiteLLM (OpenAI-compat) → Redis (cache) → Langfuse (traces)\n\n"
        "Run [bold yellow]weown-cli gateway status[/bold yellow] to verify all pods are Running.",
        border_style="green"
    ))


@gateway_app.command("status")
def gateway_status(
    cluster: str = typer.Option(
        "jaimsnet-production-doks",
        "--cluster", "-c",
        help="DOKS cluster name",
    ),
):
    """Show the rollout status and pod health of all gateway workloads."""
    from weown_cli.auth import get_token, verify_auth

    token = get_token()
    if not verify_auth(token):
        console.print("[red]Not authenticated. Run: weown-cli login[/red]")
        raise typer.Exit(1)

    env = _save_kubeconfig(token, cluster)

    table = Table(title="Gateway Stack Status", border_style="dim")
    table.add_column("Namespace", style="cyan")
    table.add_column("Workload", style="white")
    table.add_column("Rollout", style="green")

    for namespace, workload in STATUS_CHECKS:
        result = subprocess.run(
            ["kubectl", "rollout", "status", workload, "-n", namespace, "--timeout=10s"],
            env=env,
            capture_output=True,
            text=True,
        )
        status_text = "[green]✅ Ready[/green]" if result.returncode == 0 else f"[yellow]⏳ {result.stdout.strip() or result.stderr.strip()}[/yellow]"
        table.add_row(namespace, workload, status_text)

    console.print(table)

    # Also show pods
    console.print("\n[bold]Pods — gateway namespace:[/bold]")
    _run_kubectl(["get", "pods", "-n", "gateway", "-o", "wide"], env, check=False)
    # Also show pods for AnythingLLM
    console.print("\n[bold]Pods — anythingllm namespace:[/bold]")
    _run_kubectl(["get", "pods", "-n", "anythingllm", "-o", "wide"], env, check=False)


@gateway_app.command("destroy")
def gateway_destroy(
    cluster: str = typer.Option(
        "jaimsnet-production-doks",
        "--cluster", "-c",
        help="DOKS cluster name",
    ),
    skip_confirm: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
):
    """
    Tear down the full gateway stack (AnythingLLM, LiteLLM, Redis, Langfuse).

    Deletes all manifests in reverse order. Namespaces are NOT deleted by default
    to preserve PVCs and other namespace-level resources.
    """
    import questionary
    from weown_cli.auth import get_token, verify_auth

    token = get_token()
    if not verify_auth(token):
        console.print("[red]Not authenticated. Run: weown-cli login[/red]")
        raise typer.Exit(1)

    if not skip_confirm:
        ok = questionary.confirm(
            "⚠️  This will DELETE AnythingLLM, LiteLLM, Redis, and Langfuse workloads. Continue?"
        ).ask()
        if not ok:
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit()

    env = _save_kubeconfig(token, cluster)

    # Delete in reverse phase order, skipping namespace manifests
    for phase_name, manifests in reversed(DEPLOY_PLAN):
        if phase_name == "Namespaces":
            continue  # Keep namespaces to preserve PVCs
        console.print(f"\n[bold white]── Removing: {phase_name} ──[/bold white]")
        _delete_manifests(manifests, env)

    console.print(Panel("[bold green]✅ Gateway stack removed.[/bold green]", border_style="green"))


@gateway_app.command("infra")
def gateway_infra(
    cluster_name: str = typer.Option(
        "jaimsnet-production-doks",
        "--cluster", "-c",
        help="Name for the DOKS cluster",
    ),
    ssh_key_name: str = typer.Option(
        ...,
        "--ssh-key",
        help="Name of existing SSH key in DigitalOcean (for Uptime Kuma Droplet)",
        prompt="SSH key name (from your DO account)"
    ),
    domain: str = typer.Option(
        "jaims.app",
        "--domain",
        help="Primary domain for DNS records",
    ),
    skip_confirm: bool = typer.Option(False, "--yes", "-y"),
):
    """
    Provision core infrastructure with OpenTofu: DOKS, VPC, PostgreSQL, Load Balancer.

    This is Step 0 — run this before `gateway deploy`. Uses the production
    OpenTofu environment at iac/opentofu/environments/production/.
    """
    from weown_cli.auth import get_token, verify_auth
    import questionary

    token = get_token()
    if not verify_auth(token):
        console.print("[red]Not authenticated. Run: weown-cli login[/red]")
        raise typer.Exit(1)

    tofu_dir = REPO_ROOT / "iac" / "opentofu" / "environments" / "production"
    if not tofu_dir.exists():
        console.print(f"[red]OpenTofu directory not found: {tofu_dir}[/red]")
        raise typer.Exit(1)

    console.print(Panel.fit(
        f"[bold]Core Infrastructure Plan[/bold]\n\n"
        f"  OpenTofu Dir: [dim]{tofu_dir}[/dim]\n"
        f"  Cluster Name: [cyan]{cluster_name}[/cyan]\n"
        f"  SSH Key:      [cyan]{ssh_key_name}[/cyan]\n"
        f"  Domain:       [cyan]{domain}[/cyan]",
        border_style="cyan",
    ))

    if not skip_confirm:
        ok = questionary.confirm("Provision infrastructure? This will create DO resources and incur costs.").ask()
        if not ok:
            console.print("[yellow]Cancelled.[/yellow]")
            raise typer.Exit()

    env = os.environ.copy()
    env["DIGITALOCEAN_TOKEN"] = token

    def run(cmd: List[str]):
        console.print(f"[dim]  → {' '.join(cmd)}[/dim]")
        subprocess.run(cmd, env=env, check=True, cwd=str(tofu_dir))

    console.print("\n[bold]Step 1: tofu init[/bold]")
    run(["tofu", "init"])

    console.print("\n[bold]Step 2: tofu apply[/bold]")
    run([
        "tofu", "apply", "-auto-approve",
        f"-var=ssh_key_name={ssh_key_name}",
        f"-var=domain={domain}",
    ])

    console.print("\n[bold]Step 3: Saving kubeconfig[/bold]")
    subprocess.run(
        ["doctl", "kubernetes", "cluster", "kubeconfig", "save", cluster_name],
        env=env,
        check=True,
    )

    console.print(Panel(
        "[bold green]✅ Core infrastructure ready![/bold green]\n\n"
        "Next step: [bold yellow]weown-cli gateway deploy[/bold yellow]",
        border_style="green"
    ))
