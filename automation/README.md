# 🤖 ACI Automation

## Ansible
| File | What it builds |
|---|---|
| [ansible/build-tenant.yml](ansible/build-tenant.yml) | Tenant, VRF, 3 BDs, 3 EPGs, filters, contracts with logging (3-tier app) |
| [ansible/quarantine.yml](ansible/quarantine.yml) | Puts a host into a **quarantine uSeg EPG** in seconds, or releases it |

```bash
pip install ansible
ansible-galaxy collection install cisco.aci
export APIC_URL=<apic-host> APIC_USER=<user> APIC_PASS='<password>'
ansible-playbook ansible/build-tenant.yml
ansible-playbook ansible/quarantine.yml -e host_ip=10.1.2.45
ansible-playbook ansible/quarantine.yml -e host_ip=10.1.2.45 -e state=absent
```

## Other options
- **Terraform**: [CiscoDevNet/terraform-provider-aci](https://github.com/CiscoDevNet/terraform-provider-aci), and the "Network-as-Code" modules from netascode
- **Python SDKs**: `acitoolkit`, `cobra` (the official SDK)
- **API Inspector** (APIC GUI → your user menu → *Show API Inspector*): do something in the GUI and copy the exact REST call it made. The best way to learn the API!
