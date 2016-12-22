import sys

from setuptools import setup

if sys.version_info[0] < 3:
    sys.exit("Scum requires Python 3.")

VERSION = 'v0.2.7'

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
        entry_points={
            'console_scripts': [
                'scum = scum.scum:main'
            ]
        },
        data_files=[('', ['README.rst'])],
        packages = ['scum.modules', 'scum', 'scum.resources'],
        package_data = {'scum.resources': ['config.txt', 'start_up.txt', 'tabs.dat', 'help.txt']},
        long_description=open('README.rst').read(),
        **setup_kwargs
        )
