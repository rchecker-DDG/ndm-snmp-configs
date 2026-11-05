# Rollback — restore a prior configuration to a device

Rollback lets a user pick an earlier configuration version in the NCM UI and
push it back to the device. It is the only NCM operation that **writes** to a
device, so it has its own prerequisites and should be enabled deliberately,
after regular collection already works.

See [`../ARCHITECTURE.md`](../ARCHITECTURE.md#3-rollback-on-demand-not-part-of-the-regular-collection-cycle)
for the flow: NCM UI → Private Action Runner (PAR) → Agent over IPC :5001 →
device over SSH :22.

## Prerequisites

| Requirement | Detail |
|---|---|
| Supported device | Cisco IOS and Arista EOS at the time of writing — check the [rollback docs](https://docs.datadoghq.com/network_monitoring/devices/config_management_rollback/) for the current list |
| Collection already working | The device shows configs on its **Configuration** tab |
| Agent version | **7.83.0 or later** |
| Device account | Write rights: enter config mode, apply and save — see [`../least-privilege-service-account/`](../least-privilege-service-account/) |
| Remote Configuration | Enabled for the Datadog org (the PAR depends on it) |
| Private Action Runner | Running, enrolled, and allowed to run the rollback action |
| Datadog permissions | **NCM Write** for the people who will roll back |

**If Remote Configuration or the PAR is disabled, collection keeps working.**
Backup, diff and AI summaries only need the NCM check; rollback is the only
feature that needs them.

## Files

| File | Goes in |
|---|---|
| [`datadog.yaml`](datadog.yaml) | Merge into the Agent's main `/etc/datadog-agent/datadog.yaml` |
| [`conf.yaml`](conf.yaml) | `/etc/datadog-agent/conf.d/network_config_management.d/conf.yaml` |

## Steps

1. Merge `datadog.yaml` (enables rollback and runs the PAR inside the Agent,
   Agent 7.81+). Prefer installing the PAR from **Fleet Automation → Enable
   Agent to take action** if you use Fleet Automation.
2. Optionally tune the local config store in `conf.yaml` — the Agent keeps
   these copies so it has something to roll back to.
3. Make sure the Agent can write to its `run_path` (normally
   `/opt/datadog-agent/run` on Linux).
4. Restart the Agent, then confirm the runner appears under **Private Action
   Runners** in Datadog (`/var/log/datadog/private-action-runner.log` if not).
5. Assign the runner to an execution group with a policy that allows
   `com.datadoghq.remoteaction.networkconfigmanagement.rollbackConfig`.
   How the runner was enrolled decides whether execution policies or
   Connections apply — see [Enrollment and
   ownership](https://docs.datadoghq.com/actions/private_actions/enroll_runner/).
6. Test on a lab device first. A rollback is itself a config change; log it
   in your change process.

## Troubleshooting

| Symptom | Check |
|---|---|
| No **Rollback** button | Unsupported vendor, Agent below 7.83.0, rollback not enabled, or user lacks NCM Write |
| Rollback fails immediately | PAR not running/enrolled, Remote Configuration off, action not allowlisted, or no permission to use the runner |
| Rollback fails after it starts | Device account lacks write rights, or the Agent can't reach the device on :22 |
