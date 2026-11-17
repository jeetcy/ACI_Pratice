# 🧪 ACI Labs (free, using Cisco DevNet)

## Where to practise
1. Go to **developer.cisco.com/site/sandbox** and log in for free.
2. Search for **"ACI Simulator Always-On"**. The URL and login are shown on the sandbox page.
3. It's a **simulator** shared with other users:
   - ✅ The GUI, policy model, REST API, moquery, Ansible and Python all work.
   - ❌ No real data plane, so endpoint learning, zoning-rule hits and contract logs won't show real traffic. For those, use a **reservable** ACI sandbox, your company lab, or dCloud.
   - Name everything with your initials (e.g. `JC-PROD`) and **delete it when you're done**.

## Labs
| # | Lab | Skills |
|---|---|---|
| 1 | [Explore the fabric](#lab-1-explore-the-fabric) | GUI, inventory, moquery, API Inspector |
| 2 | [Build a tenant by hand](#lab-2-build-a-tenant-by-hand) | VRF, BD, EPG, contracts |
| 3 | [Same tenant with Ansible](#lab-3-same-tenant-with-ansible) | Automation |
| 4 | [Quarantine with uSeg EPG](#lab-4-quarantine-with-a-useg-epg) | Microsegmentation |
| 5 | [ESG design](#lab-5-esg-design) | Microsegmentation (modern) |
| 6 | [Monitoring with Python](#lab-6-monitoring-with-python) | Faults, health, audit log |
| 7 | [Break & fix: F0467](#lab-7-break--fix-f0467) | Troubleshooting access policies |
| 8 | [Syslog destination](#lab-8-syslog-destination) | Logs |

---
### Lab 1: Explore the fabric
1. `Fabric > Inventory > Fabric Membership`: list every node ID, role and TEP.
2. `System > Dashboard`: note the fabric health score.
3. Turn on **API Inspector** (top right → user menu). Click on any tenant and see the API calls appear.
4. SSH to the APIC and run `acidiag fnvread`, `moquery -c fvTenant | grep name`, `moquery -c faultInst -f 'fault.Inst.severity=="critical"' | grep descr`.
✅ Write down: How many leafs/spines? What's the lowest-health tenant?

### Lab 2: Build a tenant by hand
Build in the GUI: tenant `XX-PROD`, VRF `VRF1`, BDs `BD-WEB`, `BD-APP`, `BD-DB` with gateways 10.1.1.1/24, 10.1.2.1/24 and 10.1.3.1/24, AP `APP1`, EPGs WEB/APP/DB, and contracts as in [microsegmentation/06-design-example.md](../microsegmentation/06-design-example.md).
✅ Check: `Tenant > Application Profile > Topology` shows the EPGs connected by contracts.

### Lab 3: Same tenant with Ansible
Delete `XX-PROD`. Change `tenant:` in [automation/ansible/build-tenant.yml](../automation/ansible/build-tenant.yml) to `XX-PROD`, then run it.
✅ Compare the result with Lab 2. Run it a second time. Nothing should change (that's called **idempotency**).

### Lab 4: Quarantine with a uSeg EPG
Run [quarantine.yml](../automation/ansible/quarantine.yml) with `-e host_ip=10.1.2.45 -e tenant=XX-PROD`.
✅ Check: `moquery -c fvIpAttr` shows the IP; the uSeg EPG has no contracts. Then release it with `-e state=absent`.

### Lab 5: ESG design
Create `ESG-WEB` (EPG selector → WEB), `ESG-PCI` (IP selector 10.1.3.128/25), and `ESG-QUARANTINE`. Move the contracts from the EPGs to the ESGs.
✅ Check: `moquery -c fvESg`, `moquery -c fvEPSelector`. Draw the design in this repo!

### Lab 6: Monitoring with Python
Run [scripts/aci_monitor.py](../scripts/aci_monitor.py) against the sandbox. Then make a change (create a BD) and run it again.
✅ Your change appears in the **audit log** section with your username.

### Lab 7: Break & fix: F0467
1. Create a VLAN pool with VLANs 100–110, a physical domain, and an AAEP.
2. On EPG WEB, add the domain and a static port with **VLAN 200** (outside the pool!).
3. Find the fault. Write down its code, DN, and description.
4. Fix it, and watch the fault go to *raised-clearing* and then *retaining*.
✅ Add the story to [troubleshooting/my-log.md](../troubleshooting/my-log.md).

### Lab 8: Syslog destination
Follow [monitoring/syslog-snmp-setup.md](../monitoring/syslog-snmp-setup.md) to create a syslog destination group and source. (Use a fake IP if you have no reachable server. The goal is to learn the GUI path.)
✅ Find the same config with `moquery -c syslogRemoteDest`.
