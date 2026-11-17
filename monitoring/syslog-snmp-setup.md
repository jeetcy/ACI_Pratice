# Sending ACI Logs to Syslog / SIEM + SNMP

## A. Syslog

### Step 1: Create the destination group
`Admin > External Data Collectors > Monitoring Destinations > Syslog > Create`
- Name: `SYSLOG-SIEM`
- Format: `aci` (or `rfc5424` / enhanced, if your version has it)
- Add the destination: IP of the syslog server, port **514**, **minimum severity** (e.g. `information`), facility `local7`, management EPG (`default (Out-of-Band)` or in-band)

### Step 2: Choose WHAT to send (the syslog source)
**Fabric-wide** (switches + APIC):
`Fabric > Fabric Policies > Policies > Monitoring > Common Policy > Callhome/Smart Callhome/SNMP/Syslog/TACACS > Syslog`
- Create a source, min severity `warnings`, include: ✅ Faults ✅ Events ✅ Audit Logs ✅ Session Logs
- Destination group: `SYSLOG-SIEM`

**Access ports**: `Fabric > Access Policies > Policies > Monitoring > default > Callhome/.../Syslog`
**Per tenant**: `Tenant > Policies > Monitoring > (policy) > Callhome/.../Syslog`, then set that monitoring policy on the tenant

### Step 3: Contract permit/deny logs
Enable the **log** directive on your filters ([../microsegmentation/05-contract-logging.md](../microsegmentation/05-contract-logging.md)). These messages also go to syslog through the fabric syslog source.

### Step 4: Verify
- On the syslog server: `tail -f /var/log/aci/*.log`
- Create a harmless test fault (e.g. shut an unused, monitored interface) and watch it arrive.

## B. SNMP
### Step 1: The SNMP policy
`Fabric > Fabric Policies > Policies > Pod > SNMP > default`
- Admin state **Enabled**
- Community: use a strong one (or better, an **SNMPv3 user** with SHA + AES)
- **Client group**: the NMS IP + the management EPG

### Step 2: Apply it to the pod
`Fabric > Fabric Policies > Pods > Policy Groups > default` → SNMP policy = `default`

### Step 3: Traps
`Admin > External Data Collectors > Monitoring Destinations > SNMP` → destination (NMS IP, v2c/v3)
Then add an SNMP source in the same **Common/Monitoring policies** as for syslog.

### Verify
```
snmpwalk -v2c -c <community> <leaf-oob-ip> 1.3.6.1.2.1.1     # from the NMS
```

## C. NTP (do this first! logs are useless with wrong timestamps)
`Fabric > Fabric Policies > Policies > Pod > Date and Time > default` → add NTP servers, management EPG
`System > System Settings > Date and Time` → set the display time zone
Verify on a leaf: `show ntp peer-status`
