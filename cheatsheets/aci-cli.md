# 💻 ACI CLI Cheat Sheet

## APIC (SSH to the APIC)
| Command | Purpose |
|---|---|
| `acidiag fnvread` | All switches + their state |
| `acidiag avread` | APIC cluster state |
| `show controller` | Cluster health |
| `show version` | Versions of all nodes |
| `moquery -c <class>` | Query any object (see [moquery-api.md](moquery-api.md)) |
| `ssh <leaf-name>` | Jump from the APIC to a switch |

## Leaf: interfaces & L2
| Command | Purpose |
|---|---|
| `show interface eth1/10` | Status, errors, speed |
| `show interface status` | All ports |
| `show lldp neighbors` / `show cdp neighbors` | What's connected |
| `show vlan extended` | **EPG ↔ VLAN ↔ port** mapping (internal VLAN + encap) |
| `show vpc brief` | vPC status |
| `show port-channel summary` | Port-channels |
| `show lacp neighbor` | LACP partners |

## Leaf: endpoints
| Command | Purpose |
|---|---|
| `show endpoint ip X` / `show endpoint mac X` | Is it learned? Which EPG/VLAN/port? |
| `show endpoint vrf T:V` | All endpoints in a VRF |
| `show system internal epm endpoint ip X` | Full detail incl. **sclass (pcTag)** and move count |

## Leaf: routing
| Command | Purpose |
|---|---|
| `show vrf` | All VRFs on the leaf |
| `show ip route vrf T:V` | Routing table |
| `show ip interface brief vrf T:V` | BD SVIs (gateways) |
| `iping -V T:V 10.1.1.10` | Ping from the fabric, inside a tenant VRF |
| `itraceroute -V T:V 10.1.1.10` | Traceroute inside a tenant VRF |
| `show ip ospf neighbors vrf T:V` | L3Out OSPF |
| `show bgp ipv4 unicast summary vrf T:V` | L3Out BGP |

## Leaf: contracts / security
| Command | Purpose |
|---|---|
| `show zoning-rule scope <vrf-vnid>` | Contract rules (pcTag → pcTag) |
| `show zoning-rule src-epg <tag> dst-epg <tag>` | Rules between two EPGs |
| `show zoning-filter filter <id>` | What a filter matches |
| `show system internal policy-mgr stats` | Hit counters per rule |
| `contract_parser.py --vrf T:V` | Readable rules with EPG names + hits |
| `show logging ip access-list internal packet-log deny` | **Dropped flows** |
| `show logging ip access-list internal packet-log permit` | Permitted + logged flows |

## Leaf/Spine: fabric underlay
| Command | Purpose |
|---|---|
| `show isis adjacency vrf overlay-1` | Underlay neighbors |
| `show isis dteps vrf overlay-1` | Known TEPs |
| `show bgp sessions vrf overlay-1` | MP-BGP to the spines |
| `show coop internal info ip-db key ip X <vnid>` | (spine) COOP endpoint DB |
| `show ntp peer-status` | Time sync |
| `show logging logfile` | Local switch log |
