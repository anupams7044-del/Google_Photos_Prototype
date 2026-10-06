$ErrorActionPreference = "Stop"
cd "c:\NextLeap Projects\Sri Ganesh\MVP\src"

Write-Host "1/4 Checking sample photos..."
if (!(Test-Path -Path "phase1\sample_photos")) {
    New-Item -ItemType Directory -Path "phase1\sample_photos" | Out-Null
}

if ((Get-ChildItem -Path "phase1\sample_photos" -Filter *.jpg | Measure-Object).Count -lt 4) {
    Write-Host "Downloading sample images..."
    Invoke-WebRequest -Uri "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=300&q=80" -OutFile "phase1\sample_photos\beach.jpg"
    Invoke-WebRequest -Uri "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=300&q=80" -OutFile "phase1\sample_photos\mountain.jpg"
    Invoke-WebRequest -Uri "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=300&q=80" -OutFile "phase1\sample_photos\city.jpg"
    Invoke-WebRequest -Uri "https://images.unsplash.com/photo-1511895426328-dc8714191300?w=300&q=80" -OutFile "phase1\sample_photos\dinner.jpg"
    Invoke-WebRequest -Uri "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=300&q=80" -OutFile "phase1\sample_photos\lake.jpg"
}

Write-Host "2/4 Installing requirements..."
pip install -r requirements.txt

Write-Host "3/4 Running data ingestion pipeline (Setting up local DB)..."
python phase1\ingestion_pipeline.py

Write-Host "4/4 Starting the web server..."
python app_server.py
