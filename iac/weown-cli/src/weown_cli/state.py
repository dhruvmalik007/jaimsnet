import os
import hashlib
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class StateIsolationEngine:
    def __init__(self, base_state_dir: str = "~/.weown-cli/state"):
        self.base_state_dir = Path(base_state_dir).expanduser()
        self.console = console
        
    def get_isolated_path(self, auth_token: str, deployment_name: str) -> Path:
        """Hash the DO token to isolate state by account."""
        user_hash = hashlib.sha256(auth_token.encode()).hexdigest()[:12]
        isolated_dir = self.base_state_dir / user_hash / deployment_name
        isolated_dir.mkdir(parents=True, exist_ok=True)
        return isolated_dir
        
    def copy_terraform_files(self, source_dir: Path, dest_dir: Path):
        """Copy main.tf, variables.tf and rewrite relative module paths to absolute."""
        tf_files = list(source_dir.glob("*.tf"))
        
        # We need absolute path to the modules directory for rewriting
        modules_dir_absolute = (source_dir.parent.parent / "modules").resolve()
        
        for tf_file in tf_files:
            content = tf_file.read_text()
            # Replace relative paths to modules with absolute paths
            content = content.replace("../../modules", str(modules_dir_absolute))
            
            dest_file = dest_dir / tf_file.name
            dest_file.write_text(content)
            
    def write_tfvars(self, isolated_dir: Path, vars_data: Dict[str, Any]):
        tfvars_path = isolated_dir / "terraform.tfvars"
        with open(tfvars_path, "w") as f:
            for key, value in vars_data.items():
                f.write(f'{key} = "{value}"\n')
                
    def run_tofu(self, command: str, isolated_dir: Path, env_vars: Dict[str, str] = None, auto_approve: bool = True):
        cmd = ["tofu", f"-chdir={str(isolated_dir)}", command]
        
        if command in ["apply", "destroy"] and auto_approve:
            cmd.append("-auto-approve")
            
        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)
            
        self.console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            task = progress.add_task(f"Executing tofu {command}...", total=None)
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=env,
                bufsize=1,
                universal_newlines=True
            )
            
            output_lines = []
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                # Try to print important lines, but keep it clean
                clean_line = line.strip()
                if clean_line:
                    output_lines.append(clean_line)
                    if "Apply complete!" in clean_line or "Destroy complete!" in clean_line:
                        self.console.print(f"[bold green]{clean_line}[/bold green]")
                    elif "Error:" in clean_line:
                        self.console.print(f"[bold red]{clean_line}[/bold red]")
                    elif "Still creating" in clean_line or "Still destroying" in clean_line:
                        progress.update(task, description=clean_line)
                        
            process.wait()
            
            if process.returncode != 0:
                self.console.print(Panel("[bold red]❌ OpenTofu execution failed.[/bold red]"))
                raise subprocess.CalledProcessError(process.returncode, cmd, "\\n".join(output_lines))
                
        return "\\n".join(output_lines)
        
    def is_active_deployment(self, isolated_dir: Path) -> bool:
        """Check if the state contains actively provisioned resources."""
        if not (isolated_dir / "terraform.tfstate").exists():
            return False
            
        cmd = ["tofu", f"-chdir={str(isolated_dir)}", "show", "-json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(res.stdout)
            
            def any_resources(mod):
                if "resources" in mod:
                    for r in mod["resources"]:
                        if r.get("mode") == "managed":
                            return True
                for child in mod.get("child_modules", []):
                    if any_resources(child):
                        return True
                return False
                
            values = data.get("values") or {}
            root = values.get("root_module") or {}
            return any_resources(root)
        except Exception:
            return False

    def get_outputs(self, isolated_dir: Path) -> Dict[str, Any]:
        """Get tofu outputs."""
        cmd = ["tofu", f"-chdir={str(isolated_dir)}", "output", "-json"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(res.stdout)
        except subprocess.CalledProcessError:
            return {}
