# Shows a Windows notification. Used by: python make.py notify "message"
param([string]$Title = "Faceless Studio", [string]$Message = "Done")
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$safeTitle = [System.Security.SecurityElement]::Escape($Title)
$safeMessage = [System.Security.SecurityElement]::Escape($Message)
$xml.LoadXml("<toast><visual><binding template='ToastGeneric'><text>$safeTitle</text><text>$safeMessage</text></binding></visual></toast>")
$toast = New-Object Windows.UI.Notifications.ToastNotification $xml
# PowerShell's own app id, so no extra install is needed
$appId = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($appId).Show($toast)
