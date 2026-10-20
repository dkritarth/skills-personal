#!/usr/bin/env python3
"""Install per-user Delta aliases and connection sharing; never authenticate."""

import argparse
from pathlib import Path
import shutil


def install(ssh_dir: Path) -> None:
    ssh_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    ssh_dir.chmod(0o700)
    control_dir = ssh_dir / "control"
    control_dir.mkdir(exist_ok=True, mode=0o700)
    control_dir.chmod(0o700)
    snippet = ssh_dir / "ncsa-delta.conf"
    # A fixed login node makes tmux sessions reachable after reconnecting.
    content = "# Managed by msu-dminer-fleet/scripts/setup-delta-ssh.py\n"
    content += "Host delta delta-ncsa\n    HostName dt-login01.delta.ncsa.illinois.edu\n"
    for number in range(1, 5):
        content += (
            f"\nHost delta-login{number:02d}\n"
            f"    HostName dt-login{number:02d}.delta.ncsa.illinois.edu\n"
        )
    content += f'''
Host delta delta-ncsa delta-login01 delta-login02 delta-login03 delta-login04
    User kdandapat
    PreferredAuthentications keyboard-interactive,password
    PubkeyAuthentication no
    ControlMaster auto
    ControlPath "{control_dir}/%C"
    ControlPersist 30m
    ServerAliveInterval 60
    ServerAliveCountMax 3
    ForwardAgent no
    StrictHostKeyChecking yes
'''
    config = ssh_dir / "config"
    include = f'Include "{snippet}"'
    previous = config.read_text() if config.exists() else ""
    # Validate inputs before changing config. Preserve existing bytes and make
    # a one-time backup; the first Include takes precedence over older aliases.
    if snippet.exists() and not snippet.read_text().startswith(
        "# Managed by msu-dminer-fleet/scripts/setup-delta-ssh.py\n"
    ):
        raise SystemExit(f"Refusing to replace unmanaged file: {snippet}")
    if snippet.exists() and snippet.read_text() != content:
        backup = snippet.with_name("ncsa-delta.conf.before-fleet")
        if not backup.exists():
            shutil.copy2(snippet, backup)
            backup.chmod(0o600)
    snippet.write_text(content)
    snippet.chmod(0o600)
    if not previous.startswith(include + "\n"):
        backup = ssh_dir / "config.before-delta-sharing"
        if config.exists() and not backup.exists():
            shutil.copy2(config, backup)
            backup.chmod(0o600)
        config.write_text(include + "\n" + previous)
    config.chmod(0o600)
    print("Delta SSH configured. Human login on THIS machine: ssh -MNf delta")
    print("Agent check: ssh -O check delta; logout: ssh -O exit delta")
    print("Host keys must match NCSA documentation before the first login.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ssh-dir", type=Path, default=Path.home() / ".ssh")
    install(parser.parse_args().ssh_dir.expanduser().resolve())
