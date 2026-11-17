# 🧭 ACI Troubleshooting Method

## Step 0: Collect the facts
- **Source** IP/MAC, **destination** IP/MAC, **port/protocol**
- Which **tenant / VRF / BD / EPG** is each one in?
- Which **leaf + port** is each one on?
- Did it **ever** work? **What changed?** (check the **Audit Log**!)

## Step 1: Look at faults first
`System > Faults` or `Tenant > Faults`, filtered by critical/major. Faults often tell you the answer directly (e.g. F0467 = access policy problem).
```
moquery -c faultInst -f 'fault.Inst.severity=="critical"'
```

## Step 2: Follow the packet, layer by layer
| # | Question | Where / command |
|---|---|---|
| 1 | Is the port up and LLDP/CDP OK? | Leaf: `show interface eth1/10`, `show lldp neighbors` |
| 2 | Is the VLAN deployed on the port? | Leaf: `show vlan extended` (check the EPG ↔ VLAN mapping) |
| 3 | Is the endpoint learned, and in the right EPG? | Leaf: `show endpoint ip X`, `show system internal epm endpoint ip X` |
| 4 | Does the remote leaf / spine know it? | Spine: `show coop internal info ip-db key ip X <vrf-vnid>` |
| 5 | Is routing OK (gateway, L3Out)? | Leaf: `show ip route vrf T:V`, `iping` |
| 6 | Is a contract allowing it? | Leaf: `show zoning-rule`, `show logging ip access-list internal packet-log deny` |
| 7 | Is the drop somewhere else? | Atomic counters, ELAM (or the ELAM Assistant app), SPAN |

## Step 3: Use the built-in tools
- **Visibility & Troubleshooting** (`Operations > Visibility & Troubleshooting`): pick source and destination endpoints and it shows the path, faults, drops, contracts and events.
- **Endpoint Tracker** (`Operations > EP Tracker`): where an endpoint has been, and when it moved.
- **Atomic Counters**: count packets between two endpoints/EPGs across the fabric.
- **SPAN / ERSPAN**: copy traffic to Wireshark.
- **Nexus Dashboard Insights**: anomalies, flow telemetry, pre-change analysis.

## Step 4: Fix one thing → test → document
Write it in [my-log.md](my-log.md).
