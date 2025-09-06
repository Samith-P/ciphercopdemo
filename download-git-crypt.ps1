# Download Git-Crypt Pre-built Binary for Windows
# This script downloads the latest pre-built git-crypt binary

Write-Host "🔐 Downloading Git-Crypt Pre-built Binary..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Yellow

# Create download directory
$downloadPath = "C:\git-crypt"
if (!(Test-Path $downloadPath)) {
    New-Item -ItemType Directory -Path $downloadPath -Force
    Write-Host "✅ Created directory: $downloadPath" -ForegroundColor Green
}

# Download URL for pre-built binary (you may need to update this URL)
$downloadUrl = "https://github.com/AGWA/git-crypt/releases/download/0.7.0/git-crypt-0.7.0-windows.zip"
$zipPath = "$downloadPath\git-crypt-windows.zip"

try {
    Write-Host "📥 Downloading from: $downloadUrl" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath -UseBasicParsing
    Write-Host "✅ Downloaded to: $zipPath" -ForegroundColor Green
    
    # Extract the ZIP
    Write-Host "📂 Extracting archive..." -ForegroundColor Cyan
    Expand-Archive -Path $zipPath -DestinationPath $downloadPath -Force
    
    # Clean up ZIP file
    Remove-Item $zipPath
    Write-Host "✅ Extraction completed" -ForegroundColor Green
    
    # List extracted files
    Write-Host "📁 Extracted files:" -ForegroundColor Cyan
    Get-ChildItem $downloadPath -Recurse | ForEach-Object { Write-Host "   $($_.FullName)" }
    
} catch {
    Write-Host "❌ Download failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "🔗 Please manually download from: https://github.com/AGWA/git-crypt/releases" -ForegroundColor Yellow
    Write-Host "   Look for git-crypt-X.X.X-windows.zip" -ForegroundColor Yellow
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Add $downloadPath to your PATH environment variable" -ForegroundColor White
Write-Host "2. Restart your command prompt" -ForegroundColor White
Write-Host "3. Test with: git-crypt --version" -ForegroundColor White

Read-Host "`nPress Enter to continue..."
