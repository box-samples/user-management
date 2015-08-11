# coding: utf-8

from __future__ import unicode_literals

from os.path import dirname, join
import sys
from sys import version_info

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


CLASSIFIERS = []


def main():
    base_dir = dirname(__file__)
    install_requires = ['boxsdk>=1.2.1', 'py>=1.4.30']
    setup(
        name='tc_scripts',
        version='0.0.1',
        description='Collection of useful scripts used by Box Technical Consulting',
        long_description=open(join(base_dir, 'README.rst')).read(),
        author='Box',
        author_email='oss@box.com',
        url='http://opensource.box.com',
        packages=find_packages(exclude=['Packaged Individual Scripts', 'django_project']),
        install_requires=install_requires,
        classifiers=CLASSIFIERS,
        keywords='box oauth2 sdk',
        license=open(join(base_dir, 'LICENSE')).read(),
        entry_points={
            'console_scripts': [
                'box-provision = tc_scripts.scripts.provision:main',
                'box-deprovision = tc_scripts.scripts.deprovision:main',
                'box-populate-demo-account = tc_scripts.scripts.populate_demo_account:main',
            ]
        }
    )


if __name__ == '__main__':
    main()
