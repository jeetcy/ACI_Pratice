# 🏢 ACI Full: Cisco ACI Study & Troubleshooting Guide

My complete notes for **Cisco ACI (Application Centric Infrastructure)**: architecture, policy model, **microsegmentation**, **troubleshooting**, **logs & monitoring**, and automation.

> Built for CCNP Data Center (DCCOR 350-601 / DCACI 300-620) and real-world ACI operations.

## 📂 What's inside

| Folder | Contents |
|---|---|
| [`notes/`](notes/) | Architecture, policy model, access policies, forwarding, L3Out |
| [`microsegmentation/`](microsegmentation/) | uSeg EPGs, ESGs, intra-EPG isolation, contracts, vzAny, preferred group |
| [`troubleshooting/`](troubleshooting/) | Method, CLI cheat sheet, 12 real scenarios, contract & endpoint deep-dives |
| [`monitoring/`](monitoring/) | Faults, health scores, events, audit logs, Syslog/SNMP setup, log samples |
| [`scripts/`](scripts/) | Python tools: health/fault monitor, endpoint finder, contract-deny log reader |
| [`automation/`](automation/) | Ansible playbook: tenant + uSeg + contracts |
| [`labs/`](labs/) | Hands-on labs using the free Cisco DevNet ACI sandbox |
| [`cheatsheets/`](cheatsheets/) | moquery, REST API, leaf/spine/APIC commands |
| [`PROGRESS.md`](PROGRESS.md) | My study tracker ✅ |

## 🧠 ACI in one picture
```
                 ┌──────────── APIC cluster (3+) ────────────┐
                 │  Policy controller (NOT in the data path)  │
                 └───────────────────┬────────────────────────┘
          ┌──────────┐          ┌──────────┐
          │ Spine 201│          │ Spine 202│     ← IS-IS + COOP + MP-BGP (route reflectors)
          └─┬───┬───┬┘          └┬───┬───┬─┘
            │   └───┼──────┬─────┘   │   │       every leaf ↔ every spine
          ┌─┴──┐  ┌─┴──┐  ┌┴───┐  ┌──┴─┐
          │L101│  │L102│  │L103│  │L104│      ← VXLAN tunnel endpoints (VTEPs)
          └─┬──┘  └─┬──┘  └─┬──┘  └─┬──┘
          servers  servers  border  border → L3Out (WAN / Internet)
```

## 🗺️ Study order
1. [notes/01-architecture.md](notes/01-architecture.md)
2. [notes/02-policy-model.md](notes/02-policy-model.md)
3. [notes/03-access-policies.md](notes/03-access-policies.md)
4. [notes/04-forwarding-endpoint-learning.md](notes/04-forwarding-endpoint-learning.md)
5. [notes/05-l3out.md](notes/05-l3out.md)
6. [microsegmentation/](microsegmentation/)
7. [monitoring/](monitoring/)
8. [troubleshooting/](troubleshooting/)
9. [labs/](labs/) + [scripts/](scripts/)

## 🧪 Free practice
- **Cisco DevNet Sandbox**: "ACI Simulator Always-On" (free, no booking). See [labs/README.md](labs/README.md).
- **Cisco ACI Simulator** (if your company has access).

## 📚 Great resources
- [datacenter/acitoolkit](https://github.com/datacenter/acitoolkit)
- [CiscoDevNet/ansible-aci](https://github.com/CiscoDevNet/ansible-aci)
- [CiscoDevNet/terraform-provider-aci](https://github.com/CiscoDevNet/terraform-provider-aci)
- Cisco "ACI Troubleshooting" book (free on cisco.com)
- Cisco ACI Policy Model guide & APIC Management Information Model reference

⚠️ **Never** upload real company configs, IPs, hostnames, or passwords to this repo.
