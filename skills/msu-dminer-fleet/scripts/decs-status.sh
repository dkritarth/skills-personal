#!/usr/bin/env bash
set -u

hosts=(C-01 C-02 C-03 C-04 C-05 C-06 C-07 C-08 C-09)

for host in "${hosts[@]}"; do
  printf '\n=== %s ===\n' "$host"
  if ! ssh -o BatchMode=yes -o ConnectTimeout=8 "$host" 'bash -s' <<'REMOTE'
printf 'host: %s\n' "$(hostname)"
printf 'uptime/load: %s\n' "$(uptime | sed 's/^[[:space:]]*//')"
printf 'logical CPUs: %s\n' "$(getconf _NPROCESSORS_ONLN)"
free -h | awk '/^Mem:/ {printf "memory: %s used / %s total, %s available\n", $3, $2, $7}'
printf 'highest CPU processes:\n'
ps -eo user:20,pid,pcpu,pmem,etime,comm --sort=-pcpu | head -6
df -hP /egr/scratch /localscratch 2>/dev/null | awk 'NR == 1 || !seen[$6]++ {print}'
REMOTE
  then
    printf 'status: unreachable or authentication rejected\n'
  fi
done
