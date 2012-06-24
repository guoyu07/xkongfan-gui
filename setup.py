from distutils.core import setup
import py2exe

setup(
    windows = [{"script":"main.py", "icon_resources": [(1, "resource/icon.ico")]}],
    options = {
        "py2exe" : {
            "includes" : ['sys', 'tempfile', 'zipfile', 'mmap', 'encodings',
                          'json', 'hashlib', 'datetime', 'struct',
                          'os', 'time', 'random', 'math', 'xmlrpclib', 'crypto']
        }
    }
)