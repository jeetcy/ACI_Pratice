# 5. L3Out (connecting ACI to the outside world)

## Parts of an L3Out
```
L3Out (in a tenant, linked to a VRF + L3 Domain)
 ├── Logical Node Profile        → border leaf + router ID
 │     └── Logical Interface Profile → routed / sub-interface / SVI + IP
 ├── Routing protocol            → OSPF / BGP / EIGRP / static
 └── External EPG (L3 EPG / "l3extInstP")
       └── Subnets               → "which outside prefixes belong to this EPG"
```

## External EPG subnet flags (common confusion!)
| Flag | Meaning |
|---|---|
| **External Subnets for External EPG** | Classifies traffic from these prefixes into this EPG (used for **contracts**) |
| **Export Route Control** | Advertise this route out |
| **Import Route Control** | Accept this route in (only if import enforcement is on) |
| **Shared Route Control / Shared Security Import** | For sharing L3Out routes between VRFs |

`0.0.0.0/0` + "External Subnets for External EPG" = **everything outside**.

## For the outside to learn an ACI subnet you need ALL of these:
1. BD subnet scope = **Advertised Externally**
2. BD is **associated with the L3Out** (or use a route-map / export route control)
3. A **contract** between the internal EPG and the external EPG
4. The routing protocol adjacency is **up**

## Check on the border leaf
```
show ip ospf neighbors vrf PROD:VRF1
show bgp ipv4 unicast summary vrf PROD:VRF1
show ip route vrf PROD:VRF1
```
