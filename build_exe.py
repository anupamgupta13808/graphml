import os
import subprocess
import sys

def build_exe():
    # Ensure PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define the command to build the executable
    cmd = [
        "pyinstaller",
        "--name=GraphMLConverter",
        "--onefile",
        "--windowed",
        "--add-data=src;src",  # Include the src directory
        "src/main.py"
    ]

    # Run the command
    subprocess.check_call(cmd)

if __name__ == "__main__":
    build_exe() 