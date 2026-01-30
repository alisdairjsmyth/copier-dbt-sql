# use PowerShell instead of sh:
set shell := ["powershell.exe", "-c"]

# List available just commands (default)
default:
  @just --list

# Activate the virtual environment
activate:
  .venv\Scripts\Activate.ps1

# (git) Stage all changes
add:
  git add .

# (git) Amend the last commit
amend:
  git commit --amend

# (git) Initialize environment after clone
clone:
  uv venv
  just activate
  just sync
  pre-commit install --install-hooks

# (git) Commit changes with commitizen
commit:
  cz commit

# (git) Delete local (merged) branch (usage: just delete-branch feature/my-feature)
delete-branch name:
  just prune
  git branch -d {{name}}

# (git) Create a feature branch with prefix (usage: just feat my-feature)
feat name:
  @just master
  git checkout -b feature/{{name}}

# (git) Create a fix branch with prefix (usage: just fix bug-123)
fix name:
  @just master
  git checkout -b fix/{{name}}

# (git) List local branches
list-branches:
  git branch -l

# Lock project dependencies
lock:
  uv lock

# (git) Switch to master branch and pull latest changes
master:
  git checkout master
  just pull

# (git) Run pre-commit hooks on all files
pre-commit:
  pre-commit run --all-files

# (git) Sync and prune local tracking branches
prune:
  git fetch --prune
  @echo "Remote branches pruned. Use 'git branch -d' for local cleanup."

# (git) Pull changes from the remote repository
pull:
  git pull --rebase origin master

# (git) Push changes to the remote repository
push: pull
  git push origin HEAD

# Sync project dependencies to the virtual environment
sync:
  uv sync --group dev

# Update databricks CLI to the latest version (usage: just update-databricks-cli 0.282.0)
update-databricks-cli version:
  winget upgrade Databricks.DatabricksCLI --version {{version}}
