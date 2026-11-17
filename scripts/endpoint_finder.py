#!/usr/bin/env python3
"""Find where an endpoint lives in the ACI fabric.

Usage:
  python3 endpoint_finder.py 10.1.1.10
  python3 endpoint_finder.py 00:50:56:00:00:01
"""
import argparse
import re

from aci_session import Apic, attrs, children

MAC_RE = re.compile(r"^([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}$")


def parse_epg(dn):
    """uni/tn-PROD/ap-APP1/epg-WEB/cep-00:50:56:... -> ('PROD', 'APP1', 'WEB')"""
    m = re.search(r"uni/tn-([^/]+)/ap-([^/]+)/epg-([^/]+)/", dn)
    if m:
        return m.groups()
    m = re.search(r"uni/tn-([^/]+)/", dn)  # e.g. L3Out / other parents
    return (m.group(1) if m else "?", "-", dn.split("/cep-")[0].split("/")[-1])


def pretty_path(tdn):
    """topology/pod-1/paths-101/pathep-[eth1/10] -> 'leaf 101 eth1/10'"""
    m = re.search(r"paths-(\d+)/pathep-\[(.+)\]", tdn)
    if m:
        return f"leaf {m.group(1)} {m.group(2)}"
    m = re.search(r"protpaths-(\d+-\d+)/pathep-\[(.+)\]", tdn)
    if m:
        return f"vPC leafs {m.group(1)} {m.group(2)}"
    return tdn


def find_ceps(apic, key):
    sub = "&rsp-subtree=children&rsp-subtree-class=fvRsCEpToPathEp,fvIp"
    if MAC_RE.match(key):
        mac = key.replace("-", ":").upper()
        return apic.get(f'/api/class/fvCEp.json?query-target-filter=eq(fvCEp.mac,"{mac}"){sub}')
    # IP: look in fvIp (covers endpoints with several IPs), then fetch the parent fvCEp
    ceps = []
    for ip in apic.get(f'/api/class/fvIp.json?query-target-filter=eq(fvIp.addr,"{key}")'):
        parent = attrs(ip)["dn"].rsplit("/ip-[", 1)[0]
        ceps += apic.get(f"/api/mo/{parent}.json?rsp-subtree=children&rsp-subtree-class=fvRsCEpToPathEp,fvIp")
    if not ceps:  # older versions: primary IP on fvCEp
        ceps = apic.get(f'/api/class/fvCEp.json?query-target-filter=eq(fvCEp.ip,"{key}"){sub}')
    return ceps


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("key", help="IP address or MAC address")
    args = p.parse_args()

    apic = Apic()
    ceps = find_ceps(apic, args.key)
    if not ceps:
        print(f"❌ Endpoint {args.key} not found. (Silent host? Wrong VRF? See troubleshooting/endpoint-deep-dive.md)")
        return

    for cep in ceps:
        a = attrs(cep)
        tenant, ap, epg = parse_epg(a["dn"])
        ips = [attrs(c)["addr"] for c in children(cep) if "fvIp" in c] or [a.get("ip", "-")]
        paths = [pretty_path(attrs(c)["tDn"]) for c in children(cep) if "fvRsCEpToPathEp" in c]
        print("✅ Endpoint found")
        print(f"   MAC     : {a.get('mac')}")
        print(f"   IP(s)   : {', '.join(ips)}")
        print(f"   Tenant  : {tenant}")
        print(f"   App Prof: {ap}")
        print(f"   EPG     : {epg}")
        print(f"   Encap   : {a.get('encap')}")
        print(f"   Location: {', '.join(paths) or '-'}")
        print(f"   DN      : {a['dn']}\n")


if __name__ == "__main__":
    main()
