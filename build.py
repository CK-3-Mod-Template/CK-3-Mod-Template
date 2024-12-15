import os
import platform
import subprocess
import sys

def build_executable():
    system = platform.system()
    
    # PyInstaller configuration
    spec_file = 'gui.spec'
    
    # Create PyInstaller spec file
    subprocess.run([
        'pyinstaller', 
        '--onefile', 
        '--windowed', 
        '--name=CK3ModCreator', 
        'gui.py'
    ], check=True)
    
    # Platform-specific adjustments
    if system == 'Windows':
        print("Building Windows executable...")
        output_name = 'CK3ModCreator.exe'
    elif system == 'Darwin':
        print("Building macOS application...")
        output_name = 'CK3ModCreator.app'
    elif system == 'Linux':
        print("Building Linux executable...")
        output_name = 'CK3ModCreator'
    else:
        raise RuntimeError(f"Unsupported platform: {system}")
    
    print(f"Build complete. Output: {output_name}")

if __name__ == '__main__':
    build_executable()