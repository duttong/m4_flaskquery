# Conda initialization
& 'C:\ProgramData\anaconda3\shell\condabin\conda-hook.ps1'

# Activate the 'flaskq' environment
conda activate flaskq
if ($env:CONDA_DEFAULT_ENV -ne 'flaskq') {
    Write-Host "ERROR: could not activate conda environment 'flaskq'." -ForegroundColor Red
    Read-Host "Press Enter to close"
    exit 1
}

# Run from the folder this script lives in, wherever it was copied
Set-Location -Path $PSScriptRoot

# Run your Python script
python .\flaskquery.py

# Keep the window open if Python failed so the error can be read
if ($LASTEXITCODE -ne 0) {
    Write-Host "`nflaskquery.py exited with code $LASTEXITCODE" -ForegroundColor Red
    Read-Host "Press Enter to close"
}
