# Runbook: Disaster Recovery

| Field | Value |
|---|---|
| **Phase** | Phase 1 🔴 |
| **Status** | 🔄 In Progress |
| **Owner** | @RMN |
| **Last Updated** | 2025-01-01 |

Disaster recovery procedures for jAIMSnet. Covers data backup, service restoration, and full cluster rebuild.

## Recovery Time Objectives

| Service | RTO Target | RPO Target | Phase |
|---|---|---|---|
| LiteLLM API | 30 min | N/A (stateless) | Phase 1 🔴 |
| Langfuse | 1 hour | 24 hours (PG backup) | Phase 1 🔴 |
| PostgreSQL | 2 hours | 1 day (daily backup) | Phase 1 🔴 |
| Full cluster rebuild | 4 hours | N/A (IaC) | Phase 1 🔴 |

## Backup Inventory

| Data | Backup Method | Frequency | Retention |
|---|---|---|---|
| PostgreSQL (LiteLLM + Langfuse) | DigitalOcean managed backup | Daily | 7 days |
| Helm values + config | Git (this repo) | On change | Indefinite |
| Infisical secrets | Infisical Cloud (multi-region) | Continuous | Infisical SLA |
| Kubernetes manifests | Git (this repo) | On change | Indefinite |

## Recovery Procedures

### Scenario 1: Single Pod Failure

1. K8s will restart the pod automatically
2. If stuck: kubectl delete pod <pod-name> -n <namespace>
3. Check logs: kubectl logs -n <namespace> <pod-name>

### Scenario 2: Node Failure

1. DOKS autoscaler will provision a replacement node
2. Pods will reschedule automatically
3. Verify: kubectl get nodes && kubectl get pods -A

### Scenario 3: Database Restore

1. Access DigitalOcean control panel
2. Navigate to Database cluster
3. Select backup point to restore from
4. Restore to a new cluster (do not overwrite production without validation)
5. Update Infisical with new DB connection string
6. Restart LiteLLM and Langfuse deployments

### Scenario 4: Full Cluster Rebuild

1. Run OpenTofu to recreate infrastructure: cd iac/opentofu/environments/production && tofu apply
2. Restore DNS records (should be managed by OpenTofu already)
3. Deploy Helm charts in order (see deployment-guide.md)
4. Verify all services healthy
5. Update DNS TTLs and wait for propagation

## Escalation

| Scenario | Contact | SLA |
|---|---|---|
| Data loss detected | @RMN → @GTM | Immediate |
| Full outage | @RMN + @SHD | 30 min response |
| DB corruption | @SHD → DigitalOcean support | 1 hour |
