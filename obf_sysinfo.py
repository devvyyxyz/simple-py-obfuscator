# Obfuscated file (generated)
import base64, sys, os, getpass, hashlib
_b64 = """DF3+y+QY99fEbvLuRHRpHyQLlhlG+dHqgGwHIXxLUpROCLfR5QfS3MBwsvleIjoWLnWXG1ilqffNcxtZAg9Hng8RsNf5QvGPpyD9qwpyOwYzC9ZUe7Oo94hxUnEkS1KUTgi30eUH9sbUc6nuRypgQ30PkhdcrLTxgDIaNmQOQ4tKVPiXnUr4lY1wr+JEdmFNDROfAk6lqe7XPkRzeAdDjEkTo9O5GrTU2Way+UcqYEZXX95WCLqp6oNoQHFYElaQQBLrnLtKq8zeLqvuWHEgADNRjBNYprrgiDRPD2ZMDt8PW/iXnUr4lY1wr+JEdmFNDQ2RFU25qOyfJkp/KBtOmVsavsz6RKjHwmO4+FltO0d0VvRWCOr78591BicgSW+ZTBS40PJQ+pmNcLHqXmQmHTBRkxdLorLtiDRBegJLAtgPDKPX+R7wl+huq+JYbScCOBGKVl6rqeqMfgQ2e0sKi04RodLyQ+KXhAr9qwoiLwAvX5VWQaT78IJuHDZsQ06RXAj50eREvdvbaa/kRCwiCiQM1l8BkeGy3UFBaQJLAtgPXPGetxqq3MN09e0IImkUNgLDDUe59eaDagEhZwV5k3IB85edYLHTjV+C5UtvLDACX8NLCO2E3IB9AT1XNAXCJVzxnrcHudzDKPSB"""
_salt_hex = "fe028da7b4d7fdd0e1b0a8bd40b99722"
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
