# 🔐 Microsegmentation in ACI

**Microsegmentation = putting security rules between individual workloads**, even ones that share the same subnet, VLAN or EPG.

| File | Topic |
|---|---|
| [01-concepts.md](01-concepts.md) | All the tools compared: uSeg EPG, ESG, intra-EPG isolation, intra-EPG contracts, vzAny, preferred group, taboo |
| [02-useg-epg.md](02-useg-epg.md) | Attribute-based EPGs (IP / MAC / VM attributes): config + verify |
| [03-esg.md](03-esg.md) | Endpoint Security Groups (the modern way) |
| [04-intra-epg.md](04-intra-epg.md) | Isolation + intra-EPG contracts |
| [05-contract-logging.md](05-contract-logging.md) | Logging permits/denies, so you can **prove** your segmentation works |
| [06-design-example.md](06-design-example.md) | Full example: 3-tier app + PCI zone + quarantine |
