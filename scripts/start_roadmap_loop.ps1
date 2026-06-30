param(
    [string]$PdfPath = "",
    [int]$IntervalMinutes = 10
)

$root = Split-Path -Parent $PSScriptRoot
$envPath = Join-Path $root ".env.local"

function Get-EnvValue {
    param([string]$Key)
    if (!(Test-Path $envPath)) { return $null }
    $line = Get-Content $envPath | Where-Object { $_ -match "^$Key=" } | Select-Object -First 1
    if (-not $line) { return $null }
    return ($line -split "=", 2)[1].Trim()
}

function Test-DeepSeekPeakWindow {
    $provider = (Get-EnvValue "AI_TASK_RUNNER_PROVIDER")
    $offPeakOnly = (Get-EnvValue "DEEPSEEK_OFFPEAK_ONLY")
    if ($provider -ne "deepseek") { return $false }
    if ($offPeakOnly -and $offPeakOnly.ToLower() -eq "false") { return $false }

    $hour = (Get-Date).Hour
    return (($hour -ge 4 -and $hour -lt 7) -or ($hour -ge 9 -and $hour -lt 13))
}

while ($true) {
    if (Test-DeepSeekPeakWindow) {
        Write-Output "SKIP_DEEPSEEK_PEAK_WINDOW $(Get-Date -Format s)"
    } else {
        python "$root\scripts\run_cycle.py" --pdf "$PdfPath" --send-telegram --commit-push
    }
    Start-Sleep -Seconds ($IntervalMinutes * 60)
}
