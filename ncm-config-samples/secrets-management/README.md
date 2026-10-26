# Keeping SSH credentials out of plaintext conf.yaml

Every other sample in this directory uses a filled-in example password or
private key path directly in `conf.yaml`, for clarity. In production, don't
leave real credentials in plaintext inside `conf.yaml` — use the [Datadog Agent's
secrets management
feature](https://docs.datadoghq.com/agent/configuration/secrets-management/)
instead, which resolves `ENC[<handle>]` references at Agent startup through a
`secret_backend_command` you configure (commonly backed by Vault, AWS Secrets
Manager, or another secret store).

## Important: this is a general Agent capability, not an NCM-specific one

The `ENC[]` syntax and secret backend mechanism apply Agent-wide, across any
integration's `conf.yaml` — this page isn't describing an NCM-only feature.
If you haven't already set up a secret backend for another integration,
start with the [secrets management
docs](https://docs.datadoghq.com/agent/configuration/secrets-management/) and
validate it resolves correctly before assuming it will "just work" for
`network_config_management.d/conf.yaml` too.

## Key fields in this config

- `instances[].auth.username` / `auth.password` — set to `ENC[<handle>]` instead of a literal
  value; the handle name is your choice and must match what your `secret_backend_command`
  script knows how to resolve.
- Everything else is identical to
  [`single-device-ssh-password/`](../single-device-ssh-password/).

## Install

1. Confirm a `secret_backend_command` is already configured and working in `datadog.yaml`
   (test with a simpler integration first if this is your first time setting it up).
2. Store the NCM service account's username/password (or key path) in your secret backend.
3. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml`,
   using `ENC[]` handles that match what you stored.
4. Restart the Agent and confirm the secrets resolve (check Agent logs for secret resolution
   errors before assuming the credentials themselves are wrong).
