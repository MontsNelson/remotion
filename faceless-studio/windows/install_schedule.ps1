# Registers the daily run in Windows Task Scheduler.
#   powershell -ExecutionPolicy Bypass -File windows\install_schedule.ps1 -Time 07:00
# Check it:   schtasks /query /tn "Faceless Studio daily run" /v /fo list
# Run now:    schtasks /run /tn "Faceless Studio daily run"
# Turn off:   schtasks /change /tn "Faceless Studio daily run" /disable
# Turn on:    schtasks /change /tn "Faceless Studio daily run" /enable
param([string]$Time = "07:00")
$root = Split-Path -Parent $PSScriptRoot
$bat = Join-Path $root "windows\run_daily.bat"
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$bat`"" -WorkingDirectory $root
$trigger = New-ScheduledTaskTrigger -Daily -At $Time
# StartWhenAvailable = run as soon as possible after a missed start (PC was off or asleep)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 3)
Register-ScheduledTask -TaskName "Faceless Studio daily run" -Action $action -Trigger $trigger `
    -Settings $settings -Description "Makes the day's Vice City Corner and Footy Smart posts into Google Drive." -Force
Write-Host "Scheduled every day at $Time. Next run:"
(Get-ScheduledTask -TaskName "Faceless Studio daily run" | Get-ScheduledTaskInfo).NextRunTime
