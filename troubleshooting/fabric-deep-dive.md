# Fabric Deep Dive (Underlay & Controllers)

## APIC
```
acidiag fnvread              # all switches + their state (should be "active")
acidiag avread               # APIC cluster view
show controller              # cluster health from the APIC CLI
show version                 # versions of all nodes
```

## Leaf / spine underlay (VRF overlay-1)
```
show isis adjacency vrf overlay-1          # all adjacencies UP
show isis dteps vrf overlay-1              # TEPs of other switches
show ip route vrf overlay-1
show bgp sessions vrf overlay-1            # MP-BGP to the route-reflector spines
show lldp neighbors                        # cabling check
show interface ethernet 1/49 counters errors
```

## Common underlay faults
| Symptom | Likely cause |
|---|---|
| Wiring issue fault on a port | Leaf-to-leaf or spine-to-spine cable, or the wrong role |
| IS-IS adjacency missing | Fabric link down, bad optic, MTU |
| BGP sessions down | BGP route reflector policy not configured / wrong AS |
| APIC "Data Layer Partially Diverged" | Cluster sync problem: check APIC connectivity and NTP |
