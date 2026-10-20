# MSU ICER HPCC

Operational reference checked against the official MSU ICER documentation and live account access on 2026-09-04. Public hardware and partition availability can change; live Slurm output controls placement.

## Access and agent boundary

- Mac entry point: `ssh hpcc-msu`, configured locally as `$USERNAME@hpcc.msu.edu`.
- The HPCC gateway is `gateway-02.dmz` for the verified session. It is an entry point only; do not compile, train, or run long processes there.
- From the gateway, use a development node such as `ssh dev-amd24`, `ssh dev-amd24-h200`, `ssh dev-amd20`, `ssh dev-amd20-v100`, or `ssh dev-intel18`.
- Submit scheduled experiments from a development node with `sbatch`. Use `salloc`/`srun` only for bounded interactive development or smoke tests.
- The HPCC key is configured on the Mac. Do not copy the private key to dminers. If an agent is running on a dminer, verify that host's HPCC public-key login separately before using it as the submission origin.

## Account and live access

The verified `sacctmgr` associations for user `$USERNAME` were:

```text
cluster=msuhpcc account=general default-qos=$USERNAME
cluster=msuhpcc account=scavenger default-qos=scavenger
```

Use `general` by default. Use `scavenger` only when the user requests it or a live account/queue check shows it is appropriate. A successful login does not imply that every partition, buy-in resource, or GPU is available to the account at the moment of submission.

Useful live checks:

```bash
sinfo -o "%P|%a|%l|%c|%m|%G|%D|%N"
squeue -u "$USER"
sacctmgr -nP show assoc where user="$USER" format=Cluster,Account,Partition,QOS,DefaultQOS
quota
```

## Documented compute resources

The current MSU resource table lists these node families:

| Cluster | Nodes and resources | GPU resources |
|---|---|---|
| `amd24` | AMD EPYC 9654/9684X, 192 cores; 768 GB, 1.5 TB, or 2.3 TB RAM | H200 nodes (`nfh`, `neh`) and L40S nodes (`nel`) |
| `amd22` | AMD EPYC 7763, 128 or 256 cores; about 493 GB, 996 GB, or 2.0 TB RAM | none listed |
| `amd21` | AMD EPYC 7713, 128 or 256 cores; 512 GB RAM | A100 SXM (`nal`) |
| `intel21` | Intel Xeon 8358, 64 or 256 cores; 256 GB RAM | A100 PCIe (`nif`) |
| `amd20` | AMD EPYC 7H12, 128 cores; about 493 GB, 996 GB, or 2.0 TB RAM | none listed |
| `amd20-v100` | Intel Xeon 8260, 48 cores; about 178 or 565 GB RAM | 4x V100S per node (`nvf`) |
| `intel18` | Intel Xeon Gold 6148, 40 cores; about 83 GB to 996 GB RAM | none listed |
| `intel18-v100` | Intel Xeon Gold 6148, 40 cores; 367 GB RAM | 8x V100 per node (`nvl`) |
| `intel16` | Intel E7-8867, 64/144 cores; about 2.9/5.9 TB RAM | none listed |

The live 2026-09-04 `sinfo` output additionally showed GH200 nodes (`nch`) and an A100 MIG resource (`a100_1g.10gb`) in `scavenger`. Treat those as live observations, not stable inventory promises.

## Slurm workflow

Partition selection is normally automatic. MSU documents these relevant queues:

- `general-short`: jobs with requested wall time up to 4 hours.
- `general-long`: non-GPU jobs up to 7 days.
- `general-long-bigmem`: jobs requesting more than 740 GB per node, up to 7 days.
- `general-long-gpu`: jobs requesting GPUs, up to 7 days.
- `scavenger`: a live partition visible to this account; inspect its current policy and availability before using it.

Request resources, not a specific node, unless a constraint is necessary. Examples:

```bash
# CPU smoke test
sbatch --account=general --time=00:10:00 --cpus-per-task=4 --mem=16G \
  --wrap='hostname; python -c "print(\"HPCC_OK\")"'

# One H200-class GPU job; the exact GPU type must match the current table
sbatch --account=general --time=02:00:00 --ntasks=1 --cpus-per-task=8 \
  --mem=64G --gpus=h200:1 run_experiment.sh

# Interactive smoke test, not a long experiment
salloc --account=general --time=00:15:00 --cpus-per-task=2 --mem=8G
srun --pty bash
```

For GPU jobs, request the GPU type explicitly when portability matters, and request only the CPUs and memory the program can use. Slurm grants the GPU's VRAM with the GPU allocation; CPU RAM must be requested separately. Use `--gpus-per-node` or `--gpus-per-task` for multi-process jobs, and add `--gres-flags=enforce-binding` only when CPU/GPU locality matters enough to justify potentially longer queue time.

Agents should record the submitted job ID, requested resources, code/data revision, and output paths. Poll with `squeue -j JOBID`, inspect completed jobs with `sacct -j JOBID`, and preserve stdout/stderr in a durable location.

## Storage policy

- `$HOME` / `/mnt/home/$USER`: private, snapshot-protected home space; this account currently has a 100 GB quota and used about 32 KB at verification.
- Research space: `/mnt/research/GROUP` when a research allocation is provisioned; use it for shared durable group data.
- `$SCRATCH` / `/mnt/scratch/$USER`: high-I/O temporary space, nominally up to 50 TB and 1,000,000 files; not backed up and files unchanged for 45 days may be deleted. The verified non-interactive gateway shell may not export `$SCRATCH`, so agents should resolve and check the path on the target development node.
- `/mnt/local`, `/tmp`, and `/dev/shm`: node-local temporary space; not backed up and subject to purge/cleanup. Use only for staged job-local data and copy results back.

Safe pattern: keep authoritative inputs/checkpoints in Home or Research, copy working data to Scratch or node-local storage, run the Slurm job, then copy verified outputs and checkpoints back before treating the job as complete.

## Official references

- [Cluster resources](https://docs.icer.msu.edu/Cluster_Resources/)
- [Development nodes](https://docs.icer.msu.edu/development_nodes/)
- [SLURM queueing and partitions](https://docs.icer.msu.edu/SLURM_Queueing_and_Partitions/)
- [Requesting GPUs](https://docs.icer.msu.edu/Requesting_GPUs/)
- [Home space](https://docs.icer.msu.edu/Home_Space/)
- [Scratch space](https://docs.icer.msu.edu/Scratch_File_Systems/)
- [File storage and I/O guidance](https://docs.icer.msu.edu/Guidelines_for_Choosing_File_Storage_and_I_O/)
