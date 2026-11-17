# 🩺 12 ACI Troubleshooting Scenarios

---
### 1. New server can't ping its gateway. Fault F0467 on the EPG.
**Check**: `Tenant > EPG > Faults` → `invalid-vlan` / `invalid-path`.
**Cause**: The VLAN isn't in the VLAN pool, or the domain isn't on the EPG, or the AAEP isn't on the interface policy group.
**Fix**: Walk the chain: EPG → Domain → VLAN Pool → AAEP → Interface Policy Group → Interface Profile → Switch Profile. ([notes/03](../notes/03-access-policies.md))
**Verify**: Leaf `show vlan extended` shows the EPG with the VLAN on the port.

---
### 2. Two EPGs can't talk, but each can ping its gateway
**Check** on the source leaf:
```
show endpoint ip 10.1.1.10                    # learned? which EPG?
show logging ip access-list internal packet-log deny | grep 10.2.2.20
show zoning-rule src-epg <pcTag> dst-epg <pcTag>
```
**Cause**: No contract, the contract scope is wrong, the contract is provided but not consumed, or the filter has the wrong port.
**Fix**: Add/fix the contract. Check the **scope** (VRF by default; cross-tenant needs `global` + an export).

---
### 3. Contract exists, but traffic still drops
**Check**: `show zoning-rule` → is there a rule with the right **pcTags + filter**? Is the **hit counter** going up?
**Common causes**:
- Filter is TCP dst 443, but the subject has *Reverse Filter Ports* off → return traffic dropped.
- The endpoint was moved into a **uSeg EPG / ESG** with a different pcTag than you expected.
- A **taboo** contract or a higher-priority deny rule.
- Policy compression/vzAny changed the rule priorities.

---
### 4. Endpoint keeps moving ("EP flapping") / gets disabled by Rogue EP Control
**Check**: `Operations > EP Tracker`, `Fabric > Inventory > ... > Rogue Endpoints` faults, leaf `show system internal epm endpoint ip X` (look at the move count).
**Causes**: Duplicate IP; a server NIC team in an unsupported mode (e.g. active/active without a port-channel); an L2 loop through an external switch; VM vMotion storm; a firewall/LB using floating IPs or MAC.
**Fix**: Fix the NIC teaming / loop. For appliances with floating IPs, consider disabling **Endpoint Data-Plane Learning** on that EPG/BD (follow Cisco guidance).

---
### 5. External network can't reach an ACI subnet (L3Out)
**Check**: Is the subnet in the outside router's routing table?
- BD subnet = **Advertised Externally**?
- BD **associated to the L3Out** (or an export route-map)?
- **Contract** between the internal EPG and the **external EPG**?
- `show ip ospf neighbors vrf T:V` / `show bgp ipv4 unicast summary vrf T:V` on the border leaf.
**Fix**: Usually one of the three settings above is missing.

---
### 6. ACI can't reach the outside, but the external route is on the border leaf
**Check** on the **non-border** leaf: `show ip route vrf T:V`. Is the external route there?
**Cause**: The MP-BGP route reflector isn't configured (`System > System Settings > BGP Route Reflector`: set the AS + spines), or the external EPG subnet/contract is missing.

---
### 7. Silent host isn't reachable until it sends traffic
**Cause**: The fabric hasn't learned the IP yet. With hardware proxy, the spine drops traffic to unknown IPs and triggers an **ARP glean**, but some devices don't answer.
**Fix**: Make sure the BD has **Unicast Routing ON** and a subnet. For problem devices, turn on **ARP Flooding** and/or set *L2 Unknown Unicast = Flood*.

---
### 8. A uSeg EPG isn't catching the endpoint
**Check**: `uSeg EPG > Operational > Client End-Points` is empty; `show system internal epm endpoint ip X` still shows the base EPG's pcTag.
**Causes**: Different BD than the base EPG; VDS without *Allow Micro-Segmentation*; bare metal without a static leaf binding; IP not learned (data-plane learning off, or outside the BD subnet with *Limit IP Learning* on).

---
### 9. Leaf not discovered
**Check**: `Fabric > Inventory > Fabric Membership`. Is it listed as unknown? APIC: `acidiag fnvread`.
**Causes**: Not registered; cabling (leaf-to-leaf by mistake); infra VLAN mismatch; TEP pool overlap; wrong firmware. On the switch console: `show lldp neighbors`, `show discoveryissues` (on supported versions).

---
### 10. vPC port-channel is down
**Check**: Leaf `show vpc brief`, `show port-channel summary`, `show lacp neighbor`.
**Causes**: The vPC protection group is missing; the server isn't running LACP active/passive; the members are in different policy groups; speed mismatch.

---
### 11. APIC cluster unhealthy (not "Fully Fit")
**Check**: `System > Controllers > Cluster as seen by node`; APIC CLI `acidiag avread`, `show controller`.
**Causes**: An APIC lost connectivity to its leaf; database replica out of sync; mismatched versions; time not synced (configure **NTP**!).

---
### 12. Traffic drops intermittently between two leafs
**Check**: `Fabric > Inventory > (leaf) > Interfaces` for CRC errors on fabric ports; `show interface ethX/Y counters errors`; atomic counters between the two endpoints; faults about fabric links.
**Causes**: A bad optic/cable on one fabric link (ECMP sends only some flows through it), MTU issues for L3Out/IPN, or a microburst.
