# 📈 ACI Logs & Monitoring

| File | Topic |
|---|---|
| [faults-health-events.md](faults-health-events.md) | Faults, health scores, events, audit logs: what they are and how to read them |
| [syslog-snmp-setup.md](syslog-snmp-setup.md) | Step-by-step: send ACI logs to Syslog/SIEM and set up SNMP |
| [monitoring-stack.md](monitoring-stack.md) | A simple home-lab monitoring setup (rsyslog + Python poller) |
| [log-samples/](log-samples/) | Example logs with line-by-line explanations |

## The 4 types of records in ACI
| Record | Class | Answers the question | Example |
|---|---|---|---|
| **Fault** | `faultInst` | "What is **broken** right now?" | F0467 config failed on EPG |
| **Event** | `eventRecord` | "What **happened**?" | Interface went down at 10:12 |
| **Audit log** | `aaaModLR` | "**Who changed** what?" | admin deleted contract WEB-443 |
| **Health score** | `healthInst` | "How **healthy** is it, 0–100?" | Tenant PROD = 87 |

👉 Troubleshooting tip: **audit log first**. Most outages come right after a change.
