# 3. Access Policies (the part everyone gets wrong!)

Access policies tell ACI **which ports** on **which leafs** can use **which VLANs**.

## The chain (learn this by heart)
```
VLAN Pool ──► Domain (Physical / L3 / VMM) ──► AAEP ──► Interface Policy Group ──► Interface Profile ──► Switch Profile
  (VLANs)      (who can use them)            (glue)    (port settings: LACP,     (which ports,          (which leafs)
                                                         speed, CDP, LLDP)        e.g. eth1/10)
                                                 ▲
EPG ── is linked to the same Domain ─────────────┘
```

| Object | Purpose |
|---|---|
| **VLAN Pool** | Range of VLANs (static or dynamic allocation) |
| **Domain** | Physical, L3 (for L3Out), L2 external, or VMM (vCenter). Links to a VLAN pool. |
| **AAEP** (Attachable Access Entity Profile) | Connects domains to interfaces |
| **Interface Policy Group** | Access port, port-channel (PC) or vPC settings |
| **Interface Profile** | Port selectors, e.g. `eth1/10` |
| **Switch Profile** | Leaf selectors, e.g. node 101–102 |

## ❗ The most common ACI fault: F0467
If the EPG's VLAN is **not** in the VLAN pool → domain → AAEP chain for that port, the EPG binding fails with **fault F0467** (e.g. *invalid-vlan*, *invalid-path*, or *encap-already-in-use*).

**Fix checklist**
1. Does the **EPG** have the **domain** attached?
2. Is that **VLAN** inside the domain's **VLAN pool**?
3. Is the **domain** attached to the **AAEP**?
4. Is the **AAEP** attached to the **interface policy group** used on that port?
5. Is the **interface profile** linked to the **switch profile** for that leaf?

## vPC
- Create a **vPC Explicit Protection Group** (the leaf pair, e.g. 101+102).
- Use a **vPC interface policy group** + **LACP active** port-channel policy.
- Check: `show vpc brief`, `show port-channel summary` on the leaf.
