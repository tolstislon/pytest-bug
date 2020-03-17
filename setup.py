from setuptools import setup, find_packages
from os import path
import pytest_bug

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytest-bug',
    description=pytest_bug.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=pytest_bug.__version__,
    author=pytest_bug.__author__,
    author_email=pytest_bug.__author_email__,
    url=pytest_bug.__url__,
    packages=find_packages(exclude=('tests',)),
    install_requires=['pytest>=3.6.0'],
    include_package_data=True,
    python_requires='>=3.6',
    license=pytest_bug.__license__,
    entry_points={'pytest11': ['pytest_bug = pytest_bug.conftest']},
    keywords=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Testing'
    ]
)
