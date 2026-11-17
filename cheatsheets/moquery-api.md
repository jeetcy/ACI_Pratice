# 🔎 moquery & REST API Cheat Sheet

## moquery (APIC CLI)
```
moquery -c <class>                         # all objects of a class
moquery -c <class> -f '<pkg>.<Class>.<attr>=="value"'
moquery -d <dn>                            # one object by DN
moquery -c fvTenant | grep name
```
Filter syntax: class `fvAEPg` → `fv.AEPg.name`; `faultInst` → `fault.Inst.severity`.

## Most useful classes
| Class | Object |
|---|---|
| `fvTenant` | Tenant |
| `fvCtx` | VRF |
| `fvBD` / `fvSubnet` | Bridge domain / subnet |
| `fvAp` | Application profile |
| `fvAEPg` | EPG (and uSeg EPG with `isAttrBasedEPg=yes`) |
| `fvESg` / `fvEPSelector` | ESG / ESG selector |
| `fvIpAttr` / `fvMacAttr` | uSeg IP / MAC attributes |
| `fvCEp` / `fvIp` | Learned endpoint / its IPs |
| `vzBrCP` / `vzSubj` / `vzFilter` / `vzEntry` | Contract / subject / filter / entry |
| `l3extOut` / `l3extInstP` | L3Out / external EPG |
| `fvnsVlanInstP` | VLAN pool |
| `infraAttEntityP` | AAEP |
| `fabricNode` | Switches + APICs |
| `faultInst` | Faults |
| `eventRecord` | Events |
| `aaaModLR` | Audit log |
| `healthInst` | Health score |
| `syslogRemoteDest` | Syslog destination |

## REST API
```bash
# 1. Login (saves the token cookie)
curl -sk -c cookie.txt -X POST https://$APIC/api/aaaLogin.json \
  -d '{"aaaUser":{"attributes":{"name":"'"$APIC_USER"'","pwd":"'"$APIC_PASS"'"}}}'

# 2. Class query
curl -sk -b cookie.txt "https://$APIC/api/class/fvTenant.json"

# 3. One object + its children
curl -sk -b cookie.txt "https://$APIC/api/mo/uni/tn-PROD.json?query-target=children"

# 4. Filter + sort + page
curl -sk -b cookie.txt 'https://'$APIC'/api/class/faultInst.json?query-target-filter=eq(faultInst.severity,"critical")&order-by=faultInst.lastTransition|desc&page-size=10'

# 5. Create (POST)
curl -sk -b cookie.txt -X POST "https://$APIC/api/mo/uni.json" \
  -d '{"fvTenant":{"attributes":{"name":"LAB-TEST"}}}'

# 6. Delete
curl -sk -b cookie.txt -X DELETE "https://$APIC/api/mo/uni/tn-LAB-TEST.json"
```

## Query options
| Option | Example |
|---|---|
| `query-target` | `self` / `children` / `subtree` |
| `target-subtree-class` | `fvAEPg` |
| `query-target-filter` | `eq(fvAEPg.name,"WEB")`, `wcard(fvTenant.name,"PRD")`, `and(...)`, `or(...)` |
| `rsp-subtree` | `children` / `full` |
| `rsp-subtree-include` | `health`, `faults`, `count` |
| `order-by` | `faultInst.created\|desc` |
| `page-size` / `page` | `50` / `0` |

💡 Tip: use the **API Inspector** in the GUI to see the exact call for anything you click.
