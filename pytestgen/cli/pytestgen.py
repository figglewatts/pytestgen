"""pytestgen.py

This is the CLI of pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import click

from pytestgen import load
from pytestgen import parse
from pytestgen import output


@click.command()
@click.argument("input_dir", nargs=-1, type=str)
@click.argument("output_dir", nargs=1, type=str)
def cli(input_dir, output_dir):
    for in_dir in input_dir:
        input_set = load.directory(in_dir, output_dir)
        parsed_set = parse.parse_input_set(input_set)
        output.output_tests(parsed_set)


if __name__ == "__main__":
    cli.invoke(ctx={})