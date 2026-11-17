# Microsegmentation Tools Compared

| Tool | Groups endpoints by | Typical use | APIC version |
|---|---|---|---|
| **EPG + contracts** | VLAN / port / VMM port group | Basic segmentation between tiers | All |
| **uSeg EPG** (attribute-based EPG) | IP, MAC, or VM attributes (VM name, OS, tag, …) | Pull certain hosts out of a base EPG (e.g. **quarantine** a host) | 1.x+ |
| **ESG** (Endpoint Security Group) | EPG, IP subnet, tag selectors **across BDs** in one VRF | The modern, flexible way: security groups separate from network design | **5.0+** |
| **Intra-EPG isolation** | — | Block ALL traffic between members of the same EPG (e.g. backup NICs, DMZ hosts) | All |
| **Intra-EPG contract** | — | Allow only certain ports between members of the same EPG | 3.0+ |
| **Taboo contract** | — | Explicit deny | All |
| **vzAny** | "All EPGs in the VRF" | Common services (DNS/NTP) for everyone, or a permit-any baseline | All |
| **Preferred Group** | Members of the group | Open communication inside the group, contracts for everyone else. Good for migrations. | 2.2+ |

## Mental model
```
       Network design                      Security design
   (VRF / BD / subnet / VLAN)   ≠    (EPG / uSeg EPG / ESG + contracts)
```
In ACI these are **separate**. Two servers in the same subnet can be in different security groups.

## How enforcement works
Every endpoint gets a **pcTag (sclass)** from its EPG/uSeg EPG/ESG. Contracts become **zoning rules** in the leaf TCAM:
```
Rule: src pcTag 49153  →  dst pcTag 32771   filter 5 (tcp/443)   action: permit
```
Check with `show zoning-rule` on the leaf. See [../troubleshooting/contract-deep-dive.md](../troubleshooting/contract-deep-dive.md).

## Which should I use?
- **New design on APIC 5.x+** → **ESG** for security + EPGs only for network attachment.
- **Quarantine one infected VM fast** → **uSeg EPG** (IP/MAC attribute) or move it into a quarantine ESG with an IP selector.
- **Hosts that must never talk to each other** → **intra-EPG isolation**.
- **Same-tier cluster that only needs a few ports** → **intra-EPG contract**.
