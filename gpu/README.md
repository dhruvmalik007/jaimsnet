# GPU Inference

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

GPU-accelerated LLM inference for jAIMSnet using AMD MI300X GPU Droplet and vLLM serving framework. Provides self-hosted open-weight model inference behind the LiteLLM gateway.

## Infrastructure

| Resource | Spec | Status |
|---|---|---|
| GPU | AMD MI300X | 📋 Planned (Phase 2) |
| VRAM | 192 GiB HBM3 | 📋 Planned (Phase 2) |
| Runtime | ROCm 6.x | 📋 Planned (Phase 2) |
| Serving Framework | vLLM | 📋 Planned (Phase 2) |
| Deployment | Docker Compose via Ansible | 📋 Planned (Phase 2) |

## Components

| Directory | Description |
|---|---|
| [vllm/](./vllm/) | vLLM Docker deployment planning |

## Related

- [ADR-006](../docs/decisions/006-vllm-over-sglang.md) — vLLM vs SGLang decision
- [docs/runbooks/gpu-operations.md](../docs/runbooks/gpu-operations.md)
- [gateway/litellm/README.md](../gateway/litellm/README.md)
