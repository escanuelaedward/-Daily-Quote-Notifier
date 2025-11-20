# Name of the scheduled task
$taskName = "DailyQuoteNotifier"

# Check if the task exists
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
# If it exists, remove it without asking for confirmation
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Uninstalled task '$taskName'."
}
else {
# If it doesn't exist, just inform the user
    Write-Host "Task '$taskName' not found."
}
