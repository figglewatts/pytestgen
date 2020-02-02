"""setup.py

The setup script of pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""

from os import path
from setuptools import setup, find_packages

here = path.join(path.dirname(__file__))


def get_repo_file_content(filename: str) -> str:
    with open(path.join(here, filename), encoding="utf-8") as f:
        return f.read()


setup(
    name="pytestgen",
    version="#{VERSION}#",
    description="Generate pytest tests from your Python source files.",
    long_description=get_repo_file_content("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/Figglewatts/pytestgen",
    author="Figglewatts",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Testing",
    ],
    keywords="testing test generation pytest",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7",
    install_requires=["click==7.0", "jinja2==2.11.0", "markupsafe==1.1.1"],
    entry_points={
        "console_scripts": ["pytestgen=pytestgen.cli.pytestgen:cli"]
    },
)
