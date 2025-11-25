## Ensure Poetry uses a compatible Python version (Windows)
param(
    [string]$pyInterpreter = "C:\\Users\\Rezwana Binte Reza\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
)

Write-Host "Switching poetry env to $pyInterpreter"
poetry env use "$pyInterpreter"
if ($LASTEXITCODE -ne 0) { Write-Error "poetry env use failed"; exit 1 }

Write-Host "Running poetry lock and install"
poetry lock
poetry install
if ($LASTEXITCODE -ne 0) { Write-Error "poetry install failed"; exit 2 }

Write-Host "Done. Run: cd src; poetry run python manage.py makemigrations && poetry run python manage.py migrate"
