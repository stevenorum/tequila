#!/usr/bin/env python3

from distutils.core import setup

MAJOR_VERSION='0'
MINOR_VERSION='0'
PATCH_VERSION='1'

VERSION = "{}.{}.{}".format(MAJOR_VERSION, MINOR_VERSION, PATCH_VERSION)

def main():
    setup(
        name = 'tequila',
        packages = ['tequila'],
        version = VERSION,
        description = 'Lambda-SES email forwarder',
        author = 'Steve Norum',
        author_email = 'sn@drunkenrobotlabs.org',
        url = 'https://github.com/stevenorum/tequila',
        download_url = 'https://github.com/stevenorum/tequila/archive/{}.tar.gz'.format(VERSION),
        keywords = ['python','aws','lambda','ses','email','cloudformation'],
        classifiers = [],
    )

if __name__ == "__main__":
    main()
