#!/usr/bin/env python3
"""Simple interactive CLI to obfuscate Python or Go files.

Prompts for language, file path (or example), and password; writes outputs into `dist/<lang>/`.
"""
import os
import subprocess
import shutil
import getpass


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _ansi(code: str, text: str) -> str:
    return f"\x1b[{code}m{text}\x1b[0m"


def bold(text: str) -> str:
    return _ansi('1', text)


def green(text: str) -> str:
    return _ansi('32', text)


def cyan(text: str) -> str:
    return _ansi('36', text)


def yellow(text: str) -> str:
    return _ansi('33', text)


def red(text: str) -> str:
    return _ansi('31', text)


def choose(prompt, options):
    print(bold(cyan('\n' + prompt)))
    for i, o in enumerate(options, 1):
        print('  ' + green(f'{i})') + ' ' + o)
    while True:
        choice = input(bold('Choose number: ')).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(red('Invalid choice, try again.'))


def print_box(title: str):
    width = min(72, shutil.get_terminal_size((80, 20)).columns)
    line = '+' + '-' * (width - 2) + '+'
    print(cyan(line))
    centered = title.center(width - 2)
    print(cyan('|' + centered + '|'))
    print(cyan(line))


def run(cmd, cwd=None):
    print(bold('>') + ' ' + ' '.join(cmd))
    res = subprocess.run(cmd, cwd=cwd)
    if res.returncode != 0:
        print(red(f'Command failed (exit {res.returncode})'))
        raise SystemExit(res.returncode)


def main():
    root = os.path.dirname(__file__)
    examples_dir = os.path.join(root, 'examples')
    dist_dir = os.path.join(root, 'dist')
    ensure_dir(examples_dir)
    ensure_dir(dist_dir)

    print_box('Simple Obfuscator — interactive')
    lang = choose('Which language do you want to obfuscate?', ['python', 'golang'])

    # show examples for chosen language
    ex_lang_dir = os.path.join(examples_dir, lang)
    example_files = []
    if os.path.isdir(ex_lang_dir):
        example_files = [os.path.join(ex_lang_dir, f) for f in os.listdir(ex_lang_dir) if os.path.isfile(os.path.join(ex_lang_dir, f))]

    print('\n' + bold('Provide the path to the source file to obfuscate.'))
    if example_files:
        print('You can type the full path, or pick an example:')
        for i, f in enumerate(example_files, 1):
            print(f'  {i}) {f}')
        inp = input('File path or number (enter to choose example 1): ').strip()
        if inp == '':
            src = example_files[0]
        elif inp.isdigit() and 1 <= int(inp) <= len(example_files):
            src = example_files[int(inp)-1]
        else:
            src = inp
    else:
        src = input('File path: ').strip()

    if not os.path.isabs(src):
        src = os.path.join(root, src) if os.path.exists(os.path.join(root, src)) else os.path.abspath(src)

    if not os.path.exists(src):
        print('File not found:', src)
        raise SystemExit(1)

    password = getpass.getpass('Password to derive key: ')
    if password.strip() == '':
        print('Empty password not allowed')
        raise SystemExit(2)

    # prepare output path
    out_lang_dir = os.path.join(dist_dir, lang)
    ensure_dir(out_lang_dir)
    base = os.path.basename(src)
    obfname = f'obf_{base}'
    outpath = os.path.join(out_lang_dir, obfname)

    print_box('Obfuscation')
    print(yellow('\nObfuscating') + ' ' + src + ' ' + yellow('->') + ' ' + outpath)
    if lang == 'python':
        # call python obfuscator
        obf_script = os.path.join(root, 'python', 'obfuscator.py')
        run(['python3', obf_script, src, outpath, '--key', password])
        print('\n' + bold('To run:'))
        print(green(f'  OBF_KEY={password} python3 {outpath}'))
        print(green(f'  python3 {outpath} {password}'))
        print('\n' + bold('To decode:'))
        print(green(f'  python3 python/deobfuscator.py {outpath} {password} {os.path.join(out_lang_dir, "decoded_"+base)}'))

    else:  # golang
        obf_go = os.path.join(root, 'go', 'obfuscator.go')
        # check that `go` exists before trying to run it
        if shutil.which('go') is None:
            print(red('\nGo toolchain not found on PATH.'))
            print('Install Go and ensure `go` is on your PATH. Example (macOS/Homebrew):')
            print(yellow('  brew install go'))
            print('Or download from https://go.dev/dl/')
            raise SystemExit(10)
        # use `go run` to produce wrapper directly
        run(['go', 'run', obf_go, '-in', src, '-out', outpath, '-key', password])
        print('\n' + bold('To run wrapper:'))
        print(green(f'  OBF_KEY={password} go run {outpath}'))
        print(green(f'  go run {outpath} {password}'))
        print('\n' + bold('To decode (Go):'))
        print(green(f'  go run go/deobfuscator.go -in {outpath} -pass {password} -out {os.path.join(out_lang_dir, "decoded_"+base)}'))

    print('\nDone. Output written to', outpath)


if __name__ == '__main__':
    main()
