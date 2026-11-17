# Design Example: 3-Tier App + PCI Zone + Quarantine

## Requirements
1. Users → WEB on 443 only.
2. WEB → APP on 8080 only.
3. APP → DB on 1433 only.
4. DB servers that hold card data (PCI) must be separated even from other DB servers.
5. Any infected host can be **quarantined in seconds**, with no IP change.
6. Everyone can reach DNS/NTP.
7. All denies are logged.

## Design
```
VRF1 ─ BD-WEB (10.1.1.0/24) ─ BD-APP (10.1.2.0/24) ─ BD-DB (10.1.3.0/24)

ESG-WEB   (EPG selector: EPG-WEB)       provides HTTPS-443  ← consumed by L3Out ext-EPG USERS
ESG-APP   (EPG selector: EPG-APP)       provides APP-8080   ← consumed by ESG-WEB
ESG-DB    (EPG selector: EPG-DB)        provides SQL-1433   ← consumed by ESG-APP
ESG-PCI   (IP selector: 10.1.3.128/25)  provides SQL-1433   ← consumed only by ESG-PCI-APP
ESG-QUARANTINE (IP /32 selectors added on demand)   NO contracts except → REMEDIATION
vzAny consumes COMMON-DNS-NTP (provided by an EPG in tenant common)
Deny + log enabled
```
Why the PCI subnet wins over ESG-DB: the **IP subnet selector** is more specific than the EPG selector, so those endpoints are classified into ESG-PCI. (Always verify with `show system internal epm endpoint ip <ip>`.)

## Quarantine runbook
1. SOC reports that host 10.1.2.45 is infected.
2. Add an IP selector `10.1.2.45/32` to `ESG-QUARANTINE` (GUI, API, or the [Ansible playbook](../automation/ansible/)).
3. Verify: `show system internal epm endpoint ip 10.1.2.45` shows the ESG-QUARANTINE pcTag.
4. Verify: `show logging ip access-list internal packet-log deny` shows its denied attempts.
5. After cleanup, remove the selector.
