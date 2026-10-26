# NCM architecture — components and collection flow

Two diagrams: **where each component lives**, and **the step-by-step flow**
from the Agent reaching out to a device to the configuration landing in the
Datadog backend. Both are [Mermaid](https://mermaid.js.org/) diagrams, which
GitHub renders natively in markdown — no separate image file to keep in sync.

The sequence-diagram steps below are a reconstruction from the [public NCM
docs](https://docs.datadoghq.com/network_monitoring/devices/config_management/)
and general Datadog Agent architecture, not Datadog's internal implementation
spec — steps 1-9 (device-facing) are precise, since they're directly
determined by `conf.yaml` and standard SSH behavior; steps 10-13
(backend-internal: storage, diffing, AI summary) are necessarily described at
a higher level, since the backend's internals aren't publicly documented in
full.

## 1. Components and where they live

```mermaid
flowchart LR
    subgraph customer_env["Customer environment"]
        direction TB
        device["Network device<br/>(Cisco IOS / JunOS / EOS / etc.)<br/>SSH daemon on :22"]
        agent["Datadog Agent host<br/>- conf.d/snmp.d/conf.yaml (NDM)<br/>- conf.d/network_config_management.d/conf.yaml (NCM)<br/>- known_hosts file<br/>- credentials (plaintext or ENC[] secret refs)"]
        par["Private Action Runner<br/>(optional — rollback only)"]
    end

    subgraph datadog_cloud["Datadog backend (SaaS)"]
        direction TB
        intake["Agent intake<br/>(HTTPS)"]
        ndm_svc["NDM service<br/>device inventory, namespace,<br/>device identity"]
        ncm_svc["NCM service<br/>config version storage,<br/>diff engine, AI summary"]
        ui["NCM UI<br/>device page → Configuration tab"]
    end

    agent -- "SSH :22<br/>(auth + known_hosts)" --> device
    device -- "config text<br/>(running/startup)" --> agent
    agent -- "HTTPS payload<br/>(config + device metadata)" --> intake
    intake --> ncm_svc
    ncm_svc <-- "device identity,<br/>namespace" --> ndm_svc
    ncm_svc --> ui
    ui -- "rollback request" --> par
    par -- "SSH :22<br/>(apply prior config)" --> device
```

## 2. Step-by-step collection flow

```mermaid
sequenceDiagram
    participant Sched as Agent scheduler<br/>(min_collection_interval)
    participant Agent as Datadog Agent<br/>(network_config_management check)
    participant Device as Network device
    participant Intake as Datadog Agent intake
    participant NCM as NCM backend service
    participant UI as NCM UI

    Sched->>Agent: 1. Trigger collection cycle<br/>(default every 900s / 15 min)
    Agent->>Agent: 2. Read conf.yaml — resolve instances,<br/>namespace, auth, ssh block
    Agent->>Device: 3. Open TCP connection to ip_address:22
    Device-->>Agent: 4. Present SSH host key
    Agent->>Agent: 5. Verify host key against known_hosts_path<br/>(or skip if insecure_skip_verify: true)
    Agent->>Device: 6. Authenticate (username + password,<br/>or username + private_key_file)
    Device-->>Agent: 7. Auth accepted
    Agent->>Device: 8. Issue vendor-specific read commands<br/>(e.g. show running-config / show startup-config<br/>equivalents, selected by detected vendor/OS)
    Device-->>Agent: 9. Return raw config text
    Agent->>Agent: 10. Close SSH session
    Agent->>Intake: 11. Send config text + device metadata<br/>(device id, namespace, timestamp) over HTTPS
    Intake->>NCM: 12. Route payload to NCM service
    NCM->>NCM: 13. Store new config version,<br/>diff against last stored version for this device
    NCM->>NCM: 14. Generate AI natural-language<br/>summary of the diff
    NCM->>UI: 15. Surface new version, diff,<br/>and summary on device's Configuration tab
```

## 3. Rollback (on-demand, not part of the regular collection cycle)

Rollback is a separate, user-initiated flow, not something that happens on
the `min_collection_interval` schedule:

1. A user selects a prior configuration version in the NCM UI and requests rollback.
2. The backend routes the request through a **Private Action Runner (PAR)** —
   a customer-hosted component Datadog uses for actions that need to reach
   back into the customer's network to make a change, as opposed to the
   read-only collection flow above.
3. The PAR connects to the device over SSH and applies the selected prior
   configuration.

Because rollback writes to the device, the account used for it needs
write/commit-capable privileges — see
[`least-privilege-service-account/`](least-privilege-service-account/) for
how to scope that deliberately rather than by default.

## Why collection is read-only but rollback isn't

It's worth internalizing the asymmetry these diagrams show: every step in
the regular collection cycle (steps 3-10 above) is read-only — `show`-equivalent
commands, no device state changes. Rollback is the only operation in the
whole NCM feature set that writes to a device, and it only happens on
request, through a different path (the PAR), not through the Agent's regular
polling cycle. This is why a read-only service account is sufficient for
backup/diff/AI-summary, and why rollback access should be a deliberate,
separately-reviewed grant.
