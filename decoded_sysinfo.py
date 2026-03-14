#!/usr/bin/env python3
import platform
import sys
import os

def main():
    print("System:", platform.system(), platform.release())
    print("Platform:", platform.platform())
    print("Python:", sys.version.replace('\n',' '))
    print("Processor:", platform.processor())
    print("Machine:", platform.machine())
    print("Environment variables (sample):")
    for k in sorted(list(os.environ.keys())[:10]):
        print(f"  {k}={os.environ[k]}")

if __name__ == '__main__':
    main()
