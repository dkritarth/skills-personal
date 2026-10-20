# Verified machine inventory

Observed via SSH on 2026-08-21, with D-2 added on 2026-08-24. D-2 was live and reachable again on 2026-09-04. Storage availability is a point-in-time observation and must be refreshed before large writes.

| Alias | Address | CPU | Logical CPUs | RAM | GPU | Local storage and current constraint |
|---|---|---|---:|---:|---|---|
| D-1 / DM1 | 35.9.136.214 | Intel Core i7-6850K | 12 | 32 GB | NVIDIA GTX 1080 Ti, 11 GiB VRAM, compute capability 6.1 | 250 GB NVMe system disk, about 99 GB free; two 3 TB HDDs backing `/data`, about 666 GB free |
| D-2 / DM2 | 35.9.136.222 | Intel Core i7-6850K | 12 | 32 GB | NVIDIA GTX 1080 Ti, 11 GiB VRAM, compute capability 6.1 | 250 GB NVMe system disk, about 61 GB free; 3 TB RAID volume mounted at `/data`, about 1.2 TB free |
| D-3 / DM3 | 35.9.42.212 | Intel Core i9-12900KF | 24 | 128 GB | NVIDIA RTX 3090, 24 GiB VRAM, compute capability 8.6 | 2 TB NVMe system disk, about 545 GB free; unmounted 6 TB HDD observed |
| D-4 / DM4 | 35.9.136.224 | Intel Core i9-12900KF | 24 | 128 GB | NVIDIA RTX 3090, 24 GiB VRAM, compute capability 8.6 | 2 TB NVMe system disk, only about 79 GB free; 6 TB HDD mounted at `/mnt/bulk`, about 4.6 TB free |

D-1, D-3, and D-4 ran Ubuntu 20.04 at inspection; D-2 runs Ubuntu 24.04. D-1 uses NVIDIA driver 535.230.02, D-2 uses 580.173.02, D-3 uses 535.183.01, and D-4 uses 570.133.07. Driver and CUDA compatibility must be checked against the intended workload rather than inferred from the GPU alone. On 2026-09-04, D-2 responded as `dminer-dl-2` with load 0.45/0.72/0.54, 24 GiB available RAM, and 1.2 TB free in `/data`; its GTX 1080 Ti had 322 MiB allocated, including the desktop remote-access daemon.

## SSH topology

- Mac to every dminer: `ProxyJump scully-msu` with your MSU username.
- Dminer to dminer: direct MSU addresses with a per-host `~/.ssh/id_ed25519_dminer_fleet` key.
- Each host authorizes the distinct fleet public keys needed for verified bidirectional access among D-1 through D-4.

## Operational cautions

- D-4's root filesystem was 96% used at inspection time. Prefer `/mnt/bulk` for large files where NTFS semantics and performance are acceptable.
- D-3's 6 TB HDD appeared as a block device but was not mounted. Do not format or mount it without explicit user approval and ownership verification.
- D-1 has much less RAM and GPU memory than D-3/D-4 and an older GPU architecture.
