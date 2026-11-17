#!/usr/bin/env python3
"""Show contract drop (or permit) flows logged by the leaf switches.

These records exist only when contract logging is active (the implicit deny is
logged by default; for permits, enable the 'log' directive on the filter).
Field names can differ between versions, so missing ones are shown as '-'.

Usage:
  python3 deny_log_reader.py               # L3 drops
  python3 deny_log_reader.py --permit      # L3 permits (needs the log directive)
  python3 deny_log_reader.py --ip 10.1.2.45
"""
import argparse

from aci_session import Apic, attrs

PROTO = {"1": "icmp", "6": "tcp", "17": "udp", "icmp": "icmp", "tcp": "tcp", "udp": "udp"}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--permit", action="store_true", help="show permit flows instead of drops")
    p.add_argument("--ip", help="only flows where this IP is source or destination")
    p.add_argument("--limit", type=int, default=30)
    args = p.parse_args()

    cls = "acllogPermitL3Flow" if args.permit else "acllogDropL3Flow"
    query = f"/api/node/class/{cls}.json?page-size={args.limit}"
    if args.ip:
        query += f'&query-target-filter=or(eq({cls}.srcIp,"{args.ip}"),eq({cls}.dstIp,"{args.ip}"))'

    rows = [attrs(r) for r in Apic().get(query)]
    word = "PERMIT" if args.permit else "DROP"
    if not rows:
        print(f"No {word} flow records found.")
        return

    print(f"{'node':<14}{'src':<18}{'dst':<18}{'proto':<7}{'dport':<7}{'srcEPG':<16}{'dstEPG':<16}")
    print("-" * 96)
    for a in rows:
        node = a.get("dn", "").split("/sys/")[0].replace("topology/", "")
        proto = PROTO.get(str(a.get("protocol", "-")), a.get("protocol", "-"))
        print(f"{node:<14}{a.get('srcIp', '-'):<18}{a.get('dstIp', '-'):<18}{proto:<7}"
              f"{a.get('dstPort', '-'):<7}{a.get('srcEpgName', '-'):<16}{a.get('dstEpgName', '-'):<16}")
    print(f"\n{len(rows)} {word} flow(s). ✅ Use this to prove your microsegmentation rules work.")


if __name__ == "__main__":
    main()
