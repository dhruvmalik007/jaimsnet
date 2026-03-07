# Runbook: LiteLLM Operations

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Day-to-day operational guide for LiteLLM on jAIMSnet.

## Service Details

| Parameter | Value |
|---|---|
| Namespace | gateway |
| Deployment | litellm |
| Internal port | 4000 |
| External URL | https://litellm.jAIMS.app |
| Database | DigitalOcean Managed PostgreSQL |
| Cache | Redis (gateway namespace) |

## Health Checks

| Check | Command |
|---|---|
| API health | curl -s https://litellm.jAIMS.app/health |
| Pod status | kubectl get pods -n gateway |
| Logs | kubectl logs -n gateway deployment/litellm --tail=100 |
| Redis connection | kubectl exec -n gateway deploy/litellm -- litellm/test-redis |

## Common Operations

### Restart LiteLLM

kubectl rollout restart deployment/litellm -n gateway
kubectl rollout status deployment/litellm -n gateway

### Check Budget Usage

Access the LiteLLM Admin UI at https://litellm.jAIMS.app/ui (master key required from Infisical).

### Add a New Model

1. Update the LiteLLM config (via Infisical-synced ConfigMap or Helm values)
2. Restart the deployment to pick up the new config
3. Verify model availability: curl -s https://litellm.jAIMS.app/models

### Virtual Key Management

| Action | Method |
|---|---|
| Create key | LiteLLM Admin UI or API |
| List keys | LiteLLM Admin UI |
| Revoke key | LiteLLM Admin UI |
| Set budget | Via key creation params |

## Escalation

| Scenario | Contact |
|---|---|
| LiteLLM pod crash loop | @RMN |
| Provider API failures | @RMN (check provider status page) |
| Database connection issue | @SHD |
| Budget/billing concern | @GTM |
