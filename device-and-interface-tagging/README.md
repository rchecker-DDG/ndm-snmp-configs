# Device- and interface-level tagging

Tags are how you slice NDM data by site, environment, owning team, or cost center,
and there are three distinct places tags come from. This config makes the
distinction explicit so you know where each tag lands:

1. **Instance-wide `tags`** — static key:values applied to the device and *every*
   metric it emits (`site`, `env`, `team`, `cost_center`).
2. **`metric_tags`** — tags derived from *live SNMP values*. Shown in both forms:
   the direct `symbol -> tag` mapping, and the regex-split form that carves one
   symbol (here `sysName`) into multiple tags.
3. **Interface-level `tags`** (via `interface_configs`) — applied only to the
   matched interface's metrics, not the whole device.

`use_device_id_as_hostname: true` is set because custom device tags bind reliably
to the device only when it reports under its NDM device id.

## Key fields in this config

- `tags` — instance-wide; device + all metrics.
- `metric_tags` (direct) — `OID` + `symbol` + `tag`; one SNMP value → one tag.
- `metric_tags` (regex) — `OID` + `symbol` + `match` + `tags` with `\1`, `\2`
  backreferences; one SNMP value → several tags.
- `interface_configs[].tags` — interface-scoped tags only.

## Loader

Uses `loader: core`. All tagging forms shown are supported on core; no python-only
parameters are used.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/snmp.d/conf.yaml`.
2. Replace placeholders; adjust the `match:` regex to your naming convention.
3. Restart the Agent.
