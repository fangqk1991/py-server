import os

from setuptools import setup, find_packages

DIR = os.path.dirname(__file__)
REQUIREMENTS = os.path.join(DIR, 'requirements.txt')


with open(REQUIREMENTS) as f:
    reqs = f.read()

setup(
    name='fc-server',
    version='0.0.1',
    description='messenger for python',
    license='MIT Licence',
    url='https://github.com/fangqk1991/py-server',
    author='fang',
    author_email='me@fangqk.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=reqs.strip().split('\n'),
)
