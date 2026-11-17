# Faults, Health Scores, Events & Audit Logs

## Faults
**Severities**: critical · major · minor · warning · info · cleared

**Fault lifecycle**
```
condition detected → Soaking ──(still there after the soak timer)──► Raised
                                                                       │ condition clears
                                                                       ▼
                                Retaining ◄──(clearing timer)── Raised-Clearing
                                    │ (retention timer ends)
                                    ▼
                                 deleted
```
- **Soaking** stops short glitches from creating noise.
- **Retaining** keeps cleared faults for a while, so you can see what happened.
- You can **acknowledge** a fault, but that doesn't fix it.

**Where**: `System > Faults`, or the **Faults** tab of any object (tenant, EPG, leaf, interface).

**Query**:
```
# APIC CLI
moquery -c faultInst -f 'fault.Inst.severity=="critical"'
moquery -c faultInst -f 'fault.Inst.code=="F0467"'

# REST
GET /api/class/faultInst.json?query-target-filter=eq(faultInst.severity,"critical")
```
A fault's **DN** tells you exactly which object it belongs to, e.g.
`uni/tn-PROD/ap-APP1/epg-WEB/.../fault-F0467` → the problem is on EPG WEB in tenant PROD.

## Health scores
- **0–100** (100 = perfect). Every object has one, and it **rolls up**: interface → leaf → pod → fabric, and EPG → AP → tenant.
- Faults reduce the score. With the default health score policy, critical faults weigh the most, then major, minor and warning.
- **Dashboards**: `System > Dashboard`, `Tenants > (tenant) > Dashboard`.

```
GET /api/mo/topology/health.json                                  # overall fabric health
GET /api/class/fvTenant.json?rsp-subtree-include=health           # every tenant's health
GET /api/class/topSystem.json?rsp-subtree-include=health          # every node's health
```

## Events
`System > History > Events`, or `History > Events` on any object.
```
moquery -c eventRecord -f 'event.Record.created>"2026-11-17T10:00"'
```

## Audit logs
`System > History > Audit Log`, or `History > Audit Log` on an object.
Shows **user, time, object, and what changed** (created / modified / deleted).
```
moquery -c aaaModLR -f 'aaa.ModLR.user=="admin"'
GET /api/class/aaaModLR.json?order-by=aaaModLR.created|desc&page-size=20
```

## Other monitoring tools
| Tool | Use |
|---|---|
| **Atomic counters** | Count packets between two endpoints/EPGs, to find exactly where drops happen |
| **SPAN / ERSPAN** (access, fabric, tenant) | Copy traffic to an analyzer |
| **NetFlow** | Flow records to a collector |
| **Traceroute (Visibility & Troubleshooting)** | Path through the fabric between endpoints |
| **Nexus Dashboard Insights** | Anomaly detection, flow telemetry, compliance, change analysis |
| **Streaming telemetry** | Push model, to Kafka/Grafana-type stacks via Nexus Dashboard |
