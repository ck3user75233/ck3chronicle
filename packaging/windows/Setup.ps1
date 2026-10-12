[CmdletBinding()]
param([string]$ConfigPath, [string]$DataRoot, [string]$Database)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
[Windows.Forms.Application]::EnableVisualStyles()
$script:bundle = $PSScriptRoot
$script:configPath = $ConfigPath
$script:fixedSettings = [bool]$ConfigPath
$script:fixedData = [bool]$DataRoot
$script:initialDataRoot = $DataRoot
$script:databaseOverride = $Database
$script:pageIndex = 0
$script:busy = $false
$script:loaded = $false
$script:finished = $false
$script:exitCode = 130
$script:existing = $false
$script:details = @{}
$script:readyRequest = $null
$script:fields = [ordered]@{}
$script:models = @()
$script:form = New-Object Windows.Forms.Form
$form.Text = 'CK3Chronicle Setup'
$form.Font = New-Object Drawing.Font('Segoe UI', 10)
$form.Size = New-Object Drawing.Size(900, 780)
$form.MinimumSize = New-Object Drawing.Size(740, 600)
$form.StartPosition = 'CenterScreen'
$form.AutoScaleMode = 'Dpi'
$form.MaximizeBox = $false
$header = New-Object Windows.Forms.Panel
$header.Dock = 'Top'; $header.Height = 92; $header.BackColor = [Drawing.Color]::White
$script:title = New-Object Windows.Forms.Label
$title.Location = New-Object Drawing.Point(24, 16); $title.Size = New-Object Drawing.Size(820, 34)
$title.Font = New-Object Drawing.Font('Segoe UI', 18)
$script:subtitle = New-Object Windows.Forms.Label
$subtitle.Location = New-Object Drawing.Point(26, 56); $subtitle.Size = New-Object Drawing.Size(820, 30)
$header.Controls.AddRange(@($title, $subtitle))
$footer = New-Object Windows.Forms.Panel
$footer.Dock = 'Bottom'; $footer.Height = 92
$script:status = New-Object Windows.Forms.Label
$status.Location = New-Object Drawing.Point(24, 7); $status.Size = New-Object Drawing.Size(820, 34)
$status.Text = 'Reading setup information...'
$script:back = New-Object Windows.Forms.Button
$back.Text = '< Back'; $back.Size = New-Object Drawing.Size(92, 30); $back.Anchor = 'Right, Bottom'
$script:next = New-Object Windows.Forms.Button
$next.Text = 'Next >'; $next.Size = New-Object Drawing.Size(92, 30); $next.Anchor = 'Right, Bottom'
$script:cancel = New-Object Windows.Forms.Button
$cancel.Text = 'Cancel'; $cancel.Size = New-Object Drawing.Size(92, 30); $cancel.Anchor = 'Right, Bottom'
$detailButton = New-Object Windows.Forms.Button
$detailButton.Text = 'Details...'; $detailButton.Location = New-Object Drawing.Point(24, 49)
$detailButton.Size = New-Object Drawing.Size(92, 30)
$footer.Controls.AddRange(@($status, $back, $next, $cancel, $detailButton))
$footer.add_Resize({
    $script:cancel.Location = New-Object Drawing.Point(($footer.ClientSize.Width - 116), 49)
    $script:next.Location = New-Object Drawing.Point(($footer.ClientSize.Width - 216), 49)
    $script:back.Location = New-Object Drawing.Point(($footer.ClientSize.Width - 316), 49)
    $script:status.Width = $footer.ClientSize.Width - 48
})
$script:body = New-Object Windows.Forms.Panel
$body.Dock = 'Fill'
$form.Controls.AddRange(@($body, $footer, $header))
$script:pages = @()
for ($i = 0; $i -lt 5; $i++) {
    $page = New-Object Windows.Forms.FlowLayoutPanel
    $page.Dock = 'Fill'; $page.FlowDirection = 'TopDown'; $page.WrapContents = $false
    $page.AutoScroll = $true; $page.Padding = New-Object Windows.Forms.Padding(24, 12, 24, 12)
    $page.Visible = $false
    $body.Controls.Add($page); $script:pages += $page
}

function Add-Label($Parent, [string]$Text, [bool]$Heading = $false) {
    $label = New-Object Windows.Forms.Label
    $label.Text = $Text; $label.AutoSize = $true
    $label.MaximumSize = New-Object Drawing.Size(800, 0)
    $label.Margin = New-Object Windows.Forms.Padding(0, 7, 0, 7)
    if ($Heading) { $label.Font = New-Object Drawing.Font('Segoe UI', 10, [Drawing.FontStyle]::Bold) }
    $Parent.Controls.Add($label)
    return $label
}
function Add-Folder($Parent, [string]$Value) {
    $row = New-Object Windows.Forms.Panel
    $row.Size = New-Object Drawing.Size(800, 28); $row.Margin = New-Object Windows.Forms.Padding(0, 2, 0, 3)
    $entry = New-Object Windows.Forms.TextBox
    $entry.Text = $Value; $entry.Dock = 'Fill'
    $browse = New-Object Windows.Forms.Button
    $browse.Text = 'Browse...'; $browse.Dock = 'Right'; $browse.Width = 92; $browse.Tag = $entry
    $browse.add_Click({
        param($sender, $eventArgs)
        $picker = New-Object Windows.Forms.FolderBrowserDialog
        $picker.Description = 'Choose a folder'; $picker.SelectedPath = $sender.Tag.Text
        $picker.ShowNewFolderButton = ($sender.Tag -eq $script:settingsEntry -or $sender.Tag -eq $script:dataEntry)
        try {
            if ($picker.ShowDialog($script:form) -eq 'OK') {
                $sender.Tag.Text = $picker.SelectedPath
                if ($sender.Tag -eq $script:settingsEntry) { Update-SettingsLocation }
            }
        } finally { $picker.Dispose() }
    })
    $row.Controls.AddRange(@($entry, $browse)); $Parent.Controls.Add($row)
    return $entry
}
function Update-Buttons {
    $script:back.Enabled = (-not $script:busy -and $script:pageIndex -gt 0 -and $script:pageIndex -lt 4)
    $script:next.Enabled = ($script:loaded -and -not $script:busy -and ($script:pageIndex -ne 3 -or $null -ne $script:readyRequest))
    $script:next.Text = if ($script:finished) { 'Finish' } elseif ($script:pageIndex -eq 3) { 'Save settings' } elseif ($script:pageIndex -eq 2) { 'Review >' } else { 'Next >' }
    $script:cancel.Enabled = (-not $script:busy -and -not $script:finished)
    $script:body.Enabled = -not $script:busy
}
function Show-Page([int]$Index) {
    $script:pageIndex = $Index
    $titles = @('1 of 4 - Installation and settings', '2 of 4 - Choose your CK3 folders', '3 of 4 - Saved runs and model', '4 of 4 - Review and save', 'Setup complete')
    $subtitles = @('Check these locations, then click Next to choose your CK3 folders.',
        'Folders that pass checks are selected for you. Review or change them below.',
        'Choose where to save history and which model processes new runs.',
        'Review your choices, then click Save settings to finish setup.',
        'Your settings are saved. The watcher has not been started.')
    $script:title.Text = $titles[$Index]; $script:subtitle.Text = $subtitles[$Index]
    $guidance = @('Next: choose the CK3 folders to read.',
        'Next: choose storage and a processing model.',
        'Review shows all your choices before anything is saved.',
        'Save settings completes setup. Back lets you change your choices.',
        'Setup completed successfully.')
    $script:status.Text = $guidance[$Index]
    for ($i = 0; $i -lt 5; $i++) { $script:pages[$i].Visible = ($i -eq $Index) }
    $script:pages[$Index].BringToFront()
    Update-Buttons
}
function Show-Details {
    $dialog = New-Object Windows.Forms.Form
    $dialog.Text = 'CK3Chronicle - setup details'; $dialog.Size = New-Object Drawing.Size(820, 580)
    $dialog.StartPosition = 'CenterParent'; $dialog.Font = $script:form.Font
    $text = New-Object Windows.Forms.TextBox
    $text.Multiline = $true; $text.ReadOnly = $true; $text.ScrollBars = 'Both'; $text.Dock = 'Fill'
    $text.Font = New-Object Drawing.Font('Consolas', 10)
    $text.Text = ($script:details | ConvertTo-Json -Depth 25)
    $dialog.Controls.Add($text)
    try { [void]$dialog.ShowDialog($script:form) } finally { $dialog.Dispose() }
}
function Start-Backend($Request, [string]$Message, [scriptblock]$Completed) {
    if ($script:busy) { return }
    $script:busy = $true; $script:status.Text = $Message; Update-Buttons
    try {
        $info = New-Object Diagnostics.ProcessStartInfo
        $info.FileName = Join-Path $script:bundle 'runtime\python.exe'
        $backend = Join-Path $script:bundle 'setup_gui_backend.py'
        $info.Arguments = '-I -B -X utf8 "' + $backend + '"'
        $info.UseShellExecute = $false; $info.CreateNoWindow = $true
        $info.RedirectStandardInput = $true; $info.RedirectStandardOutput = $true; $info.RedirectStandardError = $true
        $info.StandardOutputEncoding = New-Object Text.UTF8Encoding($false)
        $info.StandardErrorEncoding = New-Object Text.UTF8Encoding($false)
        $script:process = New-Object Diagnostics.Process
        $script:process.StartInfo = $info
        [void]$script:process.Start()
        $script:outputTask = $script:process.StandardOutput.ReadToEndAsync()
        $script:errorTask = $script:process.StandardError.ReadToEndAsync()
        $bytes = [Text.Encoding]::UTF8.GetBytes(($Request | ConvertTo-Json -Depth 20 -Compress))
        $script:process.StandardInput.BaseStream.Write($bytes, 0, $bytes.Length)
        $script:process.StandardInput.Close()
        $script:afterJob = $Completed
        $script:timer.Start()
    } catch {
        $script:busy = $false; $script:details = @{error=$_.Exception.Message}
        $script:status.Text = 'Could not start this check. Open Details for the error.'; Update-Buttons
    }
}
$script:timer = New-Object Windows.Forms.Timer
$timer.Interval = 100
$timer.add_Tick({
    if (-not $script:process.HasExited) { return }
    $script:timer.Stop()
    try {
        $outputText = $script:outputTask.GetAwaiter().GetResult()
        $errorText = $script:errorTask.GetAwaiter().GetResult()
        $value = $outputText | ConvertFrom-Json
        if ($script:process.ExitCode -ne 0 -or $value.error) {
            throw $(if ($value.error) { $value.error } else { $errorText })
        }
        $script:busy = $false
        & $script:afterJob $value
    } catch {
        $script:busy = $false; $script:details = @{error=$_.Exception.Message}
        $script:readyRequest = $null
        $script:status.Text = 'This check needs attention. Open Details for the error.'
    } finally { $script:process.Dispose(); Update-Buttons }
})
function Get-PathMessage($Findings, [string]$Field) {
    $checks = @($Field)
    if ($Field -eq 'root_game') { $checks += 'ck3_identity' }
    if ($Field -eq 'root_logs') { $checks += @('error_log', 'logs_identity') }
    $messages = @()
    foreach ($item in $Findings) {
        if ($item.check -notin $checks) { continue }
        if ($item.severity -eq 'healthy' -and $item.check -eq $Field) { $messages += 'Folder found and readable.' }
        elseif ($item.severity -eq 'healthy' -and $item.check -eq 'ck3_identity') { $messages += 'Expected CK3 folders and ck3.exe found.' }
        elseif ($item.severity -eq 'healthy') { $messages += $item.impact }
        else { $messages += ('Needs attention: ' + $item.impact + ' ' + $item.action) }
    }
    if (-not $messages.Count) { return 'Not checked yet.' }
    return $messages -join ' '
}
function Test-PathReady($Findings, [string]$Field) {
    # Interpret Pipeline findings only; no independent filesystem validation.
    $checks = @($Field)
    if ($Field -eq 'root_game') { $checks += 'ck3_identity' }
    if ($Field -eq 'root_logs') { $checks += @('error_log', 'logs_identity') }
    $rootFound = @($Findings | Where-Object { $_.check -eq $Field -and $_.severity -eq 'healthy' }).Count -gt 0
    $attention = @($Findings | Where-Object { $_.check -in $checks -and $_.severity -ne 'healthy' }).Count -gt 0
    return ($rootFound -and -not $attention)
}
function Show-UnselectedFolder {
    foreach ($field in $script:fields.Values) {
        if (-not $field.Accept.Checked) {
            $script:status.Text = 'Review ' + $field.Label + ': check its location or select Use this folder to keep it.'
            $script:pages[1].ScrollControlIntoView($field.Entry.Parent)
            $field.Accept.Focus() | Out-Null
            return
        }
    }
}
function Load-Settings {
    $script:loaded = $false
    Start-Backend @{operation='load';config=$script:configPath;data_root=$script:initialDataRoot} 'Checking saved settings and suggested CK3 folders...' {
        param($value)
        $script:details = $value; $script:existing = $value.existing
        $script:configPath = $value.config
        $script:settingsEntry.Text = Split-Path -Parent $value.config
        foreach ($key in $script:fields.Keys) {
            $field = $script:fields[$key]
            $saved = $value.saved.paths.$key
            $field.Entry.Text = if ($saved) { $saved } else { $value.suggestions.candidates.$key }
            $source = if ($saved) { $value.saved } else { $value.suggestions }
            $field.Status.Text = Get-PathMessage $source.findings $key
            $field.CheckedPath = $field.Entry.Text
            $field.Changed = $false
            $field.Accept.Checked = Test-PathReady $source.findings $key
        }
        $script:dataEntry.Text = $value.defaults.paths.root_wip
        $script:models = @($value.models.choices | Where-Object { $_.authenticated })
        $script:modelBox.Items.Clear()
        $current = $value.defaults.model.package_id
        foreach ($model in $script:models) {
            $label = "Production model - release $($model.production_order)"
            if ($model.publication_status -ne 'production') { $label = "$($model.publication_status) model - release $($model.production_order)" }
            if ($model.package_id -eq $current) { $label += $(if ($script:existing) {' (current)'} else {' (recommended)'}) }
            $index = $script:modelBox.Items.Add($label)
            if ($model.package_id -eq $current) { $script:modelBox.SelectedIndex = $index }
        }
        $script:settingsStatus.Text = if ($script:existing) { 'Found and read your saved settings. Existing history will be preserved.' } else { 'No saved settings found here. This is a new setup.' }
        $script:dataDescription.Text = if ($script:existing) { 'Existing history stays in this folder. Setup does not move or reset it.' } else { 'Captured runs and application logs will be saved here, separately from the application.' }
        $script:loaded = $true; $script:status.Text = 'Next: choose the CK3 folders to read.'
    }
}
function Update-SettingsLocation {
    if ($script:busy) { return }
    $folder = $script:settingsEntry.Text.Trim()
    if ($folder -notmatch '^(?:[A-Za-z]:\\|\\\\[^\\]+\\[^\\]+)') {
        $script:loaded = $false; $script:settingsStatus.Text = 'Choose a full settings folder path.'; Update-Buttons; return
    }
    $filename = if ($script:configPath) { Split-Path -Leaf $script:configPath } else { 'paths.toml' }
    $selected = Join-Path ([IO.Path]::GetFullPath($folder)) $filename
    if ($selected -ne $script:configPath -or -not $script:loaded) { $script:configPath = $selected; Load-Settings }
}
function Get-Inputs {
    $inputs = @{}
    foreach ($key in $script:fields.Keys) { $inputs[$key] = $script:fields[$key].Entry.Text.Trim() }
    $inputs.data_root = $script:dataEntry.Text.Trim()
    if ($script:modelBox.SelectedIndex -ge 0) { $inputs.package_id = $script:models[$script:modelBox.SelectedIndex].package_id }
    if ($script:databaseOverride) { $inputs.database = $script:databaseOverride }
    return $inputs
}
function Check-Paths([bool]$Advance = $false) {
    $script:pathInputs = Get-Inputs
    $script:advanceAfterPaths = $Advance
    Start-Backend @{operation='paths';config=$script:configPath;inputs=$script:pathInputs} 'Checking your CK3 folders...' {
        param($value)
        $script:details = $value
        foreach ($key in $script:fields.Keys) {
            $field = $script:fields[$key]
            $field.Status.Text = Get-PathMessage $value.findings $key
            if ($field.CheckedPath -ne $script:pathInputs[$key] -or $field.Changed) {
                $field.Accept.Checked = Test-PathReady $value.findings $key
            }
            $field.CheckedPath = $script:pathInputs[$key]; $field.Changed = $false
        }
        if (@($value.findings | Where-Object severity -eq 'error').Count) { $script:status.Text = 'A required folder needs attention. Review the messages above.' }
        elseif ($script:advanceAfterPaths) {
            if (@($script:fields.Values | Where-Object { -not $_.Accept.Checked }).Count) { Show-UnselectedFolder }
            else { Show-Page 2 }
        }
        else { $script:status.Text = 'Checks complete. Folders that passed are selected. Click Next to continue.' }
    }
}
function Show-Review($Value) {
    $page = $script:pages[3]; $page.Controls.Clear()
    [void](Add-Label $page 'Settings folder' $true); [void](Add-Label $page (Split-Path -Parent $script:configPath))
    [void](Add-Label $page 'Saved runs and application logs' $true); [void](Add-Label $page $script:dataEntry.Text)
    [void](Add-Label $page 'Processing model' $true); [void](Add-Label $page $script:modelBox.Text)
    [void](Add-Label $page 'Folders CK3Chronicle will read' $true)
    foreach ($field in $script:fields.Values) { [void](Add-Label $page ($field.Label + ': ' + $field.Entry.Text)) }
    $problems = @($Value.findings | Where-Object { $_.severity -ne 'healthy' -and $_.check -notin @('root_wip','root_ck3chronicle','root_learner_state') })
    foreach ($item in $problems) { [void](Add-Label $page ($item.impact + ' ' + $item.action)) }
    if (-not $problems.Count) { [void](Add-Label $page 'No blocking problems found.') }
    [void](Add-Label $page 'Saving settings also checks that CK3Chronicle can write to the data folders.')
    if ($script:existing) { [void](Add-Label $page 'If a watcher uses these same settings, stop it before saving changes. A separate setup is unaffected.') }
}
function Next-Page {
    if ($script:busy -or -not $script:loaded) { return }
    switch ($script:pageIndex) {
        0 { Update-SettingsLocation; if ($script:loaded -and -not $script:busy) { Show-Page 1 } }
        1 {
            Check-Paths $true
        }
        2 {
            $inputs = Get-Inputs
            if ($inputs.data_root -notmatch '^(?:[A-Za-z]:\\|\\\\[^\\]+\\[^\\]+)' -or -not $inputs.package_id) {
                $script:status.Text = 'Choose a full data folder path and a displayed model.'; return
            }
            $script:readyRequest = @{operation='preview';config=$script:configPath;inputs=$inputs;accepted=@($script:fields.Keys)}
            Start-Backend $script:readyRequest 'Reviewing settings and authenticating the selected model...' {
                param($value)
                $script:details = $value
                if (@($value.findings | Where-Object severity -eq 'error').Count) {
                    $script:readyRequest = $null
                    $script:status.Text = 'Setup needs attention. Open Details for the application findings.'
                } else { Show-Review $value; $script:status.Text = 'Ready to apply. No changes have been made yet.'; Show-Page 3 }
            }
        }
        3 {
            if (-not $script:readyRequest) { return }
            $script:readyRequest.operation = 'apply'
            Start-Backend $script:readyRequest 'Applying settings and testing data-folder write access...' {
                param($value)
                $script:details = $value
                if (-not $value.applied -or $value.exit_code) {
                    $script:readyRequest = $null
                    $script:status.Text = 'Setup did not finish. Preserve the effects and database path in Details before retrying.'
                } else {
                    $script:finished = $true; $script:exitCode = 0
                    $script:finishSettings.Text = $script:configPath; $script:finishDatabase.Text = $value.database
                    $script:commands.Text = '& "' + (Join-Path $script:bundle 'Start.cmd') + '" --config "' + $script:configPath + '"' + "`r`n`r`n" +
                        '& "' + (Join-Path $script:bundle 'ck3chronicle.cmd') + '" --config "' + $script:configPath + '" runtime-stop'
                    $script:status.Text = 'Setup completed successfully.'; Show-Page 4
                }
            }
        }
        4 { $script:form.Close() }
    }
}

[void](Add-Label $pages[0] 'Application location' $true)
[void](Add-Label $pages[0] $script:bundle)
[void](Add-Label $pages[0] 'This is the folder from which you opened Setup. It contains the application and bundled runtime.')
[void](Add-Label $pages[0] 'Settings folder' $true)
if ($script:fixedSettings) {
    $script:settingsEntry = Add-Label $pages[0] ''
    [void](Add-Label $pages[0] 'The installer selected this separate settings folder for this copy.')
} else {
    $script:settingsEntry = Add-Folder $pages[0] ''
    $settingsEntry.add_Leave({ Update-SettingsLocation })
}
$script:settingsStatus = Add-Label $pages[0] 'Checking whether saved settings exist...'
[void](Add-Label $pages[0] 'Next you will choose your CK3 folders and processing model. On step 4, review your choices and save settings.')
$names = [ordered]@{root_game='CK3 game content';root_steam='Steam Workshop mods';root_local_mods='Local CK3 mods';root_logs='CK3 live logs';root_crashes='CK3 crash reports'}
foreach ($key in $names.Keys) {
    [void](Add-Label $pages[1] $names[$key] $true)
    $entry = Add-Folder $pages[1] ''; $entry.Tag = $key
    $finding = Add-Label $pages[1] 'Not checked yet.'
    $accept = New-Object Windows.Forms.CheckBox
    $accept.Text = 'Use this folder'; $accept.AutoSize = $true; $accept.Tag = $key
    $accept.Margin = New-Object Windows.Forms.Padding(0, 0, 0, 8)
    $pages[1].Controls.Add($accept)
    $script:fields[$key] = @{Label=$names[$key];Entry=$entry;Status=$finding;Accept=$accept;CheckedPath=$null;Changed=$false}
    $entry.add_TextChanged({
        param($sender, $eventArgs)
        $field = $script:fields[$sender.Tag]
        $field.Accept.Checked = $false; $field.Changed = $true
        $field.Status.Text = 'Location changed. Next will check this folder before continuing.'
        $script:readyRequest = $null
    })
    $accept.add_Click({
        param($sender, $eventArgs)
        $field = $script:fields[$sender.Tag]
        if ($field.CheckedPath -ne $field.Entry.Text.Trim() -or $field.Changed) {
            $sender.Checked = $false; Check-Paths
        }
    })
}
$checkButton = New-Object Windows.Forms.Button
$checkButton.Text = 'Check folders'; $checkButton.AutoSize = $true; $checkButton.add_Click({ Check-Paths })
$pages[1].Controls.Add($checkButton)
[void](Add-Label $pages[2] 'Saved runs and application logs' $true)
if ($script:fixedData) {
    $script:dataEntry = Add-Label $pages[2] ''
    [void](Add-Label $pages[2] 'The installer selected this separate data folder for this copy.')
} else {
    $script:dataEntry = Add-Folder $pages[2] ''
}
$script:dataDescription = Add-Label $pages[2] ''
[void](Add-Label $pages[2] 'Processing model' $true)
$script:modelBox = New-Object Windows.Forms.ComboBox
$modelBox.DropDownStyle = 'DropDownList'; $modelBox.Width = 800
$pages[2].Controls.Add($modelBox)
[void](Add-Label $pages[2] 'The current or recommended model is selected. New processing uses this model; stored runs keep their original model history.')
[void](Add-Label $pages[4] 'Settings saved to' $true)
$script:finishSettings = Add-Label $pages[4] ''
[void](Add-Label $pages[4] 'Run history' $true)
$script:finishDatabase = Add-Label $pages[4] ''
[void](Add-Label $pages[4] 'Open Start.cmd to run the watcher. Stop it with Ctrl+C in its window.')
[void](Add-Label $pages[4] 'Commands for this setup (select and copy)' $true)
$script:commands = New-Object Windows.Forms.TextBox
$commands.Multiline = $true; $commands.ReadOnly = $true; $commands.ScrollBars = 'Vertical'
$commands.Size = New-Object Drawing.Size(800, 125); $pages[4].Controls.Add($commands)
$doctor = New-Object Windows.Forms.Button
$doctor.Text = 'Check saved settings...'; $doctor.AutoSize = $true
$doctor.add_Click({
    Start-Backend @{operation='doctor';config=$script:configPath} 'Checking saved settings...' {
        param($value)
        $script:details = $value
        $script:status.Text = 'Saved settings checked. Read-only diagnosis does not repeat Apply''s write tests. See Details.'
    }
})
$pages[4].Controls.Add($doctor)
$back.add_Click({ $script:readyRequest = $null; Show-Page ($script:pageIndex - 1) })
$next.add_Click({ Next-Page })
$cancel.add_Click({ $script:form.Close() })
$detailButton.add_Click({ Show-Details })
$form.add_FormClosing({ param($sender,$eventArgs) if ($script:busy) { $eventArgs.Cancel = $true } })
$form.add_Resize({
    $width = [Math]::Max(620, $script:form.ClientSize.Width - 76)
    foreach ($page in $script:pages) {
        foreach ($control in $page.Controls) {
            if ($control -is [Windows.Forms.Label]) { $control.MaximumSize = New-Object Drawing.Size($width, 0) }
            elseif ($control -is [Windows.Forms.Panel] -or $control -is [Windows.Forms.TextBox] -or $control -is [Windows.Forms.ComboBox]) { $control.Width = $width }
        }
    }
    $script:subtitle.Width = $script:form.ClientSize.Width - 52
})
Show-Page 0
if ($MyInvocation.InvocationName -ne '.') {
    $form.add_Shown({ Load-Settings })
    try { [void]$form.ShowDialog(); exit $script:exitCode }
    finally { $timer.Dispose(); $form.Dispose() }
}
