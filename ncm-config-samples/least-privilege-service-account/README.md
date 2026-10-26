# Scoping a least-privilege service account for NCM

Several real-world NCM setups run into friction because the network team
restricts device CLI access through command authorization (AAA/TACACS+,
RADIUS command sets, or vendor-native role-based CLI) and needs to know
exactly what NCM's automation account must be allowed to run before they'll
approve it.

## What NCM actually does on the device

NCM connects over SSH and issues **read-only, vendor-native commands** to
retrieve the running (and, where supported, startup) configuration — the
same category of command an engineer would run manually to view a config,
not to change one. It does not push configuration changes during normal
collection; configuration changes only happen if you explicitly use the
**rollback** feature, which restores a prior configuration via a Private
Action Runner — at which point the account effectively does need
write/commit access for rollback to work.

## Practical scoping guidance

Because Datadog does not publish an exact, vendor-by-vendor command list
(and that list can change as new vendor profiles are added), scope the
account in terms of **capability**, not a fixed command list:

- **Read-only tier (config backup/diff/AI-summary, no rollback)**: grant the
  account whatever your platform's native role calls "show-only" or
  "read-only" exec access — equivalent to being able to view running and
  startup configs, but not enter configuration mode or save/commit.
- **If you intend to use rollback**: the account additionally needs
  whatever privilege level lets it apply and save a configuration (e.g.
  enough to enter config mode and commit/write) — treat this as a
  deliberate, reviewed grant, not a default.
- **Validate before granting broadly**: test the scoped account against one
  device first and confirm NCM successfully retrieves a config before
  rolling the same role out fleet-wide — an under-scoped account fails
  silently from NCM's perspective (it just can't fetch anything), which is
  easy to mistake for an SSH connectivity or `known_hosts` problem.
- **Keep it a dedicated service account**, separate from any individual
  engineer's personal login — this makes it easy to audit what NCM does and
  to rotate credentials ([`secrets-management/`](../secrets-management/))
  without affecting a human user's access.

## Config for this scenario

The `conf.yaml` shape doesn't change based on the account's privilege level —
it's the same structure as
[`single-device-ssh-password/`](../single-device-ssh-password/) or
[`single-device-ssh-key/`](../single-device-ssh-key/). This page is about how
you provision the credentials NCM uses, not the YAML itself.
