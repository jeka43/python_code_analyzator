from setuptools import setup, find_packages

setup(
    name='python_code_analyzator',
    version='0.1.0',
    packages=find_packages(),
    description='A library for analyzing Python code.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Evgeny',
    url='https://github.com/jeka43/python_code_analyzator',
    python_requires='>=3.6',
)
