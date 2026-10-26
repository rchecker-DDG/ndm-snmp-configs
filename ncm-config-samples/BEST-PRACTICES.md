# NCM configuration best practices &amp; troubleshooting checklist

A consolidated checklist drawn from recurring patterns in Network
Configuration Management (NCM) support cases. Fully anonymized — every item
below is abstracted to the general scenario/vendor-family level; no customer
names, hostnames, IP addresses, or org-identifying details are included.

## 1. Get the YAML structure right first

The single most common NCM support issue is not a credentials or network
problem — it's a malformed `conf.yaml`. The two recurring mistakes:

- `instances` nested inside the `ssh:` block instead of being a sibling of `init_config`.
- `instances` written as a single mapping instead of a YAML **list** (missing the leading `-`).

Both produce vague errors ("no valid instances," "no SSH configuration
found") that don't point back to the actual indentation problem. Copy the
structure from [`single-device-ssh-password/`](single-device-ssh-password/)
exactly before customizing values.

## 2. Populate `known_hosts` before you need it

`known_hosts_path` must point to a real, populated OpenSSH `known_hosts`
file containing the device's actual host key — not an empty placeholder.
Use `ssh-keyscan`, then verify the fingerprint out-of-band before trusting
it. See [`known-hosts-setup/`](known-hosts-setup/) for the full pattern, and
treat `insecure_skip_verify: true` as a temporary lab-only setting, not a
production shortcut.

## 3. Diagnose SSH handshake failures as a transport issue, not a credentials issue

"No supported methods remain" or "no common algorithm" errors mean the
device and the Agent couldn't agree on a cipher/key-exchange/host-key
algorithm — common on older or security-hardened devices. Confirm basic
connectivity works first (can you `ssh` manually with the same credentials?)
before reaching for the
[`custom-ssh-algorithms/`](custom-ssh-algorithms/) override, and remember
those overrides are global to the file, not per-device.

## 4. There is no autodiscovery — plan your device list accordingly

Every device needs its own `instances` entry
([`multi-vendor-device-list/`](multi-vendor-device-list/)). For fleets past
roughly 50-100 devices, generate this list from your existing inventory
source instead of hand-maintaining it —
see [`scale-templating/`](scale-templating/).

## 5. A missing startup config may be expected, not broken

Not every supported vendor/OS exposes both running and startup config
collection. Before treating a missing startup config as a bug, confirm the
device/vendor is on Datadog's current supported list and check with support
if you expected otherwise — see
[`vendor-collection-limitations/`](vendor-collection-limitations/).

## 6. Scope the SSH account deliberately, especially under AAA/TACACS+

If your network team restricts CLI access via command authorization, scope
NCM's account to read-only/show-equivalent access for backup-only use cases,
and only grant write/commit-capable access if you intend to use rollback.
Validate the scoped account against one device before rolling the role out
fleet-wide — an under-scoped account fails silently (it just can't fetch
anything), which is easy to misdiagnose as an SSH or `known_hosts` problem.
See [`least-privilege-service-account/`](least-privilege-service-account/).

## 7. Keep credentials out of plaintext conf.yaml

Use the Agent's secrets management (`ENC[]` + a `secret_backend_command`)
for real deployments, especially if `conf.yaml` is checked into version
control. See [`secrets-management/`](secrets-management/).

## 8. Give the first collection cycle time, and know where to look

Allow at least one full `min_collection_interval` (default 15 minutes)
before assuming a new device isn't working. Configuration history for a
device shows up in the NCM tab of its NDM device page — confirm the device
is already visible and healthy in NDM before troubleshooting NCM on top of
it, since an NCM failure caused by an underlying NDM/device issue can look
like an NCM-specific bug.

## Further reading

- [NCM official documentation](https://docs.datadoghq.com/network_monitoring/devices/config_management/)
- [NDM setup](https://docs.datadoghq.com/network_monitoring/devices/setup/) (prerequisite for NCM)
- [Agent secrets management](https://docs.datadoghq.com/agent/configuration/secrets-management/)
