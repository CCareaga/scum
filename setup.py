import sys

from distutils.core import setup
have_setuptools = False

from pkgutil import walk_packages

if sys.version_info[0] < 3:
    sys.exit("Scum requires Python 3.")

VERSION = 'v1.1.7'

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
        ]
    }


if __name__ == '__main__':
    setup(
        name='scum',
        py_modules=['src.main', 'scum'],
        data_files=[('', ['README.rst'])],
        packages = ['src.modules', 'src', 'src.resources'],
        package_data = {'src.resources': ['config.txt', 'start_up.txt', 'tabs.dat', 'help.txt']},
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
