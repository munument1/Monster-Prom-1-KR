$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
python (Join-Path $PSScriptRoot 'manage_test_patch.py') restore
if ($LASTEXITCODE -ne 0) { throw 'Test patch restore failed.' }
