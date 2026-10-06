$ErrorActionPreference = "Continue"
cd "c:\NextLeap Projects\Sri Ganesh\MVP\src\phase1\sample_photos"

Write-Host "Downloading diverse test photos..."

$urls = @{
    "dog.jpg" = "https://images.unsplash.com/photo-1517849845537-4d257902454a?w=300&q=80"
    "cat.jpg" = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?w=300&q=80"
    "car.jpg" = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=300&q=80"
    "space.jpg" = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=300&q=80"
    "architecture.jpg" = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=300&q=80"
    "pizza.jpg" = "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=300&q=80"
    "abstract.jpg" = "https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=300&q=80"
    "neon.jpg" = "https://images.unsplash.com/photo-1550684848-fac1c5b4e853?w=300&q=80"
    "portrait.jpg" = "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&q=80"
    "forest.jpg" = "https://images.unsplash.com/photo-1448375240586-882707db888b?w=300&q=80"
    "desert.jpg" = "https://images.unsplash.com/photo-1473580044384-7ba9967e16a0?w=300&q=80"
    "concert.jpg" = "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?w=300&q=80"
    "macro.jpg" = "https://images.unsplash.com/photo-1550346363-228ea15a9958?w=300&q=80"
    "winter.jpg" = "https://images.unsplash.com/photo-1483664852095-d6cc6870702d?w=300&q=80"
    "coffee.jpg" = "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?w=300&q=80"
}

foreach ($key in $urls.Keys) {
    if (!(Test-Path $key)) {
        Write-Host "Downloading $key..."
        Invoke-WebRequest -Uri $urls[$key] -OutFile $key
    }
}
Write-Host "Download complete!"
