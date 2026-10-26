# Generating `instances` from an inventory at scale

NCM has no autodiscovery ([`multi-vendor-device-list/`](../multi-vendor-device-list/)) —
every device is a hand-written `instances` entry. The single largest scale
complaint in NCM support tickets is exactly this: past roughly 50-100
devices, manually maintaining this list by copy-paste stops working and
starts drifting from the real device inventory (devices decommissioned but
left in the config, new devices forgotten, inconsistent credentials).

This sample shows the pattern, not a product: generate the `instances` block
from whatever already tracks your inventory, rather than hand-maintaining
YAML. `devices.csv` + `generate_conf.py` is a minimal, dependency-free
stand-in — in practice, swap the CSV read for a CMDB export, a NetBox API
call, your Ansible inventory, or similar.

## Files

- `devices.csv` — example inventory: IP, username, auth type (`password` or `key`), and a
  secret reference name (not a real secret — see below).
- `generate_conf.py` — reads the CSV and emits a valid `network_config_management.d/conf.yaml`
  to stdout.
- `conf.yaml` — the actual output of running the script against `devices.csv`, committed here
  so you can see the result without running anything.

## Why the output uses `ENC[]` instead of real credentials

The generated file is meant to be safe to commit to version control and
regenerate on a schedule (e.g. in CI, whenever the inventory source changes).
It emits [`ENC[]` secret-backend
handles](../secrets-management/) rather than literal passwords/keys — actual
secret values are resolved by the Agent at runtime via your configured
`secret_backend_command`, never written to this file.

## Usage

```bash
python3 generate_conf.py devices.csv > conf.yaml
```

Then deploy the generated `conf.yaml` to
`/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml` and restart
the Agent, same as any other sample in this directory. In production, wire
this generation step into whatever already owns your device inventory rather
than running it by hand.
