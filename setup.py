from pathlib import Path

from setuptools import find_packages, setup

readme_file = Path(__file__).parent.absolute().joinpath("README.md")
with readme_file.open(encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="pytest-bug",
    description="Pytest plugin for marking tests as a bug",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="tolstislon",
    author_email="tolstislon@gmail.com",
    url="https://github.com/tolstislon/pytest-bug",
    packages=find_packages(exclude=("tests", ".github")),
    use_scm_version={"write_to": "pytest_bug/__version__.py"},
    setup_requires=["setuptools_scm"],
    install_requires=["pytest>=7.1.0"],
    include_package_data=True,
    python_requires=">=3.7",
    license="MIT License",
    entry_points={"pytest11": ["pytest_bug = pytest_bug.plugin"]},
    keywords=["pytest"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
