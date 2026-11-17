# 4. Forwarding & Endpoint Learning

## Endpoint (EP) learning
A leaf learns an endpoint's **MAC** and **IP** from the traffic it sends:
- **Local EP**: learned on a front-panel port → reported to the spines by **COOP**.
- **Remote EP**: learned from VXLAN traffic coming from another leaf (cached, used to send traffic straight to that leaf).

When a leaf doesn't know the destination, it sends the traffic to the **spine proxy** (anycast), which looks it up in the COOP database.

## Bridge Domain settings that matter
| Setting | Meaning | Typical value |
|---|---|---|
| **Unicast Routing** | BD routes (gateway) + learns IPs | Enabled |
| **L2 Unknown Unicast** | `Hardware Proxy` (send to the spine) or `Flood` | Hardware Proxy (Flood when there's a firewall/L2 appliance or a migration) |
| **ARP Flooding** | Flood ARP like a normal VLAN | Enable for migrations / silent hosts |
| **Limit IP Learning to Subnet** | Only learn IPs inside the BD subnets | Enabled |
| **Endpoint Dataplane Learning** (on the BD/EPG/VRF) | Learn IPs from data packets | Disable only for special cases (e.g. some load balancers, floating IPs) |
| **Subnet scope** | `Private to VRF` / `Advertised Externally` / `Shared between VRFs` | Advertised Externally if L3Out must announce it |

## Endpoint features to know
- **EP Move Detection**: GARP-based moves.
- **Rogue EP Control**: quarantines endpoints that move ("flap") too often between ports or leafs. Usually caused by a loop, a misconfigured NIC team, or a duplicate IP.
- **IP Aging**: removes stale IPs.
- **Bounce entries**: a leaf temporarily points to the new location after an EP moves.

## Where policy is enforced
- Usually on the **ingress leaf**, if it knows the destination's pcTag.
- Otherwise on the **egress leaf**.
- For L3Out traffic, the VRF's **Policy Control Enforcement Direction** decides: `ingress` (the default, enforced on the non-border leaf) or `egress`.
