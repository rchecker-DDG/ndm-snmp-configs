# Vendor collection limitations — running vs. startup config

NCM retrieves configuration over SSH using vendor-specific commands, and
supports both **running** and **startup** configuration collection "where
supported" by the vendor/OS. In practice, not every supported vendor/OS
combination exposes both — and when a device only supports running-config
collection, the absence of a startup config in the UI is expected behavior,
not a failure.

As of this writing, Datadog's public documentation lists the supported
vendor/OS families as:

- Arista EOS
- Aruba AOS-CX / AOS-W
- Cisco IOS / NX-OS
- Dell DellOS10
- F5 TMOS
- FortiGate FortiOS
- Juniper JunOS
- Palo Alto PAN-OS

but does **not** publish a precise matrix of which specific vendor/OS/version
combinations support startup-config retrieval versus running-config only.
Rather than guess at that matrix here (it's the kind of detail that changes
as Datadog adds vendor profiles), the recommendation is:

## What to do if you only see a running config

1. Confirm the device vendor/OS is in the supported list above.
2. Check the [official NCM
   docs](https://docs.datadoghq.com/network_monitoring/devices/config_management/)
   for the current supported-devices table — this list is actively growing.
3. If your vendor/OS is listed as supported but you expected startup-config
   collection and don't see it, treat it as a question for Datadog support or
   your TAM rather than assuming it's a misconfiguration on your end — several
   support tickets on this topic turned out to be expected vendor behavior,
   not a setup error.

## Config for this scenario

There's nothing unique about the `conf.yaml` for this scenario — it's the
same structure as [`single-device-ssh-password/`](../single-device-ssh-password/)
or [`single-device-ssh-key/`](../single-device-ssh-key/). The point of this
page is the limitation itself, not a different config shape.
