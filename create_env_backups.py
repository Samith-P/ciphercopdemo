#!/usr/bin/env python3
"""
Environment File Backup Generator
This script reads all .env files in the CipherCop project and creates env.txt backups
in their respective directories.
"""

import os
import shutil
from pathlib import Path

def create_env_txt_files():
    """
    Create env.txt files from .env files in all project directories
    """
    # Base directory of the project (script is in project root)
    base_dir = Path(__file__).parent
    
    # List of .env file locations relative to the project root
    env_files = [
        "backend/.env",
        "backend_py/clone-detection/combined-analysis/.env", 
        "backend_py/clone-detection/gemini/.env",
        "backend_py/phishing-detection/.env"
    ]
    
    print("🔄 Creating env.txt files from .env files...")
    print("=" * 50)
    
    created_files = []
    failed_files = []
    
    for env_path in env_files:
        # Construct full paths
        source_file = base_dir / env_path
        target_file = source_file.parent / "env.txt"
        
        try:
            if source_file.exists():
                # Copy .env content to env.txt
                shutil.copy2(source_file, target_file)
                
                print(f"✅ Created: {target_file}")
                created_files.append(str(target_file))
                
                # Also print the content for verification
                print(f"📄 Content preview of {env_path}:")
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    lines = content.split('\n')
                    for line in lines[:5]:  # Show first 5 lines
                        if line.strip() and not line.startswith('#'):
                            # Mask sensitive values
                            if '=' in line:
                                key, value = line.split('=', 1)
                                if any(sensitive in key.upper() for sensitive in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
                                    print(f"   {key}=***MASKED***")
                                else:
                                    print(f"   {line}")
                            else:
                                print(f"   {line}")
                        else:
                            print(f"   {line}")
                    if len(lines) > 5:
                        print(f"   ... and {len(lines) - 5} more lines")
                print()
                
            else:
                print(f"❌ Source file not found: {source_file}")
                failed_files.append(str(source_file))
                
        except Exception as e:
            print(f"❌ Error processing {env_path}: {str(e)}")
            failed_files.append(str(source_file))
    
    print("=" * 50)
    print(f"📊 Summary:")
    print(f"   ✅ Successfully created: {len(created_files)} files")
    print(f"   ❌ Failed: {len(failed_files)} files")
    
    if created_files:
        print(f"\n📁 Created files:")
        for file in created_files:
            print(f"   • {file}")
    
    if failed_files:
        print(f"\n❌ Failed files:")
        for file in failed_files:
            print(f"   • {file}")
    
    return len(created_files), len(failed_files)

def main():
    """Main execution function"""
    print("🚀 Environment File Backup Generator")
    print("📍 Project: CipherCop 2025")
    print("🎯 Purpose: Create env.txt backups from .env files")
    print()
    
    try:
        created, failed = create_env_txt_files()
        
        if failed == 0:
            print("\n🎉 All environment files backed up successfully!")
        else:
            print(f"\n⚠️  Completed with {failed} errors. Check the output above.")
            
    except Exception as e:
        print(f"\n💥 Script failed with error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
