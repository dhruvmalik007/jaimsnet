# vLLM — GPU Inference

| Field | Value |
|---|---|
| **Phase** | Phase 2 🟠 |
| **Status** | 📋 Planned |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

vLLM provides OpenAI-compatible inference for open-weight LLMs on the AMD MI300X GPU Droplet. Each model runs as an independent Docker container, registered as a custom model endpoint in LiteLLM.

## Hardware

| Resource | Spec |
|---|---|
| GPU | AMD MI300X |
| VRAM | 192 GiB HBM3 |
| Runtime | ROCm 6.x |
| Host OS | Ubuntu 22.04 |
| Deployment | Docker Compose via Ansible |

## Planned Model Deployments

| Model | Container | Port | Est. VRAM | Quantization | Phase |
|---|---|---|---|---|---|
| Llama 3 70B | `vllm-llama3-70b` | 8001 | ~140 GiB (FP16) | AWQ planned | Phase 2 🟠 |
| Mistral 7B | `vllm-mistral-7b` | 8002 | ~15 GiB (FP16) | None | Phase 2 🟠 |
| Mixtral 8x7B | `vllm-mixtral-8x7b` | 8003 | ~90 GiB (FP16) | AWQ planned | Phase 2 🟠 |

## ROCm Tuning Notes

| Parameter | Value | Notes |
|---|---|---|
| `PYTORCH_HIP_ALLOC_CONF` | TBD | HIP memory allocator tuning |
| `gpu-memory-utilization` | `0.90` | Leave 10% headroom |
| `tensor-parallel-size` | `1` | Single GPU per model |
| `max-model-len` | Per-model | Context length tuning |
| `dtype` | `float16` | Default; bfloat16 if supported |

## LiteLLM Integration

Each vLLM instance is registered in LiteLLM as a custom OpenAI-compatible endpoint:

```yaml
# Planned LiteLLM model config entry (documentation only)
# model_name: llama3-70b
# litellm_params:
#   model: openai/llama3-70b
#   api_base: http://<gpu-droplet-ip>:8001
#   api_key: <vllm-api-key-from-infisical>
```

## Related

- [ADR-006](../../docs/decisions/006-vllm-over-sglang.md)
- [gateway/litellm/README.md](../../gateway/litellm/README.md)
- [docs/runbooks/gpu-operations.md](../../docs/runbooks/gpu-operations.md)
