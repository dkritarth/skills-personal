#!/usr/bin/env bash
set -u

hosts=(D-1 D-2 D-3 D-4)

for host in "${hosts[@]}"; do
  printf '\n=== %s ===\n' "$host"
  if ! ssh -o BatchMode=yes -o ConnectTimeout=8 "$host" 'bash -s' <<'REMOTE'
printf 'host: %s\n' "$(hostname)"
printf 'load: %s\n' "$(cut -d " " -f 1-3 /proc/loadavg)"
free -h | awk '/^Mem:/ {printf "memory: %s used / %s total, %s available\n", $3, $2, $7}'
if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu,temperature.gpu --format=csv,noheader
  gpu_jobs=$(nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null || true)
  if [ -n "$gpu_jobs" ]; then
    printf 'gpu processes:\n%s\n' "$gpu_jobs"
  else
    printf 'gpu processes: none reported\n'
  fi
else
  printf 'gpu: nvidia-smi unavailable\n'
fi
df -hP / /data /mnt/bulk 2>/dev/null | awk 'NR == 1 || !seen[$6]++ {print}'
REMOTE
  then
    printf 'status: unreachable\n'
  fi
done
