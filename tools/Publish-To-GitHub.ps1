# Upload the source repository using the user's own Git installation/authentication.
# No force pushes, passwords, or tokens are stored by this script.
$ErrorActionPreference = 'Stop'
$RepoUrl = 'https://github.com/VexenDeimos/Starfield-Creations-PS5-Glyph-Fix.git'
$RepoRoot = Split-Path -Parent $PSScriptRoot
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git for Windows is required. Install Git and restart PowerShell.'
}

function Invoke-Git {
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Arguments)
    & git @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Git command failed (exit $LASTEXITCODE): git $($Arguments -join ' ')" }
}

Push-Location -LiteralPath $RepoRoot
try {
    if (-not (Test-Path -LiteralPath '.git')) {
        Invoke-Git init
    }
    Invoke-Git branch -M main

    # A newly initialized repository has no origin. Check the list first instead
    # of running `git remote get-url origin`, whose stderr can terminate PS 5.1.
    $Remotes = @(& git remote)
    if ($LASTEXITCODE -ne 0) { throw 'Could not list Git remotes.' }
    if ($Remotes -contains 'origin') {
        $oldOrigin = & git remote get-url origin
        if ($LASTEXITCODE -ne 0) { throw 'Could not read existing origin URL.' }
        if ($oldOrigin.Trim() -ne $RepoUrl) {
            throw "Existing 'origin' points to $oldOrigin and was not changed."
        }
    } else {
        Invoke-Git remote add origin $RepoUrl
    }

    # Build output and game-font assets are excluded by .gitignore.
    Invoke-Git add --all
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 1) {
        Invoke-Git commit -m 'Initial standalone PS5 glyph fix source and documentation'
    } elseif ($LASTEXITCODE -ne 0) {
        throw 'Could not check staged Git changes.'
    } else {
        Write-Host 'No new changes to commit.'
    }

    Write-Host "Pushing main to $RepoUrl ..."
    Invoke-Git push -u origin main
    Write-Host 'Push completed. Open https://github.com/VexenDeimos/Starfield-Creations-PS5-Glyph-Fix'
} finally {
    Pop-Location
}
