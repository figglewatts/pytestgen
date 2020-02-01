"""pytestgen.py

This is the CLI of pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""
import logging
from os.path import isdir, exists

import click

from pytestgen import load
from pytestgen import parse
from pytestgen import output

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("path", nargs=-1, type=str, required=True)
@click.option("--output-dir",
              "-o",
              default="tests",
              type=str,
              show_default=True,
              metavar="PATH",
              help="The path to generate tests in.")
@click.option(
    "--include",
    "-i",
    multiple=True,
    default=[],
    metavar="FUNC",
    help="Function names to generate tests for. You can use this multiple times."
)
def cli(path, output_dir, include):
    """Generate pytest unit tests from your Python source code.

    \b
    Examples:
        # generate tests for directory 'my_package' in 'tests/' directory
        $ pytestgen my_package

    \b
        # generate tests for some python files and directory 'the_package'
        $ pytestgen my_module_a.py another_module.py the_package

    \b
        # generate tests for directory 'cool_app' in 'cool_tests/' directory
        $ pytestgen cool_app -o cool_tests

    \b
        # generate tests for functions 'foo' and 'bar' in 'functionality.py'
        $ pytestgen functionality.py -i foo -i bar
    """
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    for path_element in path:
        if not exists(path_element):
            logging.error(f"ERROR: path '{path_element}' did not exist")

        input_set = None
        if isdir(path_element):
            input_set = load.directory(path_element, output_dir)
        else:
            try:
                input_set = load.filename(path_element, output_dir)
            except ValueError as err:
                logging.error("ERROR: " + str(err))
                raise SystemExit(1)
        parsed_set = parse.parse_input_set(input_set)
        output.output_tests(parsed_set, include=include)


if __name__ == "__main__":
    cli.invoke(ctx={})