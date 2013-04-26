from distutils.core import setup
import py2exe

setup(
    windows = [{"script":"main.py", "icon_resources": [(1, "resource/icon.ico")]}],
    options = {
        "py2exe" : {
            "includes" : ['sys', 'encodings','json', 'os', 'time']
        }
    }
)