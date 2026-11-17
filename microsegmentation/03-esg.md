# Endpoint Security Groups (ESG), APIC 5.0+

## Why ESGs?
EPGs mix **networking** (VLAN, BD, port) with **security**. ESGs split them up:
- **EPGs** = how endpoints attach to the network.
- **ESGs** = the security groups that contracts are applied to.

An ESG is scoped to **one VRF** and can contain endpoints from **many BDs**.

## Selectors (how endpoints are put in an ESG)
| Selector | Example | Version |
|---|---|---|
| **EPG selector** | All endpoints of EPG `WEB` | 5.0 |
| **IP subnet selector** | `10.1.1.0/24` or a single `/32` | 5.0 |
| **Tag selector** | Endpoints with tag `env=prod` (IP or MAC tags) | 5.2 |
| **Policy tag selector** | BDs/EPGs/subnets with a policy tag | 5.2 |

## Rules
- Contracts between **ESGs** work like contracts between EPGs (provider / consumer).
- Once an endpoint belongs to an ESG, the **ESG's** contracts are what gets enforced for it. Don't keep the old EPG contracts and expect both to apply.
- ESG-to-EPG contracts are **not** supported (except special cases like L3Out external EPGs and vzAny). Plan a migration: map EPGs into ESGs with **EPG selectors** first, then move the contracts.
- Intra-ESG isolation is available (`Enforced`).

## GUI
`Tenants > PROD > Application Profiles > APP1 > Endpoint Security Groups > Create`
1. Name `ESG-PCI`, VRF `VRF1`
2. Selectors → IP Subnet → `10.20.0.0/24`
3. Contracts → Provided: `PCI-DB-1433`

## REST API (POST to `/api/mo/uni/tn-PROD/ap-APP1.json`)
```json
{
  "fvESg": {
    "attributes": { "name": "ESG-PCI" },
    "children": [
      { "fvRsScope": { "attributes": { "tnFvCtxName": "VRF1" } } },
      { "fvEPSelector": { "attributes": { "matchExpression": "ip=='10.20.0.0/24'" } } },
      { "fvRsProv": { "attributes": { "tnVzBrCPName": "PCI-DB-1433" } } }
    ]
  }
}
```

## Verify
```
moquery -c fvESg
moquery -c fvEPSelector
# Leaf: the endpoint's sclass should now be the ESG's pcTag
show system internal epm endpoint ip 10.20.0.15
show zoning-rule scope <vrf-vnid>
```
