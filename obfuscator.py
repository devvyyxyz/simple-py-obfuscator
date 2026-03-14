#!/usr/bin/env python3
import argparse
import base64
import sys
import os
import getpass
import hashlib
import secrets


def xor_bytes(data: bytes, key_bytes: bytes) -> bytes:
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])


def obfuscate(input_path: str, output_path: str, password: str):
    with open(input_path, 'rb') as f:
        src = f.read()

    # Derive a symmetric key from the password using PBKDF2
    salt = secrets.token_bytes(16)
    iterations = 200_000
    key_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations, dklen=32)

    enc = xor_bytes(src, key_bytes)
    b64 = base64.b64encode(enc).decode('ascii')

    # Emit stub that contains the salt and iterations (so the runtime can derive the key)
    stub = f'''# Obfuscated file (generated)
import base64, sys, os, getpass, hashlib
_b64 = """{b64}"""
_salt_hex = "{salt.hex()}"
_iters = {iterations}

_key = os.environ.get('OBF_KEY')
if not _key:
    if len(sys.argv) > 1:
        _key = sys.argv[1]
    else:
        try:
            _key = getpass.getpass('Password: ')
        except Exception:
            print('Missing key: set OBF_KEY, pass as first arg, or provide via prompt')
            sys.exit(1)

def _xor(data, key_bytes):
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])

salt = bytes.fromhex(_salt_hex)
key_bytes = hashlib.pbkdf2_hmac('sha256', _key.encode(), salt, _iters, dklen=32)
code = _xor(base64.b64decode(_b64), key_bytes)
exec(compile(code, '<obfuscated>', 'exec'))
'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(stub)
    print('Wrote obfuscated file:', output_path)


def main():
    p = argparse.ArgumentParser(description='PBKDF2-based obfuscator (XOR keystream)')
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--key', required=False, help='Secret password used to derive the key')
    args = p.parse_args()

    password = args.key
    if not password:
        try:
            password = getpass.getpass('Password to derive key: ')
        except Exception:
            print('Provide --key or run interactively')
            sys.exit(2)

    obfuscate(args.input, args.output, password)


if __name__ == '__main__':
    main()
