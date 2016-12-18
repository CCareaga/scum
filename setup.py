import sys

from setuptools import setup

if sys.version_info[0] < 3:
    sys.exit("Scum requires Python 3.")

VERSION = 'v0.2.1'

setup_kwargs = {
    "version": VERSION,
    "description": 'A scummy editor for your terminal!',
    "author": 'Christian Careaga',
    "author_email": 'christian.careaga7@gmail.com',
    "url": 'https://github.com/CCareaga/scum',
    "download_url": "https://github.com/CCareaga/scum/zipball/" + VERSION,
    "install_requires":['urwid', 'Pygments'],
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
        scripts=['scum'],
        data_files=[('', ['README.rst'])],
        packages = ['src.modules', 'src', 'src.resources'],
        package_data = {'src.resources': ['config.txt', 'start_up.txt', 'tabs.dat', 'help.txt']},
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
