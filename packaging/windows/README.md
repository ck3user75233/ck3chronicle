# Windows outer distribution

Owner: Launch & Distribution, Task 10B / TREK-10. Pipeline supplies the wheel;
this directory never rebuilds it or writes application configuration itself.

`build.py --plan <absolute input-plan.json> --output <new output directory>` runs
offline with the development Python. The plan pins every runtime file, wheel,
tool, launcher, document and notice with SHA-256. It installs wheel payloads using
the purelib/data scheme, verifies RECORD, records all installed member hashes,
generates seven CMD entry points, inventories the completed folder and writes a ZIP
and separate receipt. Existing candidate folders/archives are never replaced.

The current recipe targets Windows x64 CPython 3.12. Runtime input is an explicit
clean runtime inventory (no site-packages, developer tools or user settings).
`python312._pth` restricts imports for launchers and application-spawned children.
The shipped runtime supplies stdlib/native DLLs; chardet is installed from its
received cp312 wheel. No user pip, Python, Git or download step is required.

The canonical input plan and build output are ignored evidence, linked from
[DISTRIBUTION_HANDOFF.md](../../docs/task10/DISTRIBUTION_HANDOFF.md).
Owner direction, 2026-10-12: preserve the existing working Python/ripgrep payloads
and included notices. Additional upstream verification, comparison downloads and
remote binary correspondence are outside Task 10. The retained acquisition script
and older acquisition instructions are historical; do not run them for this work.
Continue local bundle inventory/hashes and installed-product receiving. These
identify the actual delivery and its operation. Current assembly uses the received
0.0.3 wheel and the complete corrected r4 manual; exact pins are in the handoff.

`Setup.cmd` opens the Windows Forms wizard through the bundled `pythonw.exe`.
`Setup.ps1` owns presentation; `setup_gui_backend.py` passes JSON requests to
Pipeline's received setup/config/doctor APIs using the private Python runtime.
No GUI library is installed or downloaded. Windows PowerShell 5.1 and its .NET
Framework Windows Forms components are platform dependencies. Execution policy
Bypass applies only to that PowerShell process; no saved policy is changed.
`Setup-Text.cmd` retains terminal setup via `launcher.py`. The GUI selects healthy folders by default, rechecks edits, and confirms all
locations on its final Save settings page. Text setup retains explicit per-root
confirmation. Fixed helper locations are displayed as text, without disabled
Browse controls.
The central preview/Apply owns validation, defaults, selection and initialization.
`Start.cmd` invokes the existing foreground watcher; Ctrl+C is handled by that
component. `runtime-stop` remains an explicit application command.

`Place-And-Verify.ps1` runs setup once. Its optional `-VerifyRepeatSetup` switch
requests a clearly labelled additional preservation test. The receipt records
whether repeat testing was requested/performed; skipping it is not a failure.

For a documentation freeze, refresh the issued Docs record, agree exact content,
pin every document hash in a new plan, then build a new labelled archive. Keep
earlier candidates and receipts. Verify the completed archive again; never edit
an already delivered bundle or compete for Docs' source files.
