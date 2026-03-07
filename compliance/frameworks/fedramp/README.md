# FedRAMP

| Field | Value |
|---|---|
| **Phase** | Phase 4 🟢 |
| **Status** | 📋 Planned |
| **Owner** | @RMN + @GTM |
| **Last Updated** | 2025-01-01 |

FedRAMP (Federal Risk and Authorization Management Program) planning for jAIMSnet. FedRAMP authorization is required for US federal government cloud service adoption.

## Target Authorization Level

| Level | Impact | Use Case |
|---|---|---|
| FedRAMP Moderate | Controlled Unclassified Info | Target for Phase 4 |
| FedRAMP High | Sensitive data | Phase 4+ stretch goal |

## Prerequisites (from prior phases)

FedRAMP builds on all prior compliance phases. Prerequisites include:

| Requirement | Phase | Status |
|---|---|---|
| SOC 2 Type II | Phase 3 🟡 | 📋 Planned |
| ISO 27001 | Phase 3 🟡 | 📋 Planned |
| NIST CSF alignment | Phase 3 🟡 | 📋 Planned |
| Full CI/CD security pipeline | Phase 3 🟡 | 📋 Planned |
| Continuous monitoring (ConMon) | Phase 3 🟡 | 📋 Planned |
| Penetration testing | Phase 4 🟢 | 📋 Planned |
| System Security Plan (SSP) | Phase 4 🟢 | 📋 Planned |

## NIST SP 800-53 Baseline

FedRAMP Moderate uses the NIST SP 800-53 Rev. 5 Moderate baseline (~325 controls). Key control families:

| Family | Controls | Priority |
|---|---|---|
| AC — Access Control | AC-1 through AC-25 | High |
| AU — Audit & Accountability | AU-1 through AU-16 | High |
| CA — Assessment & Authorization | CA-1 through CA-9 | High |
| CM — Configuration Management | CM-1 through CM-14 | High |
| IA — Identification & Authentication | IA-1 through IA-12 | High |
| IR — Incident Response | IR-1 through IR-10 | High |
| SC — System & Communications Protection | SC-1 through SC-45 | High |
| SI — System & Information Integrity | SI-1 through SI-23 | High |

## Notes

- FedRAMP authorization requires a 3PAO (Third-Party Assessment Organization)
- Authorization process typically takes 12–18 months
- DigitalOcean's FedRAMP status must be evaluated as a cloud service provider
