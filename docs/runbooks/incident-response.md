# Runbook: Incident Response

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Incident response procedures for jAIMSnet platform issues.

## Severity Levels

| Level | Description | Response Time | Examples |
|---|---|---|---|
| P1 — Critical | Full platform outage or data breach | Immediate | All LiteLLM APIs down, secret exposure |
| P2 — High | Major feature unavailable | < 1 hour | LiteLLM up but all models failing, Langfuse traces not recording |
| P3 — Medium | Degraded performance | < 4 hours | High latency, partial model failures |
| P4 — Low | Minor issue | < 24 hours | Dashboard cosmetic issue, non-critical alert |

## On-Call Contacts

| Role | Contact | Escalation |
|---|---|---|
| Platform Lead | @RMN | First responder for P1/P2 |
| DevOps | @SHD | Infrastructure / K8s issues |
| AI Infrastructure | @LDC | GPU / vLLM / LiteLLM issues |
| Stakeholder | @GTM | P1 notification required |

## Triage Checklist

### Step 1: Assess Impact

```bash
# Check cluster node status
kubectl get nodes

# Check all pods across namespaces
kubectl get pods -A | grep -v Running | grep -v Completed

# Check recent events
kubectl get events -A --sort-by='.lastTimestamp' | tail -20
```

### Step 2: Check Service Health

```bash
# LiteLLM
curl -s https://litellm.jAIMS.app/health | jq .

# Langfuse
curl -s https://langfuse.jAIMS.app/api/public/health | jq .

# Uptime Kuma dashboard
open https://kuma.jAIMS.app
```

### Step 3: Check Logs

```bash
# LiteLLM logs
kubectl logs -n gateway deployment/litellm --tail=100 -f

# Langfuse logs
kubectl logs -n observability deployment/langfuse --tail=100 -f

# ingress-nginx logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller --tail=100
```

### Step 4: Remediate

Refer to the relevant service runbook:
- [litellm-operations.md](./litellm-operations.md)
- [langfuse-operations.md](./langfuse-operations.md)
- [secret-rotation.md](./secret-rotation.md)
- [gpu-operations.md](./gpu-operations.md)
- [disaster-recovery.md](./disaster-recovery.md)

### Step 5: Post-Incident

- Document timeline in incident report
- Update Uptime Kuma with incident note
- Create GitHub issue for root cause fix
- Update runbook if gaps were identified
