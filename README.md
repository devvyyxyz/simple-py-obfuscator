# Simple Python Obfuscator — Quick Guide

This is a tiny toolset to hide Python code and get it back later. Plain language, step-by-step.

Files you have
- python/: Python tools and examples (`sysinfo.py`, `obfuscator.py`, `deobfuscator.py`, `test_pipeline.py`).
- go/: Go obfuscator and deobfuscator wrappers (`obfuscator.go`, `deobfuscator.go`).

How to use (3 easy steps)

1) Make a hidden (obfuscated) file

Run the Python obfuscator from the `python/` folder and type a password when asked (or add `--key`):

```bash
python3 python/obfuscator.py python/sysinfo.py python/obf_sysinfo.py --key mypassword
# or interactive:
python3 python/obfuscator.py python/sysinfo.py python/obf_sysinfo.py
```

This writes `python/obf_sysinfo.py`. The password is NOT stored inside the file.

2) Run the hidden file

You must give the same password when running the obfuscated file. Options:

```bash
# pass via environment variable
OBF_KEY=mypassword python3 python/obf_sysinfo.py

# or pass as first argument
python3 python/obf_sysinfo.py mypassword

# or run and type the password at the prompt
python3 python/obf_sysinfo.py
```

3) Get the original file back (Python)

If you ever need the original code again, run:

```bash
python3 python/deobfuscator.py python/obf_sysinfo.py mypassword python/decoded_sysinfo.py
```

3b) Go obfuscator quick example

Build or run the Go obfuscator to produce a Go wrapper that decodes and runs the original Go source at runtime:

```bash
# build the obfuscator
go build -o go/obfuscator go/obfuscator.go
# obfuscate a Go file
./go/obfuscator -in myprog.go -out obf_myprog.go -key mypassword
# run the wrapper (it will prompt or accept OBF_KEY or arg)
OBF_KEY=mypassword go run obf_myprog.go
```
