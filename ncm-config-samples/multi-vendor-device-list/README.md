# Multi-vendor device list (no autodiscovery)

NCM, as of this writing, has no subnet or network autodiscovery — unlike
NDM's SNMP integration, which can sweep a CIDR range with `network_address`.
Every device NCM should track must be its own explicit `instances` entry.
This is a common point of confusion for teams coming from the NDM/SNMP
samples elsewhere in this repo, where autodiscovery is available.

This sample shows a small, realistic mixed-vendor fleet — a core switch,
edge router, leaf switch, and firewall — as a starting template.

## Key fields in this config

- One `instances[]` entry per physical device — no range/subnet shorthand exists for NCM.
- You do not declare a vendor or profile — NCM detects the device's OS/vendor automatically
  and runs the matching vendor-specific commands over SSH. See
  [`vendor-collection-limitations/`](../vendor-collection-limitations/) for what's supported.
- Mixing `password` and `private_key_file` auth across different instances in the same file
  is normal — each device's credentials are independent.

## When this doesn't scale

Hand-maintaining an `instances` list works fine for a handful of devices.
Past roughly 50-100, manually keeping this file in sync with your device
inventory becomes its own operational burden — see
[`scale-templating/`](../scale-templating/) for a pattern that generates this
block from a CSV/inventory source instead.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml`.
2. This is a filled-in example fleet (IPs `198.51.100.20-23` are from the RFC 5737
   documentation range) — change each `# CHANGE THIS` line to your own devices and credentials.
3. Restart the Agent (`sudo systemctl restart datadog-agent` or your platform's equivalent).
