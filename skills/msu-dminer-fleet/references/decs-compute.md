# MSU DECS shared compute servers

Source: [MSU DECS Compute Servers](https://www.egr.msu.edu/decs/labs/compute-servers), checked 2026-08-21. Page specifications are administrative documentation; live facts below are labeled separately.

These are shared, CPU-focused servers available to users with valid Engineering accounts. Use them for long-running unspecialized CPU workloads, high-memory workloads, and appropriately parallel CPU computation, not routine interactive work or GPU training.

| Aliases | MSU-listed processors | Virtual cores | MSU-listed RAM | OS | Access status on 2026-08-21 |
|---|---|---:|---:|---|---|
| C-01 / CS1 / compute01 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 512 GB | AlmaLinux 9 | Verified from Mac and reachable dminers |
| C-02 / CS2 / compute02 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 512 GB | AlmaLinux 9 | Verified from Mac and reachable dminers |
| C-03 / CS3 / compute03 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 1,024 GB | AlmaLinux 9 | Verified from Mac and reachable dminers |
| C-04 / CS4 / compute04 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 512 GB | AlmaLinux 9 | Verified from Mac and reachable dminers |
| C-05 / CS5 / compute05 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 512 GB | AlmaLinux 9 | Online but rejects verified SSH keys |
| C-06 / CS6 / compute06 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 512 GB | AlmaLinux 9 | Online but rejects verified SSH keys |
| C-07 / CS7 / compute07 | 2x AMD EPYC 7H12, 2.6 GHz | 256 | 512 GB | AlmaLinux 8 | Online but rejects verified SSH keys |
| C-08 / CS8 / compute08 | 2x Intel Xeon Platinum 8180, 2.5 GHz | 112 | 768 GB | AlmaLinux 9 | Online but rejects verified SSH keys |
| C-09 / CS9 / compute09 | 2x Intel Xeon Platinum 8180, 2.5 GHz | 112 | 768 GB | AlmaLinux 9 | Online but rejects verified SSH keys |

Live inspection confirmed 256 logical CPUs on compute01 through compute04, approximately 502 GiB usable RAM on compute01, compute02, and compute04, approximately 1.0 TiB on compute03, and AlmaLinux 9.8 on those four hosts.

## Shared-server placement rules

- Check live load, available memory, and running processes immediately before placement. The MSU page recommends `computeuse`, but that command was not present in the default PATH on compute01 during verification; use the status script's portable checks when unavailable.
- Do not default to compute03. Reserve its 1 TiB memory capacity for workloads that actually need more than 512 GB or when it is clearly the least-loaded suitable host.
- Scale CPU parallelism to the application and current shared load. Avoid monopolizing a host.
- Do not assume useful NVIDIA GPUs; MSU documents CPU and RAM capacity, and GPU capability has not been verified.

## Storage and lifecycle

- `/egr/scratch` is shared across central login and compute servers.
- `/localscratch` is local to one compute server and is preferable for high-I/O temporary data when the job stays on that host.
- Files or directories older than 14 days are automatically removed from both scratch locations.
- Neither scratch location is backed up. Store durable inputs, checkpoints, results, and archives in `/home` or `/egr/research` as appropriate.
- Servers with uptime over 30 days may be rebooted for maintenance, and emergency reboots may occur at any time. Long jobs must checkpoint.

Live inspection on compute01 through compute04 showed about 1.9 TiB free in `/egr/scratch` and roughly 2.8 to 2.9 TiB free in each host's `/localscratch`; refresh before use.

## Access topology

- Mac: SSH through `scully.egr.msu.edu` automatically via configured aliases.
- Reachable dminers: direct MSU-network SSH using each dminer's distinct fleet key.
- compute01 through compute04 share `/home/$USERNAME` over NFS and authorize the Mac key plus the distinct fleet keys used by all four dminers.
- D-2 access to compute01 through compute04 was verified on 2026-08-24.
- compute05 through compute09 respond on SSH but do not accept the same keys. They are not routing options until DECS resolves or explains the host-side authentication difference.
