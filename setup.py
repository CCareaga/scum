import sys

from distutils.core import setup
have_setuptools = False

from pkgutil import walk_packages

import modules

if sys.version_info[0] < 3:
    sys.exit("Scum requires Python 3.")

VERSION = 'v0.2'

setup_kwargs = {
    "version": VERSION,
    "description": 'Scum text editor',
    "author": 'Christian Careaga',
    "author_email": 'christian.careaga7@gmail.com',
    "url": 'https://github.com/CCareaga/scum',
    "download_url": "https://github.com/CCareaga/scum/zipball/" + VERSION,
    "requires":['urwid', 'pygments'],
    "classifiers": [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: Text Editors",
        ],
    "data_files": [("", ['README.rst']),
                   ("resources", ['resources/config.txt', 'resources/help.txt', 'resources/start_up.txt', 'resources/tabs.dat'])]
    }


if __name__ == '__main__':
    setup(
        name='scum',
        py_modules=['scum'],
        scripts=['scum'],
        packages = ['modules'],
        include_package_data=True,
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
