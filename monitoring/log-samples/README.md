# 🔍 Log Samples Explained

> Examples are simplified to show the **structure**. Exact formats vary by APIC/switch version and syslog format setting.

## 1. Fault (syslog, ACI format)
```
Nov 17 10:15:02 apic1 %LOG_LOCAL7-5-SYSTEM_MSG [F0467][raised][configuration-failed][minor][uni/tn-PROD/ap-APP1/epg-WEB/nwissues/fault-F0467] Configuration failed for uni/tn-PROD/ap-APP1/epg-WEB node 101 eth1/10 due to Invalid VLAN Configuration
```
| Part | Meaning |
|---|---|
| `F0467` | Fault code |
| `raised` | Lifecycle state (raised / raised-clearing / retaining / soaking) |
| `configuration-failed` | Cause |
| `minor` | Severity |
| `uni/tn-PROD/.../epg-WEB/...` | **DN**: which object has the problem |
| text | Human-readable description |

➡️ Action: check VLAN pool → domain → AAEP for node 101 eth1/10.

## 2. Event (interface down)
```
Nov 17 10:12:44 leaf101 %LOG_LOCAL7-3-SYSTEM_MSG [E<code>][port-down][error][sys/phys-[eth1/10]] Port eth1/10 is down
```
➡️ Action: cable / server NIC / optic. Check `show interface eth1/10`.

## 3. Audit log (who changed what)
```
Nov 17 09:58:10 apic1 %LOG_LOCAL7-6-SYSTEM_MSG [deletion][uni/tn-PROD/brc-WEB-443][info] Contract WEB-443 deleted by user: netadmin from 10.99.1.25
```
➡️ This is your "what changed?" answer. Look at it **before** anything else in an outage.

## 4. Contract deny log (leaf CLI)
```
leaf101# show logging ip access-list internal packet-log deny
[ Tue Nov 17 10:20:31 2026 ][...] CName: PROD:VRF1(VXLAN: 2523136), VlanType: FD_VLAN, Vlan-Id: 12, SMac: 0x005056000066, DMac:0x0022bdf819ff, SIP: 10.1.2.45, DIP: 10.1.3.20, SPort: 50122, DPort: 1433, Src Intf: Ethernet1/10, Proto: 6, PktLen: 74
```
| Field | Meaning |
|---|---|
| `CName` | Tenant:VRF + VRF VNID (the scope for `show zoning-rule`) |
| `SIP/DIP` | Source/destination IP |
| `DPort` / `Proto: 6` | Destination port / TCP |
| `Src Intf` | Where it entered the leaf |

➡️ 10.1.2.45 (quarantined host) tried SQL to 10.1.3.20 and was **dropped**. ✅ Segmentation is working.

## 5. Endpoint move / rogue EP
```
[F<code>][raised][rogue-ep-detected][major][... ip-[10.1.1.50]] ... Endpoint is moving frequently between interfaces/nodes
```
➡️ Check for a duplicate IP, NIC teaming, or an L2 loop. Use EP Tracker. *(Look up the exact fault and event codes in the APIC fault reference for your version.)*
