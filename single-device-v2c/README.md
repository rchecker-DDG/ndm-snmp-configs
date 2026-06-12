# Single device — SNMP v2c, profile-based

The simplest realistic starting point: monitor one device that speaks SNMP v2c
with a read community string. A `profile` maps the device's `sysObjectID` to the
right set of metrics and metadata; if you omit it, the Agent auto-detects a
matching profile. `use_device_id_as_hostname` makes the device report under its
NDM device id so the `site`/`env` tags bind cleanly to it. This is the template
to copy when you just need one device flowing into NDM quickly.

## Key fields in this config

- `ip_address` — the single target device (mutually exclusive with `network_address`).
- `snmp_version: 2` — v2c; pairs with `community_string`.
- `community_string` — the v2c read community.
- `profile` — optional; maps the device to a metric/metadata set, auto-detected if omitted.
- `tags` — instance-wide tags applied to the device and every metric it emits.

## Loader

Uses `loader: core` (the recommended Go collector). No python-only parameters
are present, so there is no reason to switch to `loader: python`.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/snmp.d/conf.yaml`.
2. Replace every `<PLACEHOLDER>`.
3. Restart the Agent (`sudo systemctl restart datadog-agent` or your platform's equivalent).
