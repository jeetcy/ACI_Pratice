#!/usr/bin/env python3
"""ACI health + fault + audit monitor.

Usage:
  python3 aci_monitor.py                       # one snapshot
  python3 aci_monitor.py --watch 60            # refresh every 60 s
  python3 aci_monitor.py --watch 60 --jsonl monitor.jsonl   # also log every snapshot
"""
import argparse
import json
import time
from datetime import datetime, timezone

from aci_session import Apic, attrs, children

FAULT_QUERY = (
    "/api/class/faultInst.json?query-target-filter="
    'or(eq(faultInst.severity,"critical"),eq(faultInst.severity,"major"))'
    "&order-by=faultInst.lastTransition|desc&page-size={n}"
)
AUDIT_QUERY = "/api/class/aaaModLR.json?order-by=aaaModLR.created|desc&page-size={n}"


def fabric_health(apic):
    data = apic.get("/api/mo/topology/health.json")
    return int(attrs(data[0])["cur"]) if data else None


def tenant_health(apic):
    out = []
    for t in apic.get("/api/class/fvTenant.json?rsp-subtree-include=health"):
        score = next((attrs(c)["cur"] for c in children(t) if "healthInst" in c), "?")
        out.append((attrs(t)["name"], score))
    return sorted(out, key=lambda x: int(x[1]) if str(x[1]).isdigit() else 999)


def faults(apic, n):
    rows = []
    for f in apic.get(FAULT_QUERY.format(n=n)):
        a = attrs(f)
        rows.append({
            "time": a.get("lastTransition", "")[:19],
            "severity": a.get("severity"),
            "code": a.get("code"),
            "dn": a.get("dn"),
            "descr": a.get("descr", "")[:100],
        })
    return rows


def audit(apic, n):
    rows = []
    for m in apic.get(AUDIT_QUERY.format(n=n)):
        a = attrs(m)
        rows.append({
            "time": a.get("created", "")[:19],
            "user": a.get("user"),
            "action": a.get("ind"),
            "object": a.get("affected"),
        })
    return rows


def snapshot(apic, n):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "fabric_health": fabric_health(apic),
        "tenant_health": tenant_health(apic),
        "faults": faults(apic, n),
        "audit": audit(apic, n),
    }


def show(s):
    print(f"\n===== ACI snapshot {s['timestamp']} =====")
    fh = s["fabric_health"]
    flag = "✅" if fh is not None and fh >= 90 else "⚠️"
    print(f"{flag} Fabric health: {fh}")

    print("\nTenant health (worst first):")
    for name, score in s["tenant_health"][:10]:
        print(f"  {score:>4}  {name}")

    print(f"\nCritical/major faults ({len(s['faults'])}):")
    for f in s["faults"]:
        print(f"  {f['time']}  {f['severity']:<8} {f['code']:<6} {f['descr']}")
        print(f"      dn: {f['dn']}")

    print("\nRecent changes (audit log):")
    for a in s["audit"]:
        print(f"  {a['time']}  {a['user']:<12} {a['action']:<14} {a['object']}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--watch", type=int, metavar="SECONDS", help="repeat every N seconds")
    p.add_argument("--jsonl", metavar="FILE", help="append each snapshot as one JSON line")
    p.add_argument("--limit", type=int, default=15, help="number of faults / audit entries (default 15)")
    args = p.parse_args()

    apic = Apic()
    while True:
        s = snapshot(apic, args.limit)
        show(s)
        if args.jsonl:
            with open(args.jsonl, "a") as fh:
                fh.write(json.dumps(s) + "\n")
        if not args.watch:
            break
        time.sleep(args.watch)


if __name__ == "__main__":
    main()
