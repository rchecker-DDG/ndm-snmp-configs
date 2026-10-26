#!/usr/bin/env python3
"""Generate an NCM instances block from a device inventory CSV.

NCM has no autodiscovery (see multi-vendor-device-list/) — past roughly
50-100 devices, hand-maintaining `instances:` by copy-pasting entries stops
scaling and becomes its own source of drift against the real inventory. This
script is a minimal, dependency-free pattern for generating the YAML from
whatever already tracks your device inventory (here, a CSV; adapt the read
side to a CMDB export, NetBox, Ansible inventory, etc).

This intentionally does NOT write real secrets into the generated file --
it emits ENC[] handles (see ../secrets-management/) so the output is safe to
commit to version control, with actual secret values resolved by the Agent
at runtime via your configured secret_backend_command.

Usage:
    python3 generate_conf.py devices.csv > conf.yaml
"""
import csv
import sys


HEADER = """\
init_config:
  namespace: default
  min_collection_interval: 900
  ssh:
    timeout: 30
    known_hosts_path: /etc/datadog-agent/.ssh/known_hosts
    insecure_skip_verify: false

instances:
"""


def render_instance(row: dict) -> str:
    lines = [f"  - ip_address: {row['ip_address']}", "    auth:", f"      username: {row['username']}"]
    if row["auth_type"].strip().lower() == "key":
        lines.append(f"      private_key_file: ENC[{row['secret_ref']}]")
    else:
        lines.append(f"      password: ENC[{row['secret_ref']}]")
    return "\n".join(lines)


def main(csv_path: str) -> None:
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    sys.stdout.write(HEADER)
    for row in rows:
        sys.stdout.write(render_instance(row) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <devices.csv>", file=sys.stderr)
        sys.exit(1)
    main(sys.argv[1])
