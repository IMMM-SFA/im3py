"""Setup file for <your model name>

:author:   Chris R. Vernon
:email:    chris.vernon@pnnl.gov

License:  BSD 2-Clause, see LICENSE and DISCLAIMER files

"""

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


def get_requirements():
    with open('requirements.txt') as f:
        return f.read().split()


setup(
    name='im3py',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/IMMM-SFA/im3py.git',
    license='BSD 2-Clause',
    author='Chris R. Vernon',
    author_email='chris.vernon@pnnl.gov',
    description='A template Python model for IM3.',
    long_description=readme(),
    python_requires='>=3.6.*, <4',
    install_requires=get_requirements()
)
