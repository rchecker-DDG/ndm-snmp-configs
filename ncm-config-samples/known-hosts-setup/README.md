# known_hosts setup and the insecure_skip_verify tradeoff

`known_hosts_path` is a recurring point of confusion in NCM setups: it has to
be a real, populated OpenSSH `known_hosts` file — the exact format `ssh`
itself maintains — containing the actual host key(s) of the devices NCM will
connect to. It is not a placeholder path the Agent creates or fills in for
you, and an empty or missing file will fail host-key verification.

## Populating known_hosts

From a host that can already reach the device over SSH:

```bash
ssh-keyscan -H <DEVICE_IP> >> /etc/datadog-agent/.ssh/known_hosts
```

**Important:** `ssh-keyscan` retrieves whatever key the device presents right
now — it does not verify the key is authentic. Before trusting the result,
confirm the fingerprint out-of-band: compare it against the device's console
output, a vendor management tool, or a change record. This is the same trust
model as the first time you `ssh` into a new host manually and get prompted
to confirm a fingerprint — `known_hosts_path` is just doing that
non-interactively.

Make sure the file is readable by the Agent's user (typically `dd-agent`), and
keep it updated when a device's host key legitimately changes (e.g. after a
hardware replacement or OS reinstall) — otherwise NCM will start failing
verification for that device until the entry is refreshed.

## What the file actually looks like

See [`known_hosts.example`](known_hosts.example) in this directory for an
annotated sample showing the standard OpenSSH `known_hosts` formats you'll
see in practice: a plain entry keyed by IP, an entry keyed by hostname,
multiple aliases sharing one key, a **hashed** entry (the `ssh-keyscan -H`
output — recommended beyond a small lab, since it doesn't reveal your device
inventory if the file leaks), and an entry for a device on a non-default SSH
port. Every key blob in that example is random, fake data for illustrating
the format only — never copy the key material itself, only the shape of
the lines.

## The insecure_skip_verify tradeoff

Setting `insecure_skip_verify: true` makes NCM accept any host key the device
presents, skipping verification entirely. This removes the protection against
a man-in-the-middle or a different device silently answering at the same IP.

It's a reasonable **temporary** choice in an isolated lab or dev environment
while you build out `known_hosts` for real, but it should not ship to
production. If a Private Action Runner or jump host sits between the Agent
and the device, make sure `known_hosts` is populated on whichever host
actually opens the SSH connection.

## Install

1. Run `ssh-keyscan` (or your organization's equivalent host-key distribution process)
   to populate `known_hosts`, and verify the fingerprint out-of-band.
2. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml`.
3. Replace `<PLACEHOLDER>` values; keep `insecure_skip_verify: false` outside of a lab.
4. Restart the Agent (`sudo systemctl restart datadog-agent` or your platform's equivalent).
