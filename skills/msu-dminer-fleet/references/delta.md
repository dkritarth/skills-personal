# NCSA Delta: human login, agent execution

NCSA login name: `kdandapat`. Terminal login verified by the user on 2026-10-20. This account uses Delta, not DeltaAI. Check current allocation and partition access before deciding what jobs it can run.

## Authentication and notification boundary

Delta requires an NCSA password and NCSA Duo MFA. Ordinary accounts cannot use SSH key pairs in place of this authentication. Never run `ssh-copy-id`, store passwords, automate Duo, or copy private keys for this workflow.

SSH connection sharing lets an agent use a connection the human already authenticated on the same origin machine and Unix account. A private control socket is local authentication state. It is not copied to another machine or committed. `tmux` preserves the remote shell, but does not authenticate SSH or keep a dead network connection usable. Slurm batch jobs continue after SSH disconnects.

When human action is needed, invoke the question tool, such as Codex `request_user_input_async` or Claude `AskUserQuestion`, rather than only sending prose or ending the turn. Example question:

> Delta authentication is needed on D-3. On your Mac run `ssh -t D-3 'ssh -MNf delta'`, enter your NCSA password there, and approve Duo. Do not share credentials here. Reply "Ready" once it finishes so I can check the connection and continue.

Keep that question pending. Resume dependent access only after the reply, then verify it actually worked. Never repeatedly trigger login or Duo prompts. If the question tool is unavailable, state the notification limitation explicitly.

## One-time setup on each origin

From this skill directory:

```bash
python3 scripts/setup-delta-ssh.py
```

This creates `~/.ssh/ncsa-delta.conf`, prepends its Include to `~/.ssh/config`, and creates `~/.ssh/control` with mode 0700. Config files have mode 0600. Existing config is retained with a one-time backup at `~/.ssh/config.before-delta-sharing`. Remove the added Include to undo this setup. The default `delta` alias is pinned to `dt-login01.delta.ncsa.illinois.edu`; `delta-login01` through `delta-login04` select individual nodes.

Host verification remains enabled. Before the first login, compare the offered or scanned ED25519 key against the current official login guide. On 2026-10-20 it was `SHA256:mIv7OqNSuuWnu1tlY//wG4gWAn4z0mbE11KkBXDAY/g`. Only add a matching key for the intended hostname to `~/.ssh/known_hosts`; stop on a mismatch. Do not disable host-key checks. This setup script does not install host keys or attempt login.

## Human login commands

For an agent running on the Mac, run in a local terminal:

```bash
ssh -MNf delta
```

For an agent running on a dminer, run the corresponding command from the Mac:

```bash
ssh -t D-1 'ssh -MNf delta'
ssh -t D-2 'ssh -MNf delta'
ssh -t D-3 'ssh -MNf delta'
ssh -t D-4 'ssh -MNf delta'
```

Run only the command for the host the agent needs. Complete password and Duo directly in the terminal. The inner SSH process backgrounds on that dminer after authentication, so the outer session can exit. The master persists for 30 minutes with no client connections, and can expire earlier if the network fails or the server closes it. It is not a fixed 30-minute credential grant. Use the exact same alias for login and later commands.

## Agent preflight and commands

On the agent's execution host:

```bash
ssh -O check delta
ssh -o BatchMode=yes -o ConnectTimeout=10 delta 'hostname; whoami'
```

`ssh -O check` must succeed before remote commands. Use `BatchMode=yes` on every agent command, including SSH commands inside rsync and scp, so a missing master fails without a password or Duo prompt. If access fails, invoke the question tool with the matching human login command; a successful check alone does not prove the server connection is still healthy.

For a persistent shell, have the human run on the authenticated origin:

```bash
ssh -t delta 'tmux new-session -A -s agent-work'
```

The agent can create a detached session if absent:

```bash
ssh -o BatchMode=yes delta 'tmux has-session -t agent-work 2>/dev/null || tmux new-session -d -s agent-work'
```

Record `hostname`, session name, code revision, job IDs, and output paths in the experiment's own notes. Detach with Ctrl-b then d. Reconnect to the same login node. Do not inject commands into a shell the user is actively using; prefer ordinary SSH commands and Slurm submission. If a login node is unavailable, ask about switching aliases; existing tmux sessions remain on their original node.

## Experiments use Slurm

Login nodes are for preparation, submission, and monitoring. Run training, benchmarks, and substantial preprocessing through `sbatch`, `salloc`, or `srun` on allocated compute nodes. A tmux shell on a login node is not a compute allocation.

Check live resources and account associations:

```bash
ssh -o BatchMode=yes delta 'sinfo -o "%P|%a|%l|%G"; squeue -u "$USER"; sacctmgr -nP show assoc where user="$USER" format=Account,Partition,QOS'
```

Verify the actual account, allocation balance, partition policy, storage paths, quotas, and environment before writing a job script. Account information may require the allocation portal or a site-specific command if Slurm accounting visibility is restricted. Do not guess an account name or assume login access proves GPU eligibility. Ask through the question tool for missing user action or allocation details that cannot be retrieved.

Submit an experiment-specific script with explicit account, partition, time, CPU, memory, GPU, and output requirements. Record the `sbatch` job ID and check `squeue` / `sacct` for its result. Keep authoritative code and durable outputs in verified persistent storage; follow current NCSA purge rules for scratch. A submitted job is not a completed experiment.

## End access

After agent work finishes, close the shared connection on each origin that was authenticated:

```bash
ssh -O exit delta
```

From the Mac, for example: `ssh D-3 'ssh -O exit delta'`. Coordinate closure if another agent is still using it; do not terminate its active channels unexpectedly. This closes SSH channels, not submitted Slurm jobs or detached tmux sessions. Never cancel jobs or kill shared sessions without task authorization.

## Sources and drift

- [NCSA Delta login, MFA, host keys, and tmux](https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/login.html)
- [NCSA Delta Slurm job execution](https://docs.ncsa.illinois.edu/systems/delta/en/latest/user_guide/running_jobs.html)

Policy and hostname details checked on 2026-10-20. Recheck official documentation when access behavior changes. Probe connection state live rather than treating this date or a prior successful login as current authorization.
