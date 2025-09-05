# 🔧 Detectron2 Setup Guide for Phishpedia

## 📋 Overview
This guide provides detailed instructions for setting up Detectron2 with Phishpedia, including troubleshooting common issues encountered during installation.

## 🚨 Common Issues & Solutions

### Issue 1: `ModuleNotFoundError: No module named 'detectron2'`
**Cause:** Detectron2 is not installed in the virtual environment.

### Issue 2: Virtual Environment Activation Problems
**Cause:** `call activate` doesn't work properly in all Windows environments.

### Issue 3: PyTorch Missing During Detectron2 Build
**Cause:** PyTorch must be installed before Detectron2.

## 🛠️ Step-by-Step Setup

### Prerequisites
- **Python 3.8+** installed
- **Git** for version control
- **Windows** with Command Prompt
- **Internet connection** for downloading models

### Step 1: Create Virtual Environment
```bat
cd "D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\clone-detection\phishpedia+detectron2\Phishpedia"
python -m venv phishpedia_env
```

### Step 2: Install Dependencies Using Direct Python Path
**❌ Wrong way (activation issues):**
```bat
call phishpedia_env\Scripts\activate
pip install torch
```

**✅ Correct way (direct path):**
```bat
phishpedia_env\Scripts\python.exe -m pip install torch torchvision
phishpedia_env\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 3: Install Detectron2 from Local Directory
**❌ Wrong way (downloads from GitHub):**
```bat
pip install git+https://github.com/facebookresearch/detectron2.git
```

**✅ Correct way (uses local copy):**
```bat
phishpedia_env\Scripts\python.exe -m pip install --no-build-isolation -e ..\detectron2
```

### Step 4: Run Automated Setup
```bat
setup.bat
```

This script will:
1. ✅ Check virtual environment exists
2. ✅ Install PyTorch and dependencies
3. ✅ Install local Detectron2
4. ✅ Download required model files
5. ✅ Test all imports
6. ✅ Prepare for service startup

## 🧪 Testing Installation

### Test 1: Check Python Environment
```bat
phishpedia_env\Scripts\python.exe -c "import sys; print('Python:', sys.executable)"
```
**Expected Output:**
```
Python: D:\volume E\ciphercop-2025\overall\ciphercopdemo\backend_py\clone-detection\phishpedia+detectron2\Phishpedia\phishpedia_env\Scripts\python.exe
```

### Test 2: Check PyTorch
```bat
phishpedia_env\Scripts\python.exe -c "import torch; print('PyTorch:', torch.__version__)"
```
**Expected Output:**
```
PyTorch: 2.8.0
```

### Test 3: Check Detectron2
```bat
phishpedia_env\Scripts\python.exe -c "import detectron2; print('Detectron2: OK')"
```
**Expected Output:**
```
Detectron2: OK
```

### Test 4: Check Phishpedia
```bat
phishpedia_env\Scripts\python.exe -c "from phishpedia import PhishpediaWrapper; print('Phishpedia: OK')"
```
**Expected Output:**
```
Phishpedia: OK
```

## 🗂️ File Structure After Setup
```
phishpedia+detectron2/
├── Phishpedia/
│   ├── phishpedia_env/          # Virtual environment
│   │   └── Scripts/
│   │       └── python.exe       # Direct Python executable
│   ├── models/                  # Downloaded model files
│   │   ├── rcnn_bet365.pth
│   │   ├── faster_rcnn.yaml
│   │   ├── resnetv2_rgb_new.pth.tar
│   │   ├── domain_map.pkl
│   │   └── expand_targetlist/
│   ├── WEBtool/
│   │   └── app.py              # Web service entry point
│   ├── setup.bat               # Fixed setup script
│   └── requirements.txt
└── detectron2/                 # Local Detectron2 source
    ├── setup.py
    ├── detectron2/
    └── configs/
```

## 🚀 Running Services

### Option 1: Direct Command
```bat
cd WEBtool
..\phishpedia_env\Scripts\python.exe app.py
```

### Option 2: Using Service Manager
```bat
cd ..
manage-services.bat
```
Choose option 5 to start ML service only.

## 🔍 Troubleshooting

### Problem: "torch not found" during detectron2 installation
**Solution:**
```bat
# Install PyTorch first
phishpedia_env\Scripts\python.exe -m pip install torch torchvision

# Then install detectron2
phishpedia_env\Scripts\python.exe -m pip install --no-build-isolation -e ..\detectron2
```

### Problem: Virtual environment activation fails
**Solution:** Don't use activation! Use direct paths:
```bat
# Instead of this:
call phishpedia_env\Scripts\activate
python app.py

# Use this:
phishpedia_env\Scripts\python.exe app.py
```

### Problem: Model files missing
**Solution:**
```bat
# Re-run setup to download models
setup.bat

# Or manually download with gdown:
phishpedia_env\Scripts\python.exe -m pip install gdown
cd models
..\phishpedia_env\Scripts\python.exe -m gdown --id 1tE2Mu5WC8uqCxei3XqAd7AWaP5JTmVWH -O rcnn_bet365.pth
```

### Problem: Import errors at runtime
**Solution:**
```bat
# Check all dependencies
phishpedia_env\Scripts\python.exe -m pip list | findstr torch
phishpedia_env\Scripts\python.exe -m pip list | findstr detectron2

# Reinstall if needed
phishpedia_env\Scripts\python.exe -m pip uninstall detectron2
phishpedia_env\Scripts\python.exe -m pip install --no-build-isolation -e ..\detectron2
```

## 📝 Setup Script Details

The `setup.bat` script performs these operations in order:

1. **Environment Check:** Verifies `phishpedia_env` exists
2. **Tool Installation:** Installs `gdown` for model downloads
3. **Dependencies:** Installs requirements.txt and PyTorch
4. **Detectron2:** Installs from local directory with `--no-build-isolation`
5. **Testing:** Validates all imports work
6. **Models:** Downloads 5 required model files from Google Drive
7. **Extraction:** Unzips and organizes model files
8. **Final Test:** Confirms Phishpedia can be imported

## ⚡ Quick Commands Reference

```bat
# Full setup from scratch
python -m venv phishpedia_env
setup.bat

# Test installation
phishpedia_env\Scripts\python.exe -c "from phishpedia import PhishpediaWrapper; print('OK')"

# Start web service
phishpedia_env\Scripts\python.exe WEBtool\app.py

# Check service status
netstat -an | findstr ":5000"

# Stop service (Ctrl+C in service window)
```

## 🎯 Why This Approach Works

1. **Direct Python Paths:** Avoids Windows activation issues
2. **Local Detectron2:** Uses included source instead of downloading
3. **Proper Dependencies:** Installs PyTorch before Detectron2
4. **No Build Isolation:** Allows access to pre-installed PyTorch
5. **Comprehensive Testing:** Validates each step

## 🔄 Updates and Maintenance

### Updating Detectron2
```bat
cd ..\detectron2
git pull origin main
cd ..\Phishpedia
phishpedia_env\Scripts\python.exe -m pip install --no-build-isolation -e ..\detectron2 --force-reinstall
```

### Updating Dependencies
```bat
phishpedia_env\Scripts\python.exe -m pip install --upgrade -r requirements.txt
```

### Clean Reinstall
```bat
rmdir /s phishpedia_env
rmdir /s models
setup.bat
```

---

## 📞 Support

If you encounter issues:

1. **Check this guide first** - most problems are covered here
2. **Run the test commands** to identify the specific failure point
3. **Use direct Python paths** instead of environment activation
4. **Verify PyTorch is installed** before installing Detectron2

**Remember:** The key insight is to use direct Python executable paths rather than relying on environment activation, which can be unreliable on Windows systems.
