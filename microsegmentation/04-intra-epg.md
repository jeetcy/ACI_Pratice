# Intra-EPG Isolation & Intra-EPG Contracts

By default, **all endpoints in the same EPG can talk freely**. Two ways to change that:

## 1. Intra-EPG Isolation: block everything inside the EPG
`EPG > Policy > General > Intra EPG Isolation: Enforced`
- REST: `fvAEPg` attribute `pcEnfPref="enforced"`
- Members can still talk to **other** EPGs through contracts.
- **Bare metal**: the static port uses a **primary + secondary VLAN** (PVLAN-style) encap.
- **VMware VDS**: ACI uses PVLANs on the port group automatically.
- Use cases: backup networks, DMZ servers, VDI desktops, IoT devices.

## 2. Intra-EPG Contract: allow only certain ports inside the EPG
`EPG > Contracts > Add Intra-EPG Contract`
- e.g. web servers in a cluster may talk on **TCP 8443** only.
- When you add one, isolation is enforced automatically and **only** the contract's traffic is allowed.

## Verify
```
show zoning-rule scope <vrf-vnid> | grep <epg-pcTag>
```
With isolation you'll see a **deny** rule from the EPG's pcTag to itself. With an intra-EPG contract you'll see **permit** rules for the allowed ports, then the deny.
