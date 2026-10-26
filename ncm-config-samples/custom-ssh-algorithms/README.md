# Custom SSH algorithms for legacy/hardened devices

Some devices fail the SSH handshake against the Agent's default cipher/key-
exchange/host-key-algorithm set — common on older platforms and on gear
hardened to a specific suite by security policy. The symptom is usually an
error like "no supported methods remain" or "no common algorithm," which
looks like a connectivity or credentials problem but is actually a transport-
layer negotiation mismatch.

## How to diagnose this correctly

Before reaching for this sample, confirm it's actually an algorithm mismatch
and not something else:

- Basic reachability: can you `ssh` to the device manually from the Agent host, with the
  same credentials? If that also fails, fix connectivity/credentials first.
- If manual `ssh` works but NCM fails, check the device's SSH server
  configuration (or its logs during a failed NCM connection attempt) for which
  ciphers, key exchange algorithms, and host key algorithms it actually
  offers, rather than guessing.

## Key fields in this config

- `init_config.ssh.ciphers` / `key_exchanges` / `host_key_algorithms` — override the
  Agent's default SSH algorithm set. Valid values are documented at the
  [Go crypto/ssh constants reference](https://pkg.go.dev/golang.org/x/crypto/ssh#pkg-constants).
- These settings are **global** to the `conf.yaml` file — there's no documented
  per-instance override. If only some devices in your fleet need non-default
  algorithms, put them in a separate conf.yaml / instance file so the override
  doesn't change behavior for devices that work fine with the defaults.

## Install

1. Identify the exact algorithms your device supports (device SSH config/logs, or vendor docs).
2. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml`.
3. Replace the placeholder algorithm lists with values that match your actual device.
4. Replace `<PLACEHOLDER>` credentials.
5. Restart the Agent (`sudo systemctl restart datadog-agent` or your platform's equivalent).
