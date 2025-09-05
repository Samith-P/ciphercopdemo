# 🔐 Environment File Security Setup

## 📋 Overview
This directory contains tools for managing and securing environment files in the CipherCop 2025 project.

## 🛠️ Tools Provided

### 1. **create_env_backups.py** - Environment File Backup Generator
Creates `env.txt` backup files from all `.env` files in the project.

**Usage:**
```bash
python create_env_backups.py
```

**What it does:**
- Reads all 4 `.env` files in the project
- Creates corresponding `env.txt` files in the same directories
- Shows content preview (with sensitive values masked)
- Provides summary of success/failure

**Locations processed:**
- `backend/.env` → `backend/env.txt`
- `backend_py/clone-detection/combined-analysis/.env` → `backend_py/clone-detection/combined-analysis/env.txt`
- `backend_py/clone-detection/gemini/.env` → `backend_py/clone-detection/gemini/env.txt`
- `backend_py/phishing-detection/.env` → `backend_py/phishing-detection/env.txt`

### 2. **Git-Crypt Integration** - Environment File Encryption
Encrypts `.env` files in the git repository for secure collaboration.

## 🔒 Git-Crypt Setup

### Prerequisites
Install git-crypt on your system:

**Windows:**
```bash
choco install git-crypt
```

**macOS:**
```bash
brew install git-crypt
```

**Ubuntu/Debian:**
```bash
sudo apt-get install git-crypt
```

### Setup Process

#### Option 1: Windows (Batch Script)
```bash
setup-git-crypt.bat
```

#### Option 2: Linux/macOS (Shell Script)
```bash
chmod +x setup-git-crypt.sh
./setup-git-crypt.sh
```

#### Option 3: Manual Setup
```bash
# Initialize git-crypt
git-crypt init

# Export the encryption key
git-crypt export-key ciphercop-git-crypt.key

# Check status
git-crypt status
```

### What Gets Encrypted
The `.gitattributes` file specifies these files for encryption:
- `backend/.env`
- `backend_py/clone-detection/combined-analysis/.env`
- `backend_py/clone-detection/gemini/.env`
- `backend_py/phishing-detection/.env`

## 🔄 Workflow

### For New Team Members
1. **Clone the repository**
2. **Unlock encrypted files:**
   ```bash
   git-crypt unlock ciphercop-git-crypt.key
   ```
3. **Create your own .env files** from .env.example templates
4. **Run the backup script** if needed:
   ```bash
   python create_env_backups.py
   ```

### For Existing Team Members
1. **Make changes to .env files** as needed
2. **Create backups:**
   ```bash
   python create_env_backups.py
   ```
3. **Commit changes** (files will be automatically encrypted):
   ```bash
   git add .
   git commit -m "Update environment configuration"
   ```

### For Repository Maintenance
1. **Lock files** (optional, for extra security):
   ```bash
   git-crypt lock
   ```
2. **Unlock when needed:**
   ```bash
   git-crypt unlock ciphercop-git-crypt.key
   ```

## 📁 File Structure
```
ciphercopdemo/
├── create_env_backups.py          # Backup generator script
├── setup-git-crypt.bat            # Windows git-crypt setup
├── setup-git-crypt.sh             # Linux/macOS git-crypt setup
├── .gitattributes                 # Git-crypt configuration
├── ciphercop-git-crypt.key        # Encryption key (keep secure!)
├── backend/
│   ├── .env                       # 🔒 Encrypted
│   ├── .env.example              # Public template
│   └── env.txt                   # Created by backup script
├── backend_py/
│   ├── clone-detection/
│   │   ├── combined-analysis/
│   │   │   ├── .env              # 🔒 Encrypted
│   │   │   ├── .env.example      # Public template
│   │   │   └── env.txt           # Created by backup script
│   │   └── gemini/
│   │       ├── .env              # 🔒 Encrypted
│   │       ├── .env.example      # Public template
│   │       └── env.txt           # Created by backup script
│   └── phishing-detection/
│       ├── .env                  # 🔒 Encrypted
│       ├── .env.example          # Public template
│       └── env.txt               # Created by backup script
```

## 🔑 Key Management

### Security Best Practices
- **Never commit** `ciphercop-git-crypt.key` to the repository
- **Share the key securely** (encrypted email, secure file sharing)
- **Store backups** of the key in multiple secure locations
- **Rotate keys periodically** for enhanced security

### Key Sharing for Team Members
1. **Encrypt the key file** before sharing
2. **Use secure channels** (ProtonMail, Signal, etc.)
3. **Verify recipient** before sending
4. **Delete temporary copies** after sharing

## 🚨 Troubleshooting

### Problem: "git-crypt: command not found"
**Solution:** Install git-crypt using the commands above

### Problem: "Not in a git repository"
**Solution:** Run scripts from the project root directory

### Problem: Files not encrypting
**Solution:** 
1. Check `.gitattributes` file exists
2. Verify file paths in `.gitattributes`
3. Run `git-crypt status` to check file status

### Problem: Cannot unlock files
**Solution:**
1. Ensure you have the correct key file
2. Check key file permissions
3. Verify git-crypt is properly installed

## 🎯 Usage Examples

### Create all env.txt backups:
```bash
python create_env_backups.py
```

### Setup encryption for the first time:
```bash
# Windows
setup-git-crypt.bat

# Linux/macOS
./setup-git-crypt.sh
```

### Check encryption status:
```bash
git-crypt status
```

### Lock/unlock manually:
```bash
# Lock files
git-crypt lock

# Unlock files
git-crypt unlock ciphercop-git-crypt.key
```

---

## 🛡️ Security Notes

- **Environment files contain sensitive data** (API keys, secrets)
- **git-crypt uses AES-256** for encryption
- **Key file is the single point of access** - protect it carefully
- **Regular backups** of both code and keys are essential
- **Monitor access** to the key file and repository
