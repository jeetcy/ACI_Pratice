# 2. ACI Policy Model

## The object tree
```
Tenant (e.g. PROD)
 ├── VRF (Context)                ← L3 domain, like a separate routing table
 ├── Bridge Domain (BD)           ← L2 domain + subnets (gateways)
 │     └── Subnet 10.1.1.1/24     ← the anycast gateway on every leaf
 ├── Application Profile (AP)
 │     └── EPG (Endpoint Group)   ← group of endpoints with the same policy
 │           ├── linked to 1 BD
 │           ├── Domain (Physical / VMM)
 │           ├── Static ports (path + VLAN)
 │           └── provides/consumes Contracts
 ├── Contract
 │     └── Subject
 │           └── Filter → Entry (e.g. TCP dst 443)
 └── L3Out                        ← connection to outside routers
```

## Key objects
| Object | Simple meaning | Traditional network version |
|---|---|---|
| **Tenant** | Container for one customer/department | — |
| **VRF** | Routing table | VRF |
| **BD** | L2 flood domain + its gateway subnets | VLAN + SVI |
| **EPG** | A **security group** of endpoints | VLAN (but it's really about policy!) |
| **Contract** | Allowed traffic between EPGs | ACL / firewall rule |
| **Filter** | Match criteria (protocol / ports) | ACE |

## The golden rule: whitelist model
- Inside the **same EPG** → traffic is **allowed** by default.
- Between **different EPGs** → **denied** unless a **contract** allows it.
- (Unless the VRF is set to `unenforced`. Lab only, never in production!)

## Contracts
- **Provider** EPG = the one offering the service (e.g. Web servers provide "HTTPS").
- **Consumer** EPG = the one using the service (e.g. Clients consume "HTTPS").
- **Subject options**: *Apply Both Directions* + *Reverse Filter Ports* (both ON by default) let the return traffic back.
- **Contract scope**: `context` (VRF, the default), `application-profile`, `tenant`, `global` (to share between tenants).
- **Filter actions/directives**: permit, deny, **log**, policy compression.

## Special contract tools
| Tool | What it does |
|---|---|
| **vzAny** | "All EPGs in this VRF" as one object. Saves TCAM. |
| **Preferred Group** | EPGs inside the group talk freely without contracts |
| **Taboo contract** | Explicit **deny**, processed before permits |
| **common tenant** | Objects here (filters, contracts, VRFs, BDs) can be used by every tenant |
