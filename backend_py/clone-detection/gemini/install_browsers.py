#!/usr/bin/env python3
"""
Script to install Playwright browsers
"""
import subprocess
import sys

def install_playwright_browsers():
    """Install Playwright browsers with certificate bypass"""
    try:
        print("Installing Playwright browsers (bypassing certificate verification)...")
        
        # Set environment variable to bypass certificate verification
        import os
        env = os.environ.copy()
        env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'
        
        result = subprocess.run([
            sys.executable, "-m", "playwright", "install", "chromium"
        ], capture_output=True, text=True, env=env)
        
        if result.returncode == 0:
            print("✅ Playwright browsers installed successfully!")
            print(result.stdout)
        else:
            print("❌ Failed to install Playwright browsers:")
            print(result.stderr)
            print("\n💡 Alternative: Try using system Chrome instead")
            
    except Exception as e:
        print(f"❌ Error installing browsers: {e}")
        print("\n💡 Alternative: The service will try to use system Chrome")

if __name__ == "__main__":
    install_playwright_browsers()