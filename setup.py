from setuptools import setup

APP = ['gui.py']
DATA_FILES = ['telegram_api.py', ('', ['images']), ('', ['texts'])]
OPTIONS = {
    'argv_emulation': True,
    'site_packages': True,
    'iconfile': 'appicon.icns',
    'packages': ['wx', 'telethon'],
    'plist': {
        'CFBundleName': 'follow_unfollow',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
