# -*- coding: utf-8 -*-
from distutils.core import setup
from glob import glob

PACKAGE_NAME = 'minescrubber_core'
PACKAGE_VERSION = '0.0.1'

setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    description='The classic game of minesweeper',
    author='Alok Gandhi',
    author_email='alok.gandhi2002@gmail.com',
    url='https://github.com/alok1974/minescrubber_core',
    packages=[
        'minescrubber_core',
    ],
    package_data={
        'minescrubber_core': ['*.py'],
    },
    package_dir={
        'minescrubber_core': 'src/minescrubber_core'
    },
    scripts=glob('src/scripts/*'),
    install_requires=[
    ],
    license='MIT',
    download_url='',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Board Games',
        'License :: OSI Approved :: MIT License',
    ],
)
