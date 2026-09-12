# Development environment

The ck3chronicle checkout on this machine is:

`C:\Users\nateb\Documents\ck3chronicle`

The source repository is:

`https://github.com/ck3user75233/ck3chronicle.git`

The managed workspace permits work in this checkout. Local runtime evidence is
kept in ignored application directories and is not source code. Captured CK3
logs, SQLite databases, pending copies, review material, workbooks, and
generated evaluation results must remain outside Git.

## Python

Use the repository environment for agent-run development and verification:

```powershell
Set-Location 'C:\Users\nateb\Documents\ck3chronicle'
$python = (Resolve-Path -LiteralPath '.\.venv\Scripts\python.exe').Path

& $python -B -m unittest discover -s tests -v
& $python -I -B -c "import ck3chronicle; import ck3chronicle.cli"
& $python -I -B -m pip check
```

If `.venv` fails, diagnose or restore it as part of the task. Optional
owner-created environments are not required for routine verification.

## Runtime safety

Consult `docs/PROJECT_STATUS.md` before running commands that capture evidence,
write to the production database, process pending captures, start the watcher,
or change configured runtime roots. Ordinary compilation, imports, unit tests,
and read-only inspection should be performed by the agent doing the work.
