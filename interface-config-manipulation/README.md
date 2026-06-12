# Interface config manipulation

Real-world links don't always advertise their true speed over SNMP. A sub-rate
metro-Ethernet circuit on a GigE port reports `ifSpeed` = 1 Gbps even though the
carrier only delivers 50/25 Mbps, so any utilization percentage Datadog computes
is wrong. Port-channels have the opposite problem: each member reports its own
speed, under-counting the bundle. This config uses `interface_configs` to override
`in_speed`/`out_speed` on those links, attach interface-level `tags`, and
`disabled: true` to stop monitoring a noisy access port. It shows matching by both
`name` (ifName) and `index` (ifIndex).

## Key fields in this config

- `interface_configs[].match_field` — `name` (matches ifName) or `index` (matches ifIndex).
- `interface_configs[].match_value` — the value to match; **case-sensitive**.
- `in_speed` / `out_speed` — override speeds in **bits/sec**; absent or `0` means no override.
- `interface_configs[].tags` — tags applied only to the matched interface's metrics.
- `disabled: true` — stops monitoring the matched interface(s); default `false`.

When to match by `index` vs `name`: prefer `name` for readability, but switch to
`index` when ifName is unstable across reboots/relabeling (common on aggregates).

## Loader

Uses `loader: core`. `interface_configs` is fully supported on core; no
python-only parameters are used.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/snmp.d/conf.yaml`.
2. Replace placeholders and set `match_value` to your real interface names/indexes.
3. Restart the Agent.
