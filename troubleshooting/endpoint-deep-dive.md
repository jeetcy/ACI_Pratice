# Endpoint Deep Dive

## Commands
```
# Leaf: is the endpoint learned?
show endpoint ip 10.1.1.10
show endpoint mac 0050.5600.0001
show endpoint vrf PROD:VRF1

# Leaf: full detail (interface, VLAN, pcTag/sclass, flags, move count)
show system internal epm endpoint ip 10.1.1.10

# Spine: what COOP knows (the fabric-wide database)
show coop internal info ip-db key ip 10.1.1.10 <vrf-vnid>
show coop internal info repo ep key <bd-vnid> 0050.5600.0001

# APIC
moquery -c fvCEp -f 'fv.CEp.ip=="10.1.1.10"'
moquery -c fvIp  -f 'fv.Ip.addr=="10.1.1.10"'
```

## Endpoint flags to know
| Flag | Meaning |
|---|---|
| **L** | Local (learned on a port of this leaf) |
| **V** | vPC-attached |
| **p** | Peer-attached (learned on the vPC peer) |
| **s** | Static endpoint |
| **B** | Bounce entry (temporary pointer after a move) |

## Endpoint is missing: checklist
1. Is the host sending traffic? (Silent hosts aren't learned. See scenario 7.)
2. Is the VLAN deployed on the port? `show vlan extended`
3. Is the IP inside a BD subnet? (*Limit IP Learning to Subnet*)
4. Is data-plane learning disabled on the EPG/BD/VRF?
5. Is the EP quarantined by **Rogue EP Control**? Check the faults.

## Clearing an endpoint (use with care)
```
clear system internal epm endpoint key vrf PROD:VRF1 ip 10.1.1.10
```
