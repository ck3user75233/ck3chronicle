# Windows launcher reference

Application **0.0.3**, Windows x64. Keep the extracted bundle together and run
commands from its folder. In PowerShell, prefix a CMD filename with `.\` and
quote paths containing spaces. Follow [Installation and launch](INSTALLATION.md)
for the wizard, prerequisites, startup option and shutdown sequence.

| Entry point | Purpose |
|---|---|
| `Verify.cmd` | Check bundle contents against `release-manifest.json`. Compare the ZIP hash with its separate receipt for independent identity evidence. |
| `Setup.cmd` | Open the Windows Forms setup wizard. Final **Save settings** applies the reviewed choices. |
| `Setup-Text.cmd` | Use terminal setup prompts and final Apply. |
| `Start.cmd` | Run foreground observation with the selected configuration. Launch CK3 separately. |
| `ck3chronicle.cmd` | Use the [application commands](CLI_REFERENCE.md), including doctor, capture, ingest, runs, report and runtime-stop. |
| `ck3chronicle-model-release.cmd` | Inspect/evaluate/register model packages through the [model catalog commands](RELEASE_REFERENCE.md#model-catalog-commands). |
| `ck3chronicle-learner-release.cmd` | Use the [retained Learner interfaces](RELEASE_REFERENCE.md#select-and-run-an-exact-learner). |

Use the same `--config PATH` with Setup, Start and later application commands
when you choose a nondefault settings file. For the application CLI it precedes
the subcommand. Model/Learner administration instead uses explicit resource,
output and log paths as described in its reference.

Setup cancellation before saving exits 130. Launcher failures exit 1; application
commands retain their own documented codes. Doctor's exit 2 includes warnings
and unverified read-only findings as well as errors. Read each finding.

Stop the foreground watcher with Ctrl+C and wait for it to return, then use
`.\ck3chronicle.cmd --config 'FULL PATH' runtime-stop` before changing that setup.
The handler is independent of the watcher, and later requests can start it again.
Application files, settings and evidence have separate locations. Removing the
extracted folder leaves separately stored user data in place.

[Manual contents](README.md)
