# Single device — SNMP v3 (authPriv)

Monitor one device using SNMP v3 with both authentication and privacy enabled
(the `authPriv` security level). Instead of a community string, v3 uses a USM
`user` plus an `authProtocol`/`authKey` pair to prove identity and a
`privProtocol`/`privKey` pair to encrypt the payload on the wire. Use this when
your security posture forbids the clear-text community strings of v1/v2c. Pick the
strongest auth/priv protocols both ends support (here SHA256 + AES256).

## Key fields in this config

- `snmp_version: 3` — selects v3; the credential block replaces `community_string`.
- `user` — the USM security name (required for v3).
- `authProtocol` / `authKey` — authentication algorithm and passphrase
  (MD5, SHA, SHA224, SHA256, SHA384, SHA512).
- `privProtocol` / `privKey` — encryption algorithm and passphrase
  (DES, AES, AES192, AES192C, AES256, AES256C; `3DES` is python-only).
- `context_name` / `context_engine_id` — optional v3 context; the engine id is
  usually auto-discovered.

## Loader

Uses `loader: core`. All chosen protocols are valid on core. Note that the `3DES`
privacy protocol is **python-only** — if you must use it, switch to
`loader: python` and flag it in a comment. This config avoids it.

## Install

1. Copy `conf.yaml` to `/etc/datadog-agent/conf.d/snmp.d/conf.yaml`.
2. Replace every `<PLACEHOLDER>`; remove the optional context lines if unused.
3. Restart the Agent.
