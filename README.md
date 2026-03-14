# Simple Python Obfuscator — Quick Guide

This is a tiny toolset to hide Python code and get it back later. Plain language, step-by-step.

Files you have
- [sysinfo.py](sysinfo.py) — example program.
- [obfuscator.py](obfuscator.py) — makes an obfuscated file that hides your code.
- [deobfuscator.py](deobfuscator.py) — recovers the original code when you give the right password.
- [test_pipeline.py](test_pipeline.py) — quick demo that runs the full flow.

How to use (3 easy steps)

1) Make a hidden (obfuscated) file

Run this and type a password when asked (or add `--key`):

```bash
python obfuscator.py sysinfo.py obf_sysinfo.py --key mypassword
# or interactive:
python obfuscator.py sysinfo.py obf_sysinfo.py
```

This writes `obf_sysinfo.py`. The password is NOT stored inside the file.

2) Run the hidden file

You must give the same password when running the obfuscated file. Options:

```bash
# pass via environment variable
OBF_KEY=mypassword python obf_sysinfo.py

# or pass as first argument
python obf_sysinfo.py mypassword

# or run and type the password at the prompt
python obf_sysinfo.py
```

3) Get the original file back

If you ever need the original code again, run:

```bash
python deobfuscator.py obf_sysinfo.py mypassword decoded_sysinfo.py
```

Simple safety notes
- Keep your password secret. If someone has it, they can read your original code.
- This tool hides code but is not perfect security. For strong protection, use proper encryption libraries and secure storage.

Want help making this stronger (real encryption or signing)? Tell me which option you prefer.
