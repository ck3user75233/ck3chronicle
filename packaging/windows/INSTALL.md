# Install ck3chronicle for Windows

Application **0.0.3**, Windows x64. Read [Product Version, Introduction and
Orientation](docs/user/README.md) to understand the product. Follow the
[installation guide](docs/user/INSTALLATION.md) for prerequisites, folder choices,
launch and optional Windows sign-in startup.

Compare the ZIP hash with its separate receipt, then extract the whole ZIP to a
new folder. Keep the bundle together and user data separate. From PowerShell
in the extracted folder:

```powershell
.\Verify.cmd
.\Setup.cmd
```

Review the wizard's folders and model, then choose **Save settings** on its final
review page. Keep the returned settings and database paths. `Setup-Text.cmd`
provides terminal prompts. To begin observation with default settings:

```powershell
.\Start.cmd
```

If you chose a different configuration file, pass `--config 'FULL PATH'` to
Setup, Start and every later application command. For the application CLI the
option precedes its subcommand. Launch CK3 normally after starting observation.

For an existing setup, stop its watcher with Ctrl+C and wait for it to return,
then run `.\ck3chronicle.cmd --config 'FULL PATH' runtime-stop` before changing settings
or replacing files. Use that setup's exact configuration. A fresh setup with
separate data is independent of other setups.

Continue with [everyday workflows](docs/user/WORKFLOWS.md).
[Release notes](RELEASE_NOTES.md) and [third-party notices](THIRD_PARTY_NOTICES.md)
describe this bundle. [Manual contents](docs/user/README.md).
