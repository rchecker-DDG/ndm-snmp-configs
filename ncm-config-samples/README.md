# NCM (Network Configuration Management) sample library

A set of ready-to-adapt `conf.yaml` files for Datadog [Network Configuration
Management (NCM)](https://docs.datadoghq.com/network_monitoring/devices/config_management/) —
the config backup, diff, AI-summary, and rollback add-on for [Network Device
Monitoring (NDM)](https://docs.datadoghq.com/network_monitoring/devices/setup/).
NCM requires the device to already be monitored via NDM's SNMP integration;
see the SNMP samples in the repo root for that half of the setup.

New to NCM? See [`ARCHITECTURE.md`](ARCHITECTURE.md) first — a diagram of
where every component lives (device, Agent, Datadog backend, Private Action
Runner) and a step-by-step walkthrough of the collection flow, from the
Agent connecting over SSH to the config landing in the UI.

Each scenario here is grounded in a real, recurring pattern seen in NCM
support cases — fully anonymized; no customer names, hostnames, IP addresses,
or org-identifying details are reflected anywhere in this directory.

## Samples

| Directory | Scenario | What it addresses |
|---|---|---|
| [`single-device-ssh-password/`](single-device-ssh-password/) | Single device, SSH password | The simplest correct starting point — and the config structure that prevents the #1 support issue (malformed `instances` nesting) |
| [`single-device-ssh-key/`](single-device-ssh-key/) | Single device, SSH private key | Key-based auth instead of a password; clears up password/key field confusion |
| [`known-hosts-setup/`](known-hosts-setup/) | `known_hosts` setup | How to actually populate `known_hosts_path`, and the `insecure_skip_verify` tradeoff |
| [`multi-vendor-device-list/`](multi-vendor-device-list/) | Multi-vendor device list | NCM has no autodiscovery — explicit instances for a mixed Cisco/Juniper/Arista/Fortinet fleet |
| [`custom-ssh-algorithms/`](custom-ssh-algorithms/) | Custom SSH algorithms | Fixing SSH handshake failures against legacy/hardened devices with non-default cipher suites |
| [`vendor-collection-limitations/`](vendor-collection-limitations/) | Running vs. startup config | Why some devices only show a running config, and how to tell that apart from a real failure |
| [`least-privilege-service-account/`](least-privilege-service-account/) | Least-privilege service account | Scoping the SSH account NCM uses when your AAA/TACACS+ policy requires command authorization |
| [`secrets-management/`](secrets-management/) | Secrets management | Keeping SSH credentials out of plaintext `conf.yaml` using the Agent's secret backend |
| [`scale-templating/`](scale-templating/) | Scale templating | Generating `instances` from an inventory source instead of hand-maintaining it past ~50-100 devices |

See also [`BEST-PRACTICES.md`](BEST-PRACTICES.md) for a consolidated
troubleshooting checklist drawn from the same support-case research.

## Where the file goes

For every sample, the destination is the same:

```
/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml
```

Then restart the Agent (`sudo systemctl restart datadog-agent`, or your
platform's equivalent).

## ⚠️ These are examples — validate before production

Every sample is a filled-in, working example rather than a bracketed
template — IPs use RFC 5737 documentation ranges (`192.0.2.0/24`,
`198.51.100.0/24`, `203.0.113.0/24`) and hostnames use RFC 2606 reserved
domains (`.example.net`), so nothing resembles real production infrastructure.
Lines you need to change are marked `# CHANGE THIS`. Replace **all** of
them with your own device IPs and credentials, validate against a
non-production device first, and treat SSH credentials and private keys as
secrets — see [`secrets-management/`](secrets-management/) before putting
real credentials in a committed file.
