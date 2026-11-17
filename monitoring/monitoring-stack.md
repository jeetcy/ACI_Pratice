# Simple Home-Lab Monitoring Stack

```
 ACI fabric ──syslog udp/514──► Linux VM (rsyslog) ──► /var/log/aci/*.log ──► grep / Graylog / ELK / Splunk
     ▲
     └──REST API (every 60 s)── scripts/aci_monitor.py ──► health + faults + audit log ──► aci_monitor.jsonl
```

## 1. rsyslog receiver (Ubuntu)
`/etc/rsyslog.d/10-aci.conf`
```
module(load="imudp")
input(type="imudp" port="514" ruleset="aci")

template(name="AciFile" type="string" string="/var/log/aci/%HOSTNAME%.log")
ruleset(name="aci") {
  action(type="omfile" dynaFile="AciFile")
}
```
```bash
sudo mkdir -p /var/log/aci && sudo systemctl restart rsyslog
```

## 2. Handy one-liners
```bash
grep -h "\[F0467\]" /var/log/aci/*.log                    # one fault code
grep -hE "\]\[critical\]|\]\[major\]" /var/log/aci/*.log   # critical + major faults
grep -h "aaaModLR\|deleted" /var/log/aci/*.log            # changes
tail -f /var/log/aci/*.log | grep --line-buffered -i deny # live contract drops
```

## 3. API poller
```bash
pip install requests
export APIC_URL=https://<apic> APIC_USER=<user> APIC_PASS='<password>'
python3 scripts/aci_monitor.py --watch 60 --jsonl aci_monitor.jsonl
```
See [../scripts/README.md](../scripts/README.md).

## 4. Next level
- **Graylog / ELK / Splunk** dashboards on the syslog data
- **Nexus Dashboard Insights** for full ACI telemetry
- Alert rules: any new **critical** fault, fabric health < 90, any **audit delete** on a contract or EPG
