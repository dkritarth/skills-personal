---
name: msu-dminer-fleet
version: 1.1.0
allowed-tools: [Read, Grep, Glob, Bash, AskUserQuestion]
description: Route and run research compute tasks across MSU Dminer, DECS, ICER HPCC, and NCSA Delta. Use for compute placement, SSH access, human password/Duo handoff, tmux, and Slurm experiments on these systems; not for unrelated server administration.
---

# MSU DMiner Fleet

Select and access the MSU research machine matching task requirements. The dminers provide dedicated GPU resources, DECS compute servers provide shared high-memory CPU capacity, and HPCC handles large batch workloads.

## When to use

Use for this fleet's access, workload placement, and experiment execution, including NCSA Delta. Unlike generic debugging or Git workflow skills, this skill carries the machine topology and authentication handoff required to reach the compute resources.

## When not to use

Do not apply this inventory to unrelated servers or infer permission to launch an experiment solely from loading this skill.

## Notify the user when their action is required

When blocked on a password, Duo approval, an expired SSH connection, or another required user action, invoke the environment's question/request-user-input tool. A final response or commentary alone does not notify this user. State exactly what they need to do, the machine and terminal where they must do it, and what reply will let work resume. Never ask for passwords or Duo codes in chat.

Use `request_user_input_async` in Codex when available, or the harness's equivalent question tool, such as `AskUserQuestion`. After issuing the question, keep the request pending and wait for the user's answer before retrying dependent access. Continue independent work if useful. Do not silently poll, treat elapsed time as completion, or finish the turn with only an authentication instruction. If no question tool is available, clearly report that limitation and the required action rather than pretending a notification was sent.

## Pre-flight checklist

1. Review [references/machines.md](references/machines.md) for verified hardware capacity and active constraints.
2. For DECS servers, review [references/decs-compute.md](references/decs-compute.md).
3. For HPCC cluster work, review [references/hpcc.md](references/hpcc.md).
   For NCSA Delta, review [references/delta.md](references/delta.md), including its human login and connection-sharing workflow.
4. Run `scripts/fleet-status.sh` for dminers or `scripts/decs-status.sh` for DECS servers. For HPCC, query `sinfo`, `squeue`, and `quota` from a development node. Use live load metrics to make final placement decisions.
5. Check for active user jobs and current load. Never kill, pause, renice, or displace running processes without explicit authorization.
6. Verify free disk space on the target filesystem. Keep at least 10% free space and avoid placing large artifacts on D-4 root storage.

## Machine routing

- **D-3**: Primary choice for GPU training and memory-intensive CPU jobs. Hardware: RTX 3090 (24 GiB VRAM), 128 GB RAM, ample root storage.
- **D-4**: Secondary choice for GPU jobs when D-3 is occupied and the task has modest persistent storage needs. Use `/mnt/bulk` for large durable datasets; do not fill `/`.
- **D-1 / D-2**: For lighter CUDA workloads, preprocessing, downloads, and CPU jobs fitting within 32 GB RAM. Both host GTX 1080 Ti GPUs (11 GiB VRAM, compute capability 6.1). Verify framework compatibility first. Prefer the host already holding required data.
- **DECS shared servers (`compute01` to `compute09`)**: Reserved for non-GPU long-running CPU batch jobs, large-memory computations, or CPU parallel tasks benefiting from large core counts. Do not use for routine interactive editing or small tests. Prefer `compute03` when memory requirements exceed 512 GB RAM. Otherwise select the least-loaded AMD host among `compute01`, `compute02`, and `compute04`. Nodes `compute05` through `compute09` currently reject SSH keys and should be treated as unavailable.
- **HPCC cluster**: Slurm-managed batch jobs needing extensive CPU scaling, more than 128 GB RAM, modern GPUs (V100, A100, L40S, H200, GH200), multi-node MPI, or jobs running beyond an interactive session. Default Slurm account is `general`.
- **NCSA Delta**: Allocation-backed Slurm CPU/GPU work. Check the user's actual Delta account, partition access, remaining allocation, and storage before submitting. Delta and DeltaAI are separate systems. Password and Duo authentication require a human; agents reuse an authenticated SSH connection on their execution host.

When multiple hosts are idle, pick the host that avoids transferring existing large datasets across the local network.

## Access patterns

From macOS:
- Connect to dminers: `ssh D-1`, `ssh D-2`, `ssh D-3`, or `ssh D-4` (proxies automatically via `scully.egr.msu.edu`).
- Connect to DECS: `ssh C-01` through `ssh C-04`.
- Connect to HPCC: `ssh hpcc-msu`, then connect to a dev node (such as `ssh dev-amd24`) to prepare and submit batch scripts with `sbatch`. Never run heavy compute on the login gateway.
- Prepare Delta access once with `python3 scripts/setup-delta-ssh.py` from this skill directory. The human runs `ssh -MNf delta` on the agent's execution host and completes password/Duo. The agent checks `ssh -O check delta` before `ssh -o BatchMode=yes delta 'hostname'`. See the Delta reference for tmux, expiry, and Slurm.

From any configured dminer:
- Connect to other dminers directly via aliases `D-1` through `D-4`.
- Connect to DECS servers directly via `compute01` through `compute04`.
- Delta connection sharing is local to each dminer and Unix account. A Mac login does not unlock Delta access from D-1 through D-4. Ask the human to authenticate on the specific origin using the question tool above.

Job execution rules:
- Run background tasks in `tmux` or `screen`.
- Output experiment logs and checkpoints to persistent disks, not temporary scratch paths.
- Announce the selected host and the reasoning before launching long jobs.

## Environment verification

Verify shell utilities on dminers using `fleet-doctor` and view command summaries with `fleet-help`. Use the fleet repository for shell configuration deployment.
