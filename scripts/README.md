# 🐍 ACI Python Scripts

Plain `requests` scripts, easy to read and change. They work with any APIC, including the free DevNet sandbox.

| Script | What it does |
|---|---|
| [aci_monitor.py](aci_monitor.py) | Fabric + tenant health, critical/major faults, recent audit log. `--watch` mode + JSON-lines logging |
| [endpoint_finder.py](endpoint_finder.py) | Find an endpoint by IP or MAC → tenant / AP / EPG / VLAN / leaf + port |
| [deny_log_reader.py](deny_log_reader.py) | Shows the contract **drop** (and optionally permit) flows logged by the leafs |
| [aci_session.py](aci_session.py) | Shared login helper |

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APIC_URL=https://<apic-ip-or-name>
export APIC_USER=<username>
export APIC_PASS='<password>'
# export APIC_VERIFY_SSL=false   # only for labs with self-signed certs
```
🔒 Never write passwords inside the scripts or commit a `.env` file (it's in `.gitignore`).

## Examples
```bash
python3 aci_monitor.py
python3 aci_monitor.py --watch 60 --jsonl monitor.jsonl
python3 endpoint_finder.py 10.1.1.10
python3 endpoint_finder.py 00:50:56:00:00:01
python3 deny_log_reader.py --limit 50
python3 deny_log_reader.py --permit
```
