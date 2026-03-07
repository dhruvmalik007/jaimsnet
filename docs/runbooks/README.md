# Runbooks

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Operational runbooks for managing the jAIMSnet platform. Each runbook covers a specific operational scenario with step-by-step instructions.

## Runbook Index

| Runbook | File | Description | Phase | Status |
|---|---|---|---|---|
| LiteLLM Operations | [litellm-operations.md](./litellm-operations.md) | Day-to-day LiteLLM management | Phase 1 🔴 | 🔄 In Progress |
| Langfuse Operations | [langfuse-operations.md](./langfuse-operations.md) | Day-to-day Langfuse management | Phase 1 🔴 | 🔄 In Progress |
| Secret Rotation | [secret-rotation.md](./secret-rotation.md) | Rotating secrets via Infisical | Phase 1 🔴 | 🔄 In Progress |
| Incident Response | [incident-response.md](./incident-response.md) | Incident triage and response | Phase 1 🔴 | 🔄 In Progress |
| GPU Operations | [gpu-operations.md](./gpu-operations.md) | vLLM and MI300X operations | Phase 2 🟠 | 📋 Planned |
| Disaster Recovery | [disaster-recovery.md](./disaster-recovery.md) | DR procedures for all services | Phase 1 🔴 | 🔄 In Progress |

## Runbook Conventions

- Each runbook lists **prerequisites** before step-by-step instructions
- Commands are shown in code blocks with the expected context (shell, namespace, etc.)
- Runbooks include **verification steps** to confirm success
- Escalation contacts and on-call procedures are listed at the end
