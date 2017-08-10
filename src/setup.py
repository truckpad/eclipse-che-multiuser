#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='eclipse-che-provisioner',
    version='0.0.1',
    description='Eclipse Che Provisioner, for using with bit.ly oauth2_proxy, nginx and docker',
    packages=find_packages(),
    license='MIT',
    author='Marcos Araujo Sobrinho',
    author_email='marcos.sobrinho@truckpad.com.br',
    url='https://github.com/truckpad/eclipse-che-multiuser/',
    download_url='https://github.com/truckpad/eclipse-che-multiuser/',
    keywords=['docker', 'eclipse', 'eclipse-che', 'ide'],
    # long_description=open('README.md').read(),
    scripts=['eclipse-che/provisioner.py'],
    install_requires=open('requirements.txt').read().strip('\n').split('\n')
)
