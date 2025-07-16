from setuptools import setup, find_packages

setup(
    name='qgjob',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'qgjob=qgjob.cli:cli',
        ],
    },
    author='QualGent',
    description='QualGent Job CLI for AppWright test orchestration',
    python_requires='>=3.7',
) 