# Runbook: GPU Operations (vLLM / MI300X)

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

Operational procedures for managing vLLM inference on the AMD MI300X GPU Droplet.

## Infrastructure

| Resource | Detail |
|---|---|
| GPU | AMD MI300X (192GiB HBM3) |
| Host | DigitalOcean GPU Droplet |
| Runtime | ROCm 6.x |
| Framework | vLLM (Docker) |
| Orchestration | Docker Compose via Ansible |

## Deployed Models (Planned)

| Model | Instance | Port | VRAM Allocation |
|---|---|---|---|
| Llama 3 70B | vllm-llama3-70b | 8001 | TBD |
| Mistral 7B | vllm-mistral-7b | 8002 | TBD |
| Mixtral 8x7B | vllm-mixtral-8x7b | 8003 | TBD |

## Common Operations

### Check Model Status

```bash
# SSH to GPU Droplet
ssh ubuntu@<gpu-droplet-ip>

# Check running containers
docker ps --filter "name=vllm"

# Check model health
curl -s http://localhost:8001/health
```

### Restart a Model Instance

```bash
docker compose -f /opt/vllm/docker-compose.yml restart vllm-llama3-70b
docker logs vllm-llama3-70b --tail=50 -f
```

### Monitor VRAM Usage

```bash
# ROCm VRAM monitor
rocm-smi --showmeminfo vram

# Per-process VRAM
rocm-smi --showpids
```

### Add a New Model

1. Update `/opt/vllm/docker-compose.yml` with the new service definition
2. Pull the model weights (via Hugging Face or local cache)
3. Start the new container: `docker compose up -d <service-name>`
4. Register the endpoint in LiteLLM config (see [gateway/litellm/README.md](../../gateway/litellm/README.md))

## Escalation

| Scenario | Contact |
|---|---|
| vLLM container crash loop | @LDC |
| ROCm driver issue | @LDC → DigitalOcean support |
| LiteLLM not routing to GPU | @RMN |
