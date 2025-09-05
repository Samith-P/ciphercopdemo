#!/bin/bash
# Git-Crypt Setup Script for CipherCop 2025
# This script initializes git-crypt for protecting sensitive environment files

echo "🔐 Git-Crypt Setup for CipherCop 2025"
echo "======================================"

# Check if git-crypt is installed
if ! command -v git-crypt &> /dev/null; then
    echo "❌ git-crypt is not installed!"
    echo ""
    echo "📥 Install git-crypt:"
    echo "   Windows: choco install git-crypt"
    echo "   macOS:   brew install git-crypt"
    echo "   Ubuntu:  sudo apt-get install git-crypt"
    echo ""
    exit 1
fi

echo "✅ git-crypt is installed"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository!"
    echo "Please run this script from the project root directory."
    exit 1
fi

echo "✅ In git repository"

# Initialize git-crypt
echo ""
echo "🔧 Initializing git-crypt..."
git-crypt init

if [ $? -eq 0 ]; then
    echo "✅ git-crypt initialized successfully"
else
    echo "❌ Failed to initialize git-crypt"
    exit 1
fi

# Generate a key for the project
echo ""
echo "🔑 Generating git-crypt key..."
git-crypt export-key ciphercop-git-crypt.key

if [ $? -eq 0 ]; then
    echo "✅ Key exported to: ciphercop-git-crypt.key"
    echo "⚠️  IMPORTANT: Keep this key file safe and secure!"
    echo "   - Share it securely with authorized team members"
    echo "   - Do NOT commit this key to the repository"
else
    echo "❌ Failed to export key"
    exit 1
fi

# Show status of encrypted files
echo ""
echo "📊 Encrypted file status:"
git-crypt status

echo ""
echo "🎉 Git-crypt setup completed!"
echo ""
echo "📋 Next steps:"
echo "   1. Add and commit the .gitattributes file"
echo "   2. Add and commit your .env files (they will be encrypted)"
echo "   3. Share ciphercop-git-crypt.key securely with team members"
echo ""
echo "🔓 To unlock files on a new machine:"
echo "   git-crypt unlock ciphercop-git-crypt.key"
echo ""
echo "🔒 To lock files (optional):"
echo "   git-crypt lock"
