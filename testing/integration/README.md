# Integration Tests

| Field | Value |
|---|---|
| **Phase** | Phase 3 🟡 |
| **Status** | 📋 Planned |
| **Owner** | @LDC |
| **Last Updated** | 2025-01-01 |

Integration tests validate end-to-end behavior of jAIMSnet services. Run in CI on `push` to `main` and on PRs targeting `main`.

## Test Suites (Planned)

| Suite | Description | Phase | Status |
|---|---|---|---|
| LiteLLM Endpoint | Validate `/health`, `/chat/completions` responses | Phase 3 🟡 | ⬜ TODO |
| Langfuse Trace Verification | Confirm traces are recorded in Langfuse | Phase 3 🟡 | ⬜ TODO |
| Redis Cache Validation | Confirm cache hit/miss behavior | Phase 3 🟡 | ⬜ TODO |
| Virtual Key + Budget Tests | Validate key creation, budget limits, rate limits | Phase 3 🟡 | ⬜ TODO |
| Secret Sync Test | Confirm Infisical → K8s secret sync | Phase 3 🟡 | ⬜ TODO |
| TLS Validation | Confirm valid TLS for all domains | Phase 3 🟡 | ⬜ TODO |

## Test Environment

| Parameter | Value |
|---|---|
| Target | `https://litellm.jAIMS.app` (staging endpoint planned) |
| Auth | Virtual key from Infisical (CI secret) |
| CI workflow | `.github/workflows/integration-test.yaml` |
| Trigger | PR merge to `main`, nightly |

## Test Conventions

- Tests use **non-production virtual keys** with minimal budgets
- No real LLM API calls in CI — use LiteLLM mock mode or dedicated test models
- Tests must clean up any created resources (keys, logs)
- Test results reported as GitHub Check annotations
