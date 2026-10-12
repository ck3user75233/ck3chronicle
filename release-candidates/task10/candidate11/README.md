# Proposed Windows release candidate 11

This folder preserves the actual Task 10 install ZIP alongside the source checkpoint.
It is **a proposed release candidate, not an accepted production deployment**.
The archive was copied unchanged from the received 2026-10-12 C11 delivery.

| Item | Identity |
|---|---|
| Archive | `ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip` |
| Size | 20,980,042 bytes |
| ZIP SHA-256 | `97f52263beca3387390d220d33ea461d6e60edaca7e70314096f473566750771` |
| Application | 0.0.3; wheel SHA-256 `f03afb5b6abb5d7ee42522d832089d16d20a259374a987ae88dcb0f1a523ee38` |
| Manual | `manual-20261012-r4-application0.0.3`; 18 inputs |
| Manual input-manifest SHA-256 | `b58a48f4159368b01a2e742a0e2f33b7740c74a850273a602b5ac24fa3a240d2` |
| Model | `2b12932103f3a3111a4e1880`, catalog order 9 |
| Model manifest SHA-256 | `02c70654c3ffa9678df80108985206a12c92bb67b0c36311fbec393b329e1505` |
| Learner | `2ec4b671428a75de65c0ccd614b3bf15e04fdb83444689821d71864c2caaf485`, v61, catalog order 10 |
| Learner manifest SHA-256 | `9ba2c5faa9253aafb2ddea5dc473819be68d43f669abc63a23463d6613151b8e` |
| Release manifest SHA-256 | `7d820a624be69a96a182cf609b73cc6ef7fcbde3c110c78ab2be823807bf4af7` |

[SHA256SUMS](SHA256SUMS) covers the ZIP and the byte-identical copy of its
[release manifest](release-manifest.json). That original manifest retains its
build-time source-baseline and acceptance statements. This README is a separate
checkpoint summary, not a rewrite of the original delivery receipt.

The ZIP has one versioned root folder, 1,506 payload files and its manifest.
It includes the private Python 3.12.14 runtime, application, chardet 7.6.0,
ripgrep 15.2.0, retained models/Learners, GUI and text setup, launchers, manual
and existing license notices. Python, pip and Git are not needed to run the
extracted application. Windows x64, Windows PowerShell 5.1/.NET desktop
components and the user's actual readable CK3 folders remain prerequisites.

## Extract and start

1. Compare the ZIP's SHA-256 with `SHA256SUMS`, for example using PowerShell
   `Get-FileHash -Algorithm SHA256 -LiteralPath '.\ck3chronicle-0.0.3-task10b-candidate11-win-x64.zip'`.
2. Extract the whole archive to a new application location. Keep the versioned
   folder's contents together; do not overlay another installation.
3. Open PowerShell in the extracted versioned folder and run `.\Verify.cmd`.
4. Run `.\Setup.cmd`, review the local CK3 folders and choose separate writable
   settings/data locations. For an isolated trial, supply explicit new locations:
   `.\Setup.cmd --config 'D:\ChronicleC11\settings\paths.toml' --data-root 'D:\ChronicleC11\data'`.
   Replace these example paths with suitable locations on that workstation.
5. When ready to observe CK3, run
   `.\Start.cmd --config 'D:\ChronicleC11\settings\paths.toml'`.
   Starting observation can process retained pending captures and perform configured
   retention. Use the same saved configuration for every command.
6. Press Ctrl+C in that terminal and wait for return. Before maintenance, run
   `.\ck3chronicle.cmd --config 'D:\ChronicleC11\settings\paths.toml' runtime-stop`.

Read the included `docs/user/INSTALLATION.md` and manual contents for full setup,
configuration, retention and recovery behavior. Setup saves configuration; it does
not start observation. This checkpoint preparation did not execute these steps.

## Evidence and limits

TREK-10 CMT-193 delivered C11; CMT-194 received its local bundle, and TREK-11
CMT-195 received r4. Prior receiving authenticated all 1,506 payloads, all 18
manual inputs and 157 manual links, and checked installed help/imports/resources.
It reused earlier genuine workflow evidence for corresponding unchanged bytes.
The same chat authored the manual and assembly; that receipt is not independent
or blind acceptance. This Advisory review independently rehashed the ZIP and
every payload and verified the copied files against their originals.

Actual C11 external placement, clean-Windows operation, and ordinary-console
Watcher Ctrl+C followed by explicit handler stop remain with TREK-16. The optional
sign-in shortcut is unexercised. Owner acceptance and production activation remain
separate. See [current receiving](../../../docs/TASK10_HANDOFF.md) and
[distribution handoff](../../../docs/task10/DISTRIBUTION_HANDOFF.md).

No runtime database, captured log, machine configuration or Trekker store is
included. Historical paths remain in already-retained model metadata, Learner
tools and application package metadata; these authenticated bytes are preserved.
The archive is not a sanitized public marketing release. Existing dependency
payloads/notices are preserved under the Owner's 2026-10-12 direction; no new
upstream download or comparison is an acceptance prerequisite.

The source checkpoint supplies [build recipes](../../../packaging/windows/README.md).
The original machine-specific input plan and separate wheel inputs remain local
evidence, so this is not a claim of a clone-only byte-identical rebuild. The ZIP
itself supplies the complete runnable candidate without those build inputs.
