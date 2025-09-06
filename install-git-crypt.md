# 📥 Git-Crypt Installation Guide for Windows

## Option 1: Download Pre-built Binary (Recommended)

### Step 1: Download git-crypt
1. Go to: https://github.com/AGWA/git-crypt/releases/latest
2. Download `git-crypt-X.X.X-windows.zip` (where X.X.X is the version)
3. Or use this direct link to latest: https://github.com/AGWA/git-crypt/releases

### Step 2: Install git-crypt
1. **Extract the ZIP file** to a folder (e.g., `C:\git-crypt\`)
2. **Add to PATH**:
   - Open "Environment Variables" (Search "env" in Start Menu)
   - Click "Environment Variables..." button
   - Under "System Variables", find and select "Path"
   - Click "Edit..." then "New"
   - Add the path where you extracted git-crypt (e.g., `C:\git-crypt\`)
   - Click "OK" to save
3. **Restart your command prompt**
4. **Test installation**: Run `git-crypt --version`

## Option 2: Using Chocolatey Package Manager

### Install Chocolatey first (if not installed):
```powershell
# Run as Administrator in PowerShell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```

### Then install git-crypt:
```cmd
choco install git-crypt
```

## Option 3: Using Windows Subsystem for Linux (WSL)

If you have WSL installed:
```bash
sudo apt-get update
sudo apt-get install git-crypt
```

## Option 4: Manual Compilation (Advanced Users)

### Prerequisites:
- Visual Studio Build Tools or Visual Studio Community
- Git for Windows

### Steps:
```cmd
git clone https://github.com/AGWA/git-crypt.git
cd git-crypt
make
```

## 🧪 Test Installation

After installation, test with:
```cmd
git-crypt --version
```

You should see output like:
```
git-crypt 0.7.0
```

## ✅ Once Installed

Run the setup script:
```cmd
setup-git-crypt.bat
```

## 🚨 Troubleshooting

### "git-crypt is not recognized..."
- Make sure you added git-crypt to your PATH
- Restart your command prompt after modifying PATH
- Try using the full path to git-crypt.exe

### Permission Denied
- Make sure you have write permissions in the project directory
- Try running command prompt as Administrator

### Build Errors (if compiling)
- Ensure you have Visual Studio Build Tools installed
- Make sure all dependencies are available

---

## 📋 Quick Installation Summary

**Fastest method for most users:**
1. Download: https://github.com/AGWA/git-crypt/releases/latest
2. Extract to `C:\git-crypt\`
3. Add `C:\git-crypt\` to PATH
4. Restart command prompt
5. Run `git-crypt --version` to verify
6. Run `setup-git-crypt.bat` to configure project
