param(
    [string]$PdfPath = "",
    [int]$IntervalMinutes = 10
)

$root = Split-Path -Parent $PSScriptRoot

while ($true) {
    python "$root\scripts\run_cycle.py" --pdf "$PdfPath" --send-telegram --commit-push
    Start-Sleep -Seconds ($IntervalMinutes * 60)
}
