#!/usr/bin/env python3
"""
Script to uninstall all packages listed in requirements.txt from the global Python environment.
This will help clean up a cluttered global Python environment.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors gracefully."""
    print(f"  {description}...")
    try:
        # Use list format to avoid shell issues with special characters
        cmd_parts = command.split()
        result = subprocess.run(cmd_parts, capture_output=True, text=True, check=True)
        print(f"  ✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {description} failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"  ✗ {description} failed with error: {e}")
        return False

def uninstall_packages():
    """Uninstall all packages from requirements.txt"""
    
    # Check if requirements.txt exists
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt file not found!")
        return False
    
    print("🧹 Starting cleanup of global Python environment...")
    print("⚠️  WARNING: This will uninstall ALL packages listed in requirements.txt")
    print("⚠️  Make sure you're not in a virtual environment!")
    
    # Read requirements.txt and extract package names
    packages = []
    
    # Try different encodings
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
    content = None
    
    for encoding in encodings:
        try:
            with open('requirements.txt', 'r', encoding=encoding) as f:
                content = f.read()
            print(f"✓ Successfully read file with {encoding} encoding")
            break
        except UnicodeDecodeError:
            continue
    
    if content is None:
        print("❌ Could not read requirements.txt with any supported encoding")
        return False
    
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith('#'):
            # Extract package name (everything before ==)
            package_name = line.split('==')[0].split('>=')[0].split('<=')[0].split('>')[0].split('<')[0]
            # Clean up any remaining special characters
            package_name = package_name.strip().replace('\ufeff', '').replace('\x00', '')  # Remove BOM and null chars
            if package_name and package_name.isprintable():  # Only add valid printable package names
                packages.append(package_name)
    
    print(f"📦 Found {len(packages)} packages to uninstall")
    
    # Uninstall packages one by one to avoid command line length limits on Windows
    success_count = 0
    failed_packages = []
    
    for i, package in enumerate(packages, 1):
        print(f"\n📦 Uninstalling package {i}/{len(packages)}: {package}")
        
        # Use pip uninstall with -y flag to avoid prompts
        command = f"pip uninstall -y {package}"
        
        if run_command(command, f"Uninstalling {package}"):
            success_count += 1
        else:
            failed_packages.append(package)
    
    print(f"\n✅ Cleanup completed!")
    print(f"📊 Successfully uninstalled: {success_count} packages")
    print(f"📊 Failed to uninstall: {len(failed_packages)} packages")
    print(f"📊 Total packages in requirements.txt: {len(packages)}")
    
    if failed_packages:
        print(f"\n⚠️  Failed packages:")
        for package in failed_packages[:10]:  # Show first 10 failed packages
            print(f"   - {package}")
        if len(failed_packages) > 10:
            print(f"   ... and {len(failed_packages) - 10} more")
    
    return True

def verify_cleanup():
    """Verify the cleanup by checking remaining packages"""
    print("\n🔍 Verifying cleanup...")
    
    try:
        result = subprocess.run("pip list", shell=True, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')[2:]  # Skip header lines
        remaining_packages = len([line for line in lines if line.strip()])
        
        print(f"📦 Remaining packages in global environment: {remaining_packages}")
        
        if remaining_packages < 20:  # Reasonable number for a clean environment
            print("✅ Environment appears to be clean!")
        else:
            print("⚠️  Still many packages remaining. Some may be system packages or dependencies.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Could not verify cleanup: {e}")

if __name__ == "__main__":
    print("🐍 Python Environment Cleanup Tool")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  WARNING: You appear to be in a virtual environment!")
        print("⚠️  This script is designed to clean the GLOBAL Python environment.")
        print("⚠️  Please deactivate your virtual environment first.")
        response = input("\nDo you want to continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("❌ Cleanup cancelled.")
            sys.exit(1)
    
    # Confirm before proceeding
    print("\n⚠️  This will uninstall ALL packages listed in requirements.txt from your global Python environment.")
    response = input("Are you sure you want to continue? (y/N): ")
    
    if response.lower() != 'y':
        print("❌ Cleanup cancelled.")
        sys.exit(0)
    
    # Perform cleanup
    if uninstall_packages():
        verify_cleanup()
        print("\n🎉 Cleanup process completed!")
    else:
        print("\n❌ Cleanup process failed!")
        sys.exit(1)
