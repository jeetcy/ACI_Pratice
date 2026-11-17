# Contract Deep Dive: Reading Zoning Rules

## 1. Find the VRF scope (VNID) and the EPG pcTags
**APIC GUI**: `Tenant > EPG > Policy > General` shows the **pcTag**; `Tenant > VRF > Policy` shows the **Segment** (= scope).

**APIC CLI**:
```
moquery -c fvAEPg -f 'fv.AEPg.name=="WEB"' | egrep "dn|pcTag|scope"
moquery -c fvCtx  -f 'fv.Ctx.name=="VRF1"' | egrep "dn|scope|seg"
```
**Leaf CLI**:
```
show system internal epm endpoint ip 10.1.1.10     # shows the sclass (pcTag) + VRF VNID
```

## 2. Show the zoning rules for that VRF
```
leaf101# show zoning-rule scope 2523136
+---------+--------+--------+----------+----------------+---------+---------+------+-----------------+----------------------+
| Rule ID | SrcEPG | DstEPG | FilterID |      Dir       |  operSt |  Scope  | Name |      Action     |       Priority       |
+---------+--------+--------+----------+----------------+---------+---------+------+-----------------+----------------------+
|   4100  | 49153  | 32771  |    5     |     bi-dir     | enabled | 2523136 | WEB  |      permit     |       fully_qual(7)  |
|   4101  | 32771  | 49153  |    6     | uni-dir-ignore | enabled | 2523136 | WEB  |      permit     |       fully_qual(7)  |
|   4099  |   0    |   0    | implicit |    uni-dir     | enabled | 2523136 |      |     deny,log    |   any_any_any(21)    |
+---------+--------+--------+----------+----------------+---------+---------+------+-----------------+----------------------+
```
*(Example only. Your numbers will differ.)*

How to read it:
- **SrcEPG / DstEPG** = pcTags. `0` = any.
- **FilterID** → look it up with `show zoning-filter filter 5`.
- **Dir**: `bi-dir` = consumer→provider; `uni-dir-ignore` = the return direction (from Reverse Filter Ports).
- **Action**: permit / deny / `deny,log` / redirect (PBR).
- **Priority**: lower number = checked first.
- The last rule is the **implicit deny** (any → any).

## 3. Check the filter
```
show zoning-filter filter 5
# FilterId  Name   EtherT  Prot  ... DFromPort  DToPort ...
#   5       5_0    ip      tcp       https      https
```

## 4. Are packets hitting the rule?
```
show system internal policy-mgr stats | grep 4100
```
Run it twice. Does the counter go up?

## 5. One-shot helper
```
contract_parser.py --vrf PROD:VRF1
```
(Available on the leaf in many versions.) It prints the rules with **EPG names** instead of numbers, plus hit counters.

## Common mistakes found here
| What you see | Meaning |
|---|---|
| No rule between the two pcTags | Contract not provided/consumed, or the scope is wrong |
| Rule exists, 0 hits | Traffic is classified into a **different** pcTag (uSeg/ESG/L3Out), or is dropped earlier |
| Filter shows the wrong port/protocol | Filter entry mistake |
| Only a `bi-dir` rule, no return rule | Reverse Filter Ports is off |
