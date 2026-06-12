# Subnet autodiscovery

Instead of listing devices one by one, point the Agent at a CIDR range and it
sweeps the subnet, probes each address, and starts monitoring every device that
responds to the shared community string. This is the right model for access/edge
fleets where devices come and go. `ignored_ip_addresses` keeps known
non-targets (gateways, broadcast, servers) out of the sweep, and the
`discovery_*`/`workers` knobs control sweep cadence and concurrency.

## Key fields in this config

- `network_address` — the CIDR to scan (mutually exclusive with `ip_address`).
- `ignored_ip_addresses` — list of addresses to skip during discovery.
- `discovery_interval` — seconds between full subnet sweeps.
- `discovery_allowed_failures` — consecutive failures before dropping a device.
- `workers` — concurrent device-collection workers.
- `discovery_workers` — concurrent discovery/probe workers (**core-only**).
- `tags` — applied to every device discovered in the range.

## Loader

Uses `loader: core`. `discovery_workers` is a **core-only** parameter, so core is
required here — do not switch this file to `loader: python` without removing it.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/snmp.d/conf.yaml`.
2. Set `network_address` to your real CIDR and fill the other placeholders.
3. Restart the Agent. Discovered devices appear in NDM as the sweep completes.
