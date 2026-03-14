#!/usr/bin/env python3
import sys
import re
import base64
import hashlib


def extract_payload(path):
    text = open(path, 'r', encoding='utf-8').read()
    # base64 payload (supports triple-quoted or single/double-quoted)
    m = re.search(r'_b64\s*=\s*"""(.+?)"""', text, re.S)
    if not m:
        m = re.search(r"_b64\s*=\s*([\'\"])" + r"(.+?)" + r"\1", text, re.S)
    if not m:
        raise ValueError('No embedded base64 payload found')
    # For the first pattern group 1 is the content; for the second, group 2 is the content
    if m.lastindex == 1:
        b64 = m.group(1)
    else:
        b64 = m.group(2)

    m2 = re.search(r'_salt_hex\s*=\s*"([0-9a-fA-F]+)"', text)
    if not m2:
        m2 = re.search(r"_salt_hex\s*=\s*([\'\"])" + r"([0-9a-fA-F]+)" + r"\1", text)
    salt = bytes.fromhex(m2.group(1) if m2 and m2.lastindex==1 else (m2.group(2) if m2 else '')) if m2 else None

    m3 = re.search(r"_iters\s*=\s*(\d+)", text)
    iters = int(m3.group(1)) if m3 else None

    return b64, salt, iters


def xor_bytes(data: bytes, key_bytes: bytes) -> bytes:
    return bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])


def main():
    if len(sys.argv) < 3:
        print('Usage: deobfuscator.py obfuscated.py password [out.py]')
        sys.exit(2)
    obf = sys.argv[1]
    password = sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else obf + '.decoded.py'
    b64, salt, iters = extract_payload(obf)
    raw = base64.b64decode(b64)

    if salt is None or iters is None:
        print('Missing salt/iterations in obfuscated file; cannot derive key')
        sys.exit(3)

    key_bytes = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iters, dklen=32)
    orig = xor_bytes(raw, key_bytes)
    with open(out, 'wb') as f:
        f.write(orig)
    print('Wrote decoded file to', out)


if __name__ == '__main__':
    main()
