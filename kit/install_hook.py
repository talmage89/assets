"""Install a hook for this worktree only; never overwrite another hook."""
import subprocess
from pathlib import Path
root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
# Hook path is worktree-local; common .git/hooks must not affect another worktree.
folder=root/'build/hooks';folder.mkdir(parents=True,exist_ok=True)
path=folder/'pre-commit'
body='#!/bin/sh\nset -eu\nexec python3 "$(git rev-parse --show-toplevel)/kit/repo_check.py" --staged\n'
if path.exists() and path.read_text()!=body:raise SystemExit('Existing worktree hook differs; refusing to overwrite')
path.write_text(body);path.chmod(0o755)
subprocess.run(['git','config','extensions.worktreeConfig','true'],check=True)
subprocess.run(['git','config','--worktree','core.hooksPath',str(folder)],check=True)
print('Installed worktree-local pre-commit hook:',path)
