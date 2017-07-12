from setuptools import setup, find_packages

setup(
    name='cronlog-client',
    version='1.0.0',
    packages=find_packages(),
    install_requires = ['thrift==0.9.3', 'click==3.3'],
    author='Surya Prashanth',
    author_email='prashantsurya@ymail.com',
)
