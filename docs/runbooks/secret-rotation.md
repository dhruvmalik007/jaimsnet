# Runbook: Secret Rotation

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @SHD |
| **Last Updated** | 2025-01-01 |

Procedure for rotating secrets managed in Infisical Cloud and re-syncing them to Kubernetes via the Infisical Operator.

## Prerequisites

| Requirement | Detail |
|---|---|
| Infisical access | Admin role on jAIMSnet project |
| kubectl access | Cluster admin on `jaimsnet-cluster` |
| Infisical CLI | `infisical` v0.x installed locally |

## Affected Namespaces

| Namespace | Secret | Infisical Path |
|---|---|---|
| `gateway` | `litellm-secrets` | `/gateway/litellm` |
| `observability` | `langfuse-secrets` | `/observability/langfuse` |
| `infisical` | `infisical-operator-credentials` | `/infisical/operator` |

## Rotation Procedure

### 1. Update Secret in Infisical

1. Log in to [Infisical Cloud](https://app.infisical.com) → jAIMSnet project
2. Navigate to the relevant environment (`production`)
3. Locate the secret to rotate
4. Update the secret value
5. Save and confirm the change

### 2. Trigger Re-sync

The Infisical Operator watches for changes automatically. To force a re-sync:

```bash
# Check InfisicalSecret sync status
kubectl get infisicalsecret -A

# Annotate to force re-sync (if needed)
kubectl annotate infisicalsecret <name> -n <namespace> \
  infisical.com/resync="$(date +%s)" --overwrite
```

### 3. Verify Secret Updated in Kubernetes

```bash
# Verify secret exists and was updated (do NOT print values)
kubectl get secret <secret-name> -n <namespace> -o jsonpath='{.metadata.resourceVersion}'

# Check operator logs for sync confirmation
kubectl logs -n infisical deployment/infisical-operator -f --tail=50
```

### 4. Restart Affected Deployments

```bash
kubectl rollout restart deployment/litellm -n gateway
kubectl rollout restart deployment/langfuse -n observability
kubectl rollout status deployment/litellm -n gateway
kubectl rollout status deployment/langfuse -n observability
```

### 5. Verify Service Health

```bash
# LiteLLM health check
curl -s https://litellm.jAIMS.app/health | jq .

# Langfuse health check
curl -s https://langfuse.jAIMS.app/api/public/health | jq .
```

## Escalation

| Scenario | Contact |
|---|---|
| Infisical sync failing | @SHD |
| Service not recovering after rotation | @RMN |
| Production incident | @RMN → @GTM |
