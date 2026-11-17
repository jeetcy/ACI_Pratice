# uSeg EPGs (Attribute-Based EPGs)

## Idea
You have a **base EPG** (e.g. `WEB`). You create a **uSeg EPG** in the **same BD** with a rule like "IP = 10.1.1.66". Any endpoint that matches is **reclassified**: it gets the uSeg EPG's pcTag and contracts.

## Attributes
| Domain type | Attributes you can match |
|---|---|
| **Physical / bare metal** | IP, MAC |
| **VMware VDS (VMM)** | IP, MAC, VM name, VM ID, OS, host (hypervisor), datacenter, custom attribute, VM tag, vNIC DN |

- Matching can be **any** (OR) or **all** (AND), set on the criteria (`fvCrtrn match="any|all"`).
- If several uSeg EPGs match one endpoint, ACI uses its built-in **attribute precedence**, then the **EPG Match Precedence** value you set.

## GUI steps
`Tenants > PROD > Application Profiles > APP1 > uSeg EPGs > Create uSeg EPG`
1. Name: `uSeg-QUARANTINE`
2. Bridge Domain: **the same BD** as the base EPG
3. Domain: the same domain as the base EPG
   - **VMware VDS**: on the **base EPG's** VMM domain association, tick **Allow Micro-Segmentation**.
   - **Bare metal**: add a **static leaf** binding (the node where the hosts connect) to the uSeg EPG.
4. **uSeg Attributes** → `+` → IP Address → `10.1.1.66`
5. Add **no contracts** (or only a "to-remediation-server" contract) → the host is isolated.

## REST API (POST to `/api/mo/uni/tn-PROD/ap-APP1.json`)
```json
{
  "fvAEPg": {
    "attributes": { "name": "uSeg-QUARANTINE", "isAttrBasedEPg": "yes" },
    "children": [
      { "fvRsBd": { "attributes": { "tnFvBDName": "BD-WEB" } } },
      { "fvCrtrn": {
          "attributes": { "name": "default", "match": "any" },
          "children": [
            { "fvIpAttr": { "attributes": { "name": "infected-host", "ip": "10.1.1.66" } } }
          ]
      } }
    ]
  }
}
```

## Verify
```
# APIC
moquery -c fvIpAttr
moquery -c fvAEPg -f 'fv.AEPg.isAttrBasedEPg=="yes"'

# Leaf: which EPG / pcTag does the endpoint have now?
show endpoint ip 10.1.1.66
show system internal epm endpoint ip 10.1.1.66      # look at the sclass / pcTag
```
GUI: `uSeg EPG > Operational > Client End-Points` should list the host.

## Gotchas
- uSeg EPG and base EPG **must** use the **same BD**.
- On bare metal, an IP uSeg relies on **IP learning**: check `Limit IP Learning to Subnet` and data-plane learning.
- After you change attributes, the endpoint may need traffic (or an EP flush) before it is reclassified.
