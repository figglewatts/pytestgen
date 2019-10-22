"""pytestgen.py

This is the CLI of pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import click

from .. import input
from .. import parse


@click.command()
def cli():
    input_set = input.package("pytestgen", "")
    parsed_set = parse.parse_input_set(input_set)
    for f in parsed_set.parsed_files:
        for func in f.testable_funcs:
            print(func.get_test_name())


if __name__ == "__main__":
    cli()