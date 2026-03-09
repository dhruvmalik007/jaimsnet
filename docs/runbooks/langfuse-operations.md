# Runbook: Langfuse Operations

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Day-to-day operational guide for Langfuse on jAIMSnet.

## Service Details

| Parameter | Value |
|---|---|
| Namespace | observability |
| Deployment | langfuse |
| Internal port | 3000 |
| External URL | https://langfuse.jAIMS.app |
| Database | DigitalOcean Managed PostgreSQL |
| LiteLLM integration | Success/failure callback |

## Health Checks

| Check | Command |
|---|---|
| API health | curl -s https://langfuse.jAIMS.app/api/public/health |
| Pod status | kubectl get pods -n observability |
| Logs | kubectl logs -n observability deployment/langfuse --tail=100 |

## Common Operations

### Restart Langfuse

kubectl rollout restart deployment/langfuse -n observability
kubectl rollout status deployment/langfuse -n observability

### Verify Trace Recording

After making an API call via LiteLLM:
1. Open https://langfuse.jAIMS.app
2. Navigate to Traces
3. Confirm the trace appears within 30 seconds

### Database Maintenance

| Task | Action |
|---|---|
| Check PG connection | kubectl logs -n observability deploy/langfuse | grep -i database |
| DB migration (on upgrade) | Langfuse runs migrations on startup automatically |

## Trace Retention

| Setting | Value | Notes |
|---|---|---|
| Retention policy | TBD | Configure in Langfuse settings |
| Evidence backup | TBD | PG backups cover trace data |

## Escalation

| Scenario | Contact |
|---|---|
| Langfuse pod crash loop | @RMN |
| Traces not appearing | @RMN (check LiteLLM callback config) |
| Database issue | @SHD |
