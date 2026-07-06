"""
C++ compilation helper
"""
import subprocess
import os
import sys

def compile_analytics():
    cpp_file = os.path.join(os.path.dirname(__file__), "analytics.cpp")
    out_file = os.path.join(os.path.dirname(__file__), "analytics.exe" if sys.platform == "win32" else "analytics")
    
    if not os.path.exists(cpp_file):
        print("C++ source file not found!")
        return False
        
    try:
        # Check if g++ is installed
        subprocess.run(["g++", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("g++ compiler detected. Compiling C++ analytics engine...")
        # Compile
        subprocess.run(["g++", "-O3", cpp_file, "-o", out_file], check=True)
        print(f"Compilation success! Executable saved at: {out_file}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: g++ compiler not found or compilation failed. Application will fallback to python analytics emulator.")
        return False

if __name__ == "__main__":
    compile_analytics()
