# coding: utf-8

from __future__ import unicode_literals
from os.path import dirname, join
from setuptools import setup, find_packages


CLASSIFIERS = []


def main():
    base_dir = dirname(__file__)
    install_requires = ['boxsdk>=1.2.1', 'py>=1.4.30']
    setup(
        name='box_manage_users',
        version='0.0.3',
        description='Collection of useful scripts used by Box Technical Consulting',
        long_description=open(join(base_dir, 'README.rst')).read(),
        author='Box',
        author_email='oss@box.com',
        url='http://opensource.box.com',
        packages=find_packages(exclude=['Packaged Individual Scripts', 'django_project']),
        install_requires=install_requires,
        classifiers=CLASSIFIERS,
        keywords='box admin enterprise users',
        license=open(join(base_dir, 'LICENSE')).read(),
        entry_points={
            'console_scripts': [
                'box-provision = box_manage_users.scripts.provision:main',
                'box-deprovision = box_manage_users.scripts.deprovision:main',
                'box-populate-demo-account = box_manage_users.scripts.populate_demo_account:main',
            ]
        }
    )


if __name__ == '__main__':
    main()
