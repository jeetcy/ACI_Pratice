# 1. ACI Architecture

## Main building blocks
| Component | Role |
|---|---|
| **APIC** (Application Policy Infrastructure Controller) | The brain. Stores policy, pushes it to switches. A cluster of 3+ for redundancy. **Not in the data path**: if every APIC goes down, traffic keeps flowing. |
| **Spine** (Nexus 9500 / 9300 / 9364C, etc.) | Connects all leafs. Holds the COOP endpoint database. Acts as the BGP route reflector. |
| **Leaf** (Nexus 9300) | Connects everything else: servers, firewalls, routers, APICs. Does the policy enforcement. |
| **Nexus Dashboard (NDI/NDO)** | Optional. Insights (monitoring/analytics) and Orchestrator (multi-site). |

## Rules of the spine-leaf topology
- Every leaf connects to **every** spine.
- Leafs **never** connect to leafs. Spines **never** connect to spines (except in multi-pod / remote leaf designs).
- Endpoints (servers) connect **only** to leafs.
- So any server-to-server traffic crosses at most leaf → spine → leaf.

## Protocols inside the fabric (the "infra" tenant, VRF `overlay-1`)
| Protocol | Job |
|---|---|
| **LLDP** | Fabric discovery and wiring checks |
| **DHCP** | APIC gives TEP addresses to switches from the **TEP pool** |
| **IS-IS** | Underlay routing between TEPs |
| **VXLAN** | Overlay: carries tenant traffic between leafs, with a header that holds the **VNID** and the source **pcTag/sclass** |
| **COOP** | Leafs report their local endpoints to the spines. The spines keep the full endpoint database (spine proxy). |
| **MP-BGP (VPNv4/v6)** | Spreads external (L3Out) routes to all leafs. The spines are route reflectors. |

## Fabric discovery (good interview question!)
1. APIC1 connects to a leaf and sends LLDP.
2. The leaf shows up in **Fabric > Inventory > Fabric Membership** as "unknown/undiscovered".
3. You register it (node ID + name).
4. The leaf gets a TEP IP via DHCP, downloads its firmware/config, and becomes **active**.
5. Spines are discovered next, through that leaf, and then the other leafs.

APIC check: `acidiag fnvread`. Every node should be `active`.

## Important IDs
| ID | What it is |
|---|---|
| **Node ID** | Switch number (e.g. leafs 101–199, spines 201–299 by convention) |
| **TEP IP** | Switch address inside the underlay |
| **VNID** | VXLAN ID for a **BD** (L2) or a **VRF** (L3) |
| **pcTag / sclass** | Number that identifies an **EPG/ESG** for contract enforcement |
| **Scope (VRF VNID)** | Used in `show zoning-rule scope <id>` |
