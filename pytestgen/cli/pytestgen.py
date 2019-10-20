"""pytestgen.py

This is the CLI of pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import click

from ..input import _get_python_files_from_package


@click.command()
def cli():
    _get_python_files_from_package('pytestgen', '')


if __name__ == "__main__":
    cli()