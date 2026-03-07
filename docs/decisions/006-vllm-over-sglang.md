# ADR-006: vLLM Over SGLang for GPU Inference

| Field | Value |
|---|---|
| **Status** | ✅ Accepted |
| **Date** | 2025-01-01 |
| **Owner** | @LDC |
| **Deciders** | @LDC, @RMN |

## Context

jAIMSnet Phase 2 introduces GPU-accelerated inference on an AMD MI300X GPU Droplet. A serving framework must be chosen to host open-weight LLMs (e.g., Llama 3, Mistral, Mixtral) and expose an OpenAI-compatible API that LiteLLM can proxy.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **vLLM** | OpenAI-compatible API, strong ROCm/AMD support, PagedAttention for VRAM efficiency, active community, LiteLLM native integration, multi-model via separate instances | Single-model per process (multi-instance needed for multi-model) |
| **SGLang** | RadixAttention for prefix caching, faster for structured generation, multi-model engine | Younger project, less AMD/ROCm maturity at decision time |
| **Ollama** | Simple setup, easy multi-model | Not production-grade, limited VRAM management, less LiteLLM integration depth |
| **TGI (Hugging Face)** | Production-grade, quantization support | Less flexible, commercial licensing concerns for some features |

## Decision

Use **vLLM** as the GPU inference serving framework, deployed as Docker containers on the MI300X GPU Droplet. Each model runs as a separate vLLM instance behind a shared reverse proxy, registered as custom model endpoints in LiteLLM.

## Configuration Notes

| Parameter | Value | Rationale |
|---|---|---|
| Runtime | ROCm 6.x | AMD MI300X native |
| API mode | OpenAI-compatible | LiteLLM integration |
| VRAM allocation | Per-model tuning | MI300X has 192GiB HBM3 |
| Quantization | AWQ / GPTQ planned | Fit more models in VRAM |
| Deployment | Docker Compose | Managed via Ansible |

## Consequences

### Positive
- Direct LiteLLM integration via OpenAI-compatible endpoint
- Proven production usage at scale
- ROCm support actively maintained by vLLM community
- PagedAttention maximizes MI300X VRAM utilization

### Negative / Trade-offs
- Multi-model requires multiple processes (higher overhead vs. SGLang's multi-model engine)
- ROCm Docker images are large; pull times may be significant

## References
- [vLLM Documentation](https://docs.vllm.ai)
- [vLLM ROCm Support](https://docs.vllm.ai/en/latest/getting_started/amd-installation.html)
- [LiteLLM Custom Endpoints](https://docs.litellm.ai/docs/providers/custom_openai_proxy)
- [gpu/vllm/README.md](../../gpu/vllm/README.md)
