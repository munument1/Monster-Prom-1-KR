$ErrorActionPreference = 'Stop'
python (Join-Path $PSScriptRoot 'manage_logo_patch.py') restore
if ($LASTEXITCODE -ne 0) { throw 'Logo restore failed.' }
