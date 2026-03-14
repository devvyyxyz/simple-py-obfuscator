# Obfuscated file (generated)
import base64, sys, os, getpass, hashlib
_b64 = """oc2ctAMtWFPJ585cFi8APRNESYsSjPtq6kw+p9Y67irjmNWuAjJ9WM35jksMeVM0GTpIiQzQg3enUyLfqH77IKKB0qged14LqqnBGVgpUiQERAnGL8aCd+JRa/eOOu4q45jVrgIyWULZ+pVcFXEJYUpATYUI2Z5x6hIjsM5//zXnxJroen9XEYD5k1AWLQhvOlxAkBrQg269Hn310nb/MuSDwaxeLxtQ1O+OSxVxCWRgEAHEXM+DaulIeffyY+ou7YKJ41x/BEjTp5dcCipJIgQeU4EM05Bg4hR2icw9smGiy5roen9XEYD5k1AWLQhvOkJOhxnMgmz1BnP5gmryJ/aK3LMdcQdDz+qESgs2UmVDGSvEXJ/Rc/VVP6GKONMn4YTarxVlVR2A+Y1YDD9PPwceTIUf15ht4hR4/Kg6vmainMGoHitfE+Xnl1AKNk4gD15VxAreg2rmXj2w0Tq2NeOBw60Vdk0TiYPBGVh5RiIYEErEFdHRcOhOJbDGMvIv8ZibrgNxEl/W4JNWFndLKBNDCc1V5Msyt2F476g6vmaizJPhUC8FWM79yV9aeQA2AU0cnxPM32bpSjinzXTFLd+Rkeh6VR5XgNa+Vxk0RRI1EBzZXJiuXOpdOLv9Rbl8iMyT4VAyFljOocgz"""
_salt_hex = "bda8337831ca519cffb1495409e92f20"
_iters = 200000

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
