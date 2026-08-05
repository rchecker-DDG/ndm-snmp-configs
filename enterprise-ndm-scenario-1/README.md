# Enterprise Network Device Monitoring — Scenario 1

**Multi-site enterprise SD-WAN with dual-ISP redundancy, overlapping branch IPs, and full NDM feature coverage.**

---

## Scenario Overview

This scenario models a realistic enterprise network spanning five sites (2 datacenters + 3 branches) connected over Cisco Catalyst SD-WAN (Viptela) with dual-ISP WAN redundancy. Every Datadog NDM capability is exercised: SNMP v3 autodiscovery, interface tagging, topology collection, VPN metrics, SNMP traps, NetFlow/IPFIX/sFlow, syslog, remote config, and Agent HA.

```
                        ┌─────────────────────────────┐
                        │    AWS Cloud (us-east-1)    │
                        │  VPC 172.16.0.0/16 · TGW   │
                        └──────────┬──────────────────┘
                                   │ Cloud OnRamp
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
   ┌────┴───┐        ┌─────────────────────────┐        ┌────┴───┐
   │  DC1   │───WAN1─┤  Service Provider WAN   ├─WAN1───│  DC2   │
   │Primary │───WAN2─┤  ISP-1: AT&T (primary)  ├─WAN2───│   DR   │
   └────────┘        │  ISP-2: Comcast (backup)│        └────────┘
                     │  Cisco SD-WAN: vManage  │
                     │   vSmart · vBond (SaaS) │
                     └────┬──────────┬────┬────┘
                          │          │    │
                     ┌────┴──┐  ┌───┴─┐  └────┐
                     │BranchA│  │Br B │       │Br C│
                     │192.168│  │192.168      │10.3│
                     │.10/24 │  │.10/24       │/24 │
                     └───────┘  └─────┘       └────┘
                      ⚠ overlapping IPs — namespace isolation
```

---

## Sites

| Site | Role | Subnet | Namespace | Agent Host | WAN1 (ISP-1/AT&T) | WAN2 (ISP-2/Comcast) |
|------|------|--------|-----------|-----------|-------------------|----------------------|
| DC1 | Primary DC | 10.0.0.0/24 · 10.0.2.0/24 (ACI) | `dc1` | dd-agent-dc1-01/02 | 203.0.113.1/30 | 209.51.188.1/30 |
| DC2 | DR Datacenter | 10.1.0.0/24 | `dc2` | dd-agent-dc2-01/02 | 203.0.113.5/30 | 209.51.188.5/30 |
| Branch-A | Branch (NYC) | 192.168.10.0/24 ⚠ | `branch-a` | dd-agent-bra-01 | 100.64.1.1/30 | 100.64.11.1/30 |
| Branch-B | Branch (BOS) | 192.168.10.0/24 ⚠ | `branch-b` | dd-agent-brb-01 | 100.64.2.1/30 | 100.64.12.1/30 |
| Branch-C | Branch (LAX) | 10.3.0.0/24 | `branch-c` | dd-agent-brc-01 | 100.64.3.1/30 | 100.64.13.1/30 |

> ⚠ Branch-A and Branch-B share the same RFC1918 subnet `192.168.10.0/24`. The `namespace` field in each agent's `datadog.yaml` is what makes them unique in Datadog (device IDs become `branch-a:192.168.10.1` vs `branch-b:192.168.10.1`).

---

## Devices per Site

### DC1 — Primary Datacenter

| Device | IP | Role | Telemetry |
|--------|-----|------|-----------|
| cEdge-DC1 (Cisco CSR1000v) | 10.0.0.1 | SD-WAN cEdge router | SNMP v3 · NetFlow v9 · collect_vpn |
| PA-5220 (Palo Alto) | 10.0.0.2 | Next-gen firewall | SNMP v3 · IPFIX → 4739 · traps |
| F5 BIG-IP-01 (Active) | 10.0.0.10 | Load balancer | SNMP v3 · sFlow → 6343 · traps |
| F5 BIG-IP-02 (Standby) | 10.0.0.11 | Load balancer HA | SNMP v3 · sFlow → 6343 |
| C9500-Core (Cisco Catalyst) | 10.0.0.20 | Core/distribution switch | SNMP v3 · NetFlow v9 → 2055 |
| ACI APIC | 10.0.0.30 | ACI controller | SNMP v3 |
| ACI Spine-1, Spine-2 | 10.0.2.1, .2 | ACI fabric spine | SNMP v3 · NetFlow v9 → 2056 |
| ACI Leaf-101, Leaf-102 | 10.0.2.101, .102 | ACI fabric leaf | SNMP v3 |
| Meraki MR57 | 10.0.0.40 | Enterprise WiFi AP | Dashboard API |
| Meraki MS390 | 10.0.0.41 | PoE switch | Dashboard API |

### DC2 — DR Datacenter

| Device | IP | Role | Telemetry |
|--------|-----|------|-----------|
| cEdge-DC2 (Cisco CSR1000v) | 10.1.0.1 | SD-WAN cEdge router | SNMP v3 · collect_vpn |
| PA-3220 (Palo Alto) | 10.1.0.2 | Next-gen firewall | SNMP v3 · IPFIX → 4739 |
| F5 BIG-IP-DR | 10.1.0.10 | Load balancer DR | SNMP v3 · sFlow → 6343 |
| C9500-DR | 10.1.0.20 | Core switch DR | SNMP v3 · NetFlow v9 → 2055 |
| C9300-DC2 | 10.1.0.21 | Access switch | SNMP v3 |
| Meraki MR46 | 10.1.0.40 | Enterprise WiFi AP | Dashboard API |
| Meraki MS250 | 10.1.0.41 | Switch | Dashboard API |

### Branches A / B / C (same device types, different IPs)

| Device | Role | Telemetry |
|--------|------|-----------|
| cEdge-BRx (Cisco ISR4331) | SD-WAN branch router | SNMP v3 · NetFlow v9 → 2055 · collect_vpn |
| C9300-BRx (Cisco Catalyst) | Access switch | SNMP v3 · NetFlow v9 → 2055 |
| EX2300-BRx (Juniper Mist) | Mist-managed switch | SNMP v3 · Mist API |
| AP43-BRx (Juniper Mist) | WiFi access point | SNMP v3 · traps v3 → 9162 |

---

## NDM Features Exercised

| Feature | Config location | Sites |
|---------|----------------|-------|
| SNMP v3 autodiscovery (subnet sweep) | `datadog.yaml` → `network_devices.autodiscovery` | All 5 |
| Namespace isolation (overlapping IPs) | `namespace: branch-a` vs `namespace: branch-b` | BrA + BrB |
| Topology collection (LLDP/CDP) | `collect_topology: true` | All 5 |
| SD-WAN VPN metrics | `collect_vpn: true` | All 5 (cEdge) |
| Interface tagging (role/provider/geo) | `interface_configs` in autodiscovery + snmp.d | All 5 |
| Speed overrides | `speed_override:` per interface | All 5 |
| Ping/ICMP alongside SNMP | `ping.enabled: true` | All 5 |
| SNMP Trap receiver | `network_devices.snmp_traps` port 9162 | All 5 |
| v3 traps multi-vendor | `users:` Cisco + PA + F5 + Juniper | DC1, DC2, branches |
| NetFlow v9 | `flow_type: netflow9` port 2055/2056 | All 5 |
| IPFIX | `flow_type: ipfix` port 4739 | DC1, DC2 |
| sFlow | `flow_type: sflow` port 6343 | DC1, DC2 |
| Reverse DNS enrichment | `reverse_dns_enrichment_enabled: true` | All 5 |
| Agent HA (deduplication) | `use_deduplication: true` | DC1, DC2 |
| Remote Configuration | `remote_configuration.enabled: true` | All 5 |
| Syslog collection | `conf.d/syslog.d/conf.yaml` ports 5014 UDP+TCP | DC1, DC2 |
| Meraki Dashboard API | `conf.d/cisco_meraki.d/conf.yaml` | DC1, DC2 |
| Juniper Mist (SNMP + API) | `conf.d/snmp.d/conf.yaml` + Mist dashboard | Branches |
| Custom device tags | `use_device_id_as_hostname: true` + `tags:` | All 5 |
| Vendor/geo/role tags | per-device in `snmp.d/conf.yaml` | All 5 |

---

## Repository Structure

```
enterprise-ndm-scenario-1/
├── README.md                            ← this file
├── topology/
│   ├── enterprise-ndm-topology.svg      ← network diagram (SVG, render in browser)
│   └── enterprise-ndm-topology.excalidraw  ← editable diagram (open at excalidraw.com)
├── dc1/
│   ├── datadog.yaml                     ← main agent config: SNMP, traps, NetFlow, syslog, HA
│   └── conf.d/
│       ├── snmp.d/conf.yaml             ← 10 device instances with interface tags
│       ├── cisco_meraki.d/conf.yaml     ← Meraki MR57 + MS390 Dashboard API
│       └── syslog.d/conf.yaml           ← UDP + TCP syslog listener
├── dc2/
│   ├── datadog.yaml
│   └── conf.d/
│       ├── snmp.d/conf.yaml             ← 5 device instances
│       ├── cisco_meraki.d/conf.yaml     ← Meraki MR46 + MS250
│       └── syslog.d/conf.yaml
├── branch-a/
│   ├── datadog.yaml                     ← namespace: branch-a (192.168.10.0/24)
│   └── conf.d/snmp.d/conf.yaml
├── branch-b/
│   ├── datadog.yaml                     ← namespace: branch-b (192.168.10.0/24 — same subnet!)
│   └── conf.d/snmp.d/conf.yaml
└── branch-c/
    ├── datadog.yaml                     ← namespace: branch-c (10.3.0.0/24)
    └── conf.d/snmp.d/conf.yaml
```

---

## Quick Start

### 1. Set environment variables on each agent host

```bash
# Required — from your Datadog org settings
export DD_API_KEY="<your-datadog-api-key>"

# SNMP v3 credentials (all sites use same user; rotate keys per site in production)
export DD_SNMP_AUTH_KEY="<snmpv3-auth-passphrase-min-8-chars>"
export DD_SNMP_PRIV_KEY="<snmpv3-priv-passphrase-min-8-chars>"

# Trap v3 credentials per vendor
export DD_TRAP_CISCO_AUTH_KEY="<cisco-trap-auth>"
export DD_TRAP_CISCO_PRIV_KEY="<cisco-trap-priv>"
export DD_TRAP_PA_AUTH_KEY="<pa-trap-auth>"
export DD_TRAP_PA_PRIV_KEY="<pa-trap-priv>"
export DD_TRAP_F5_AUTH_KEY="<f5-trap-auth>"
export DD_TRAP_F5_PRIV_KEY="<f5-trap-priv>"
export DD_TRAP_JUNIPER_AUTH_KEY="<juniper-trap-auth>"
export DD_TRAP_JUNIPER_PRIV_KEY="<juniper-trap-priv>"

# Meraki (DC1 + DC2 only)
export DD_MERAKI_API_KEY="<meraki-dashboard-api-key>"
```

### 2. Deploy agent config files

```bash
# Example: DC1 agent
scp -r dc1/datadog.yaml root@10.0.0.50:/etc/datadog-agent/datadog.yaml
scp -r dc1/conf.d/      root@10.0.0.50:/etc/datadog-agent/conf.d/
systemctl restart datadog-agent

# Add iptables rules for SNMP traps + syslog
iptables -t nat -A PREROUTING -p udp --dport 162 -j REDIRECT --to-port 9162
iptables -t nat -A PREROUTING -p udp --dport 514 -j REDIRECT --to-port 5014
iptables -t nat -A PREROUTING -p tcp --dport 514 -j REDIRECT --to-port 5014
```

### 3. Configure SNMP v3 on network devices

```
# Cisco IOS-XE (cEdge, C9300, C9500)
snmp-server group DD_GROUP v3 priv
snmp-server user dd_snmpv3 DD_GROUP v3 auth sha256 <auth-key> priv aes 256 <priv-key>
snmp-server host <agent-ip> traps version 3 priv cisco_trap_v3

# Palo Alto
Device > Setup > Operations > SNMP Setup → v3 credentials
Device > Log Forwarding → IPFIX to agent-ip:4739

# F5 BIG-IP
tmsh modify sys snmp communities delete all
tmsh modify sys snmp v3-users add { dd_snmpv3 { ... } }
```

### 4. HA at DC sites (optional)

Run a second agent (`dd-agent-dc1-02`) with the **identical** `datadog.yaml`. The `use_deduplication: true` setting ensures both agents don't double-poll the same device. Requires Agent ≥ 7.67.

---

## Agent Version Requirements

| Feature | Min Agent Version |
|---------|-----------------|
| `network_devices.autodiscovery` (new-style) | 7.54 |
| `network_devices.snmp_traps` | 7.37 |
| `network_devices.netflow` | 7.45 |
| `use_deduplication` (HA) | 7.67 |
| `remote_configuration.enabled` | 7.41 |
| `collect_topology` | 7.46 |
| `collect_vpn` | 7.52 |

---

## Topology Diagram

Open `topology/enterprise-ndm-topology.excalidraw` at [excalidraw.com](https://excalidraw.com) to view and edit the full network diagram.

The SVG version (`topology/enterprise-ndm-topology.svg`) can be rendered directly in any browser.

---

*Generated 2026-08-05 · Datadog NDM Enterprise Scenario 1*
