# Single device — SSH username/password

The simplest realistic starting point for [Network Configuration Management
(NCM)](https://docs.datadoghq.com/network_monitoring/devices/config_management/):
one device, authenticated with a plain SSH username and password. NCM pulls
the device's running (and, where the vendor supports it, startup)
configuration over SSH on a schedule, then gives you diffing, AI-generated
change summaries, and rollback in the Datadog UI.

NCM is an add-on to [Network Device Monitoring
(NDM)](https://docs.datadoghq.com/network_monitoring/devices/setup/) — the
device must already be monitored via the SNMP integration (see the samples
in the repo root) before NCM can track its configuration.

## The most common mistake this sample prevents

By far the most frequent support issue with NCM is a malformed `conf.yaml`:
`instances` nested incorrectly inside the `ssh:` block, or written as a single
mapping instead of a YAML list (missing the leading `-`). Both produce vague
errors like "no valid instances" or "no SSH configuration found" that don't
point back to the actual indentation problem. This sample's structure —
`init_config` and `instances` as siblings, `instances` as a list — is the
thing to copy exactly, even before you fill in real values.

## Key fields in this config

- `namespace` — must match the namespace the device already uses in NDM (SNMP). Default `default`.
- `min_collection_interval` — seconds between config pulls; default `900` (15 minutes).
- `ssh.known_hosts_path` — path to a real `known_hosts` file containing this device's actual host key.
  See [`known-hosts-setup/`](../known-hosts-setup/) — this is not a placeholder path.
- `instances[].ip_address` — the device's IP; should match the device already visible in NDM.
- `instances[].auth.username` / `auth.password` — SSH credentials for config retrieval.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml`.
2. Replace every `<PLACEHOLDER>`, including `known_hosts_path` with a real, populated file.
3. Restart the Agent (`sudo systemctl restart datadog-agent` or your platform's equivalent).
4. Confirm the device appears with configuration history in the NCM tab of its NDM device page —
   allow up to one `min_collection_interval` for the first pull.
