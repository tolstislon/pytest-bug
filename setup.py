from setuptools import setup, find_packages
from os import path
import pytest_bug

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytest-bug',
    description='Pytest plugin Mark test as a bug',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=pytest_bug.__version__,
    author='tolstislon',
    author_email='tolstislon@gmail.com',
    url='https://github.com/tolstislon/pytest-bug',
    packages=find_packages(exclude=('tests',)),
    install_requires=['pytest>=3.6.0'],
    include_package_data=True,
    python_requires='>=3.5',
    license='MIT License',
    entry_points={'pytest11': ['pytest_bug = pytest_bug.plugin']},
    keywords=['pytest'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Pytest',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Testing'
    ]
)
