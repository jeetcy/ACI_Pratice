# Contract Logging: Prove Your Segmentation Works

## Turn on logging
**Permit + log** for a subject's filter:
`Contract > Subject > Filters > (filter) > Directives: ✅ Log`
REST: `vzRsSubjFiltAtt` → `"directives": "log"` (and `"action": "deny"` for a deny filter).

**The default (implicit) deny**: drops that match no contract are logged by the leaf by default (rate-limited). To log a specific deny, use a **deny + log** filter in a contract or a taboo contract.

## Where to read the logs
**APIC GUI**
- `Tenants > PROD > Operational > Flows` → **L3 Permit / L3 Drop** (and L2)
- `Tenants > PROD > Operational > Packets` → **Permit / Drop** counts

**Leaf CLI (best for quick checks)**
```
show logging ip access-list internal packet-log deny
show logging ip access-list internal packet-log permit
```
Example output (format may vary by version):
```
[ Tue Nov 17 10:12:44 2026 ] LID=... VRF=PROD:VRF1 VLAN-Id=... Src=10.1.1.66 Dst=10.2.2.20 Proto=6 SPort=51514 DPort=1433 ...  Action=Deny
```
Read it as: **who** (Src) tried to reach **what** (Dst:DPort), and it was **denied**. ✅ Your quarantine is working.

**Send to Syslog**: see [../monitoring/syslog-snmp-setup.md](../monitoring/syslog-snmp-setup.md). Contract log messages can go to your SIEM.

## Script
[`../scripts/deny_log_reader.py`](../scripts/deny_log_reader.py) pulls the drop/deny flow records from the APIC API and prints a table.

## ⚠️ Notes
- Logging uses rate-limited CPU copies. It's for **visibility**, not a full firewall log.
- Turn it on for troubleshooting or audits, then turn it off for very busy flows.
