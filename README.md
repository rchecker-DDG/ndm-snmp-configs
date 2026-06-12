# NDM SNMP `conf.yaml` sample library

A graded set of ready-to-adapt `conf.yaml` files for Datadog
[Network Device Monitoring](https://docs.datadoghq.com/network_monitoring/devices/setup)
(NDM) — the SNMP integration. The `conf.yaml` is what the Datadog Agent's SNMP
check reads from `/etc/datadog-agent/conf.d/snmp.d/`: it tells the Agent which
devices to poll, how to authenticate, and how to tag, enrich, and shape the data.

Each sample is a complete, standalone file with inline comments explaining the
non-obvious fields, `<ANGLE_BRACKET>` placeholders for anything secret or
environment-specific, and its own README. Every file is grounded in the upstream
[`conf.yaml.example`](https://github.com/DataDog/integrations-core/blob/master/snmp/datadog_checks/snmp/data/conf.yaml.example).

## Samples

| Directory | Use case | Headline feature | Details |
|---|---|---|---|
| [`single-device-v2c/`](single-device-v2c/) | Single device, SNMP v2c | Simplest realistic starting point: one device, community string, profile | [README](single-device-v2c/README.md) |
| [`single-device-v3-authpriv/`](single-device-v3-authpriv/) | Single device, SNMP v3 (authPriv) | Full v3 credential block: `authProtocol` + `privProtocol` | [README](single-device-v3-authpriv/README.md) |
| [`subnet-autodiscovery/`](subnet-autodiscovery/) | Subnet autodiscovery | `network_address` CIDR sweep with `ignored_ip_addresses`, `discovery_*`, workers | [README](subnet-autodiscovery/README.md) |
| [`interface-config-manipulation/`](interface-config-manipulation/) | Interface config manipulation | `in_speed`/`out_speed` overrides, interface tags, `disabled` — by name and index | [README](interface-config-manipulation/README.md) |
| [`device-and-interface-tagging/`](device-and-interface-tagging/) | Device- and interface-level tagging | Instance `tags`, regex-split `metric_tags`, interface-level tags | [README](device-and-interface-tagging/README.md) |
| [`full-capability-reference/`](full-capability-reference/) | Full-capability reference | "Kitchen sink": globals, ping, v3, topology, VPN, custom metrics, interfaces | [README](full-capability-reference/README.md) |

## Where the file goes

For every sample, the destination is the same:

```
/etc/datadog-agent/conf.d/snmp.d/conf.yaml
```

Then restart the Agent (`sudo systemctl restart datadog-agent`, or your platform's
equivalent).

## Loader: core vs python

Samples default to `loader: core` (the recommended Go-based collector). A few
parameters are **python-only** — if a config uses one, it must set `loader: python`
and say so in a comment. The `full-capability-reference` sample lists which
parameters are python-only and which are mutually exclusive.

## ⚠️ These are examples — validate before production

Every file ships with placeholders. Replace **all** `<ANGLE_BRACKET>` values,
substitute real interface names/indexes, and validate against a non-production
device before rolling out widely. Treat community strings and v3 keys as secrets.

## Generate a custom config

Need something these samples don't cover? The companion
[`ndm-snmp-conf-wizard`](https://github.com/rchecker-DDG/ndm-snmp-conf-wizard)
repo is an interactive CLI that interviews you and emits a valid `conf.yaml`.
