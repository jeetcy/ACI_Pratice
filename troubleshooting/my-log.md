# 📓 My ACI Troubleshooting Log

| Date | Symptom | Fault/Log seen | Commands used | Root cause | Fix |
|---|---|---|---|---|---|
| 2026-11-17 | Example: new EPG can't reach the gateway | F0467 invalid-vlan | `show vlan extended`, checked the VLAN pool | VLAN 120 missing from pool `PHY-POOL` | Added 120 to the pool |
| | | | | | |
