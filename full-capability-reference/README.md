# Full-capability reference ("kitchen sink")

A single, valid core-loader file that exercises as many parameters as can coexist:
`init_config` globals (`oid_batch_size`, `min_collection_interval`,
`global_metrics`) plus a `ping` block; and one SNMP v3 (authPriv) instance with a
`profile`, topology and VPN collection, a custom table `metrics` definition, scalar
`metric_tags`, `interface_configs` (speed overrides + tags + disable), and
instance-wide device `tags`. Use it as a lookup for "where does field X go and what
does it look like" rather than as a starter you deploy verbatim.

## Key fields in this config

- `init_config`: `loader: core`, `use_device_id_as_hostname`, `oid_batch_size`,
  `min_collection_interval` (core-only), `global_metrics`, `ping` (+ `linux.use_raw_socket`).
- Instance connection: `ip_address`, `port`, `snmp_version: 3`, `timeout`, `retries`.
- v3 auth: `user`, `authProtocol`, `authKey`, `privProtocol`, `privKey`, `context_name`.
- Behavior: `profile`, `use_global_metrics`, `collect_topology`, `collect_vpn`, `tags`.
- Custom data: `metrics` (table with `metric_tags`), device-level `metric_tags`.
- Interfaces: `interface_configs` with `in_speed`/`out_speed`, `tags`, `disabled`.

## Deliberately omitted (and why)

- `network_address` — mutually exclusive with `ip_address` (used here).
- `loader: python` and the python-only params it would enable:
  `refresh_oids_cache_interval`, `optimize_mib_memory_usage`, `mibs_folder`,
  `ignore_nonincreasing_oid` (init_config); `enforce_mib_constraints`,
  `bulk_threshold` (instance); `privProtocol: 3DES`.

To use any python-only parameter, set `loader: python` and flag it in a comment.

## Loader

Uses `loader: core`. Every field present is core-compatible. The block at the
bottom of `conf.yaml` lists what was left out because it is python-only or
mutually exclusive.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/snmp.d/conf.yaml`.
2. Replace placeholders; trim the sections you don't need.
3. Restart the Agent.
