#!/usr/bin/env python3
import subprocess
import os
import sys
import difflib

def run(cmd, env=None):
    print('>',' '.join(cmd))
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.stdout:
        print(res.stdout, end='')
    if res.stderr:
        print(res.stderr, file=sys.stderr, end='')
    return res.returncode

def main():
    pwd = 'test'
    infile = 'sysinfo.py'
    obf = 'obf_sysinfo.py'
    decoded = 'decoded_sysinfo.py'

    for f in (obf, decoded):
        try:
            os.remove(f)
        except OSError:
            pass

    # Obfuscate
    rc = run(['python3', 'obfuscator.py', infile, obf, '--key', pwd])
    if rc != 0:
        print('Obfuscation failed', file=sys.stderr)
        sys.exit(1)

    # Run obfuscated (use OBF_KEY env)
    env = os.environ.copy()
    env['OBF_KEY'] = pwd
    rc = run(['python3', obf], env=env)
    if rc != 0:
        print('Running obfuscated file failed', file=sys.stderr)
        sys.exit(2)

    # Decode
    rc = run(['python3', 'deobfuscator.py', obf, pwd, decoded])
    if rc != 0:
        print('Decoding failed', file=sys.stderr)
        sys.exit(3)

    # Compare
    with open(infile, 'rb') as f:
        a = f.read()
    with open(decoded, 'rb') as f:
        b = f.read()

    if a == b:
        print('SUCCESS: decoded matches original')
        sys.exit(0)
    else:
        print('FAIL: decoded differs')
        for line in difflib.unified_diff(a.decode('utf-8','replace').splitlines(), b.decode('utf-8','replace').splitlines(), lineterm=''):
            print(line)
        sys.exit(4)

if __name__ == '__main__':
    main()
