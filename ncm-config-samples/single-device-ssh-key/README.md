# Single device — SSH private-key authentication

Same as [`single-device-ssh-password/`](../single-device-ssh-password/), but
authenticating with an SSH private key instead of a password — the preferred
option where your network/security team's AAA policy allows key-based access
for automation accounts.

## Key fields in this config

- `instances[].auth.private_key_file` — path (on the host running the Agent) to the private key.
- `instances[].auth.username` — still required alongside the key.
- `instances[].auth.password` — leave unset when using a key. The docs don't specify a precedence
  order if both `password` and `private_key_file` are present, so setting both only creates
  ambiguity about which credential was actually used — pick one.

## A note on key management

The private key file must be readable by the Agent's user (typically `dd-agent`) and
should be scoped to this automation account only — don't reuse an individual
engineer's personal SSH key. See
[`least-privilege-service-account/`](../least-privilege-service-account/) for
guidance on scoping the account itself, and
[`secrets-management/`](../secrets-management/) for keeping the key path and
any related secrets out of plaintext `conf.yaml`.

## Install

1. Place the private key on the Agent host with restrictive permissions (e.g. `chmod 600`)
   and an owner the Agent process can read.
2. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml`.
3. Replace every `<PLACEHOLDER>`.
4. Restart the Agent (`sudo systemctl restart datadog-agent` or your platform's equivalent).
