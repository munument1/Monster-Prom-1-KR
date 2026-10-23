$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
python (Join-Path $PSScriptRoot 'manage_test_patch.py') apply
if ($LASTEXITCODE -ne 0) { throw 'Test patch apply failed.' }
