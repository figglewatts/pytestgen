import os
from os import path

from click.testing import CliRunner
import pytest

from pytestgen.cli.pytestgen import cli


def mock_existing_files(package_dir, file_name):
    os.makedirs(package_dir, exist_ok=True)
    with open(path.join(package_dir, file_name), "w") as f:
        f.write("""def testable_func():
    pass


def testable_func_with_args(arg_one, arg_two):
    pass


class AClass:
    def __init__(self):
        pass

    def testable_func_in_class(self):
        pass""")


def mock_existing_files_tests_generated(package_dir, output_dir, file_name):
    os.makedirs(path.join(output_dir, package_dir), exist_ok=True)
    with open(path.join(output_dir, package_dir, f"test_{file_name}"),
              "w") as f:
        f.write("""def test_testable_func():
    pass


def test_testable_func_with_args():
    pass


def test_aclass_init():
    pass


def test_aclass_testable_func_in_class():
    pass


def not_a_test_function():
    pass""")


@pytest.mark.parametrize("help_arg", [("-h"), ("--help")])
def test_cli_help(help_arg, fs):
    """Make sure the CLI shows help text."""
    runner = CliRunner()
    result = runner.invoke(cli, [help_arg])
    assert result.exit_code == 0


@pytest.mark.parametrize("package_dir",
                         [("package_dir"),
                          (path.join("deeply", "nested", "package"))])
def test_cli_generate_tests_dir(package_dir):
    """Make sure we can generate tests from a directory."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        mock_existing_files(package_dir, "a_file.py")
        result = runner.invoke(cli, [package_dir, "-o", "output"])

        assert result.exit_code == 0

        assert path.exists(path.join("output", package_dir,
                                     "test_a_file.py")) == True


@pytest.mark.parametrize("package_dir",
                         [("package_dir"),
                          (path.join("deeply", "nested", "package"))])
def test_cli_generate_tests_file(package_dir):
    """Make sure we can generate tests from a file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        file_path = path.join(package_dir, "a_file.py")
        mock_existing_files(package_dir, "a_file.py")
        result = runner.invoke(cli, [file_path, "-o", "output"])

        assert result.exit_code == 0

        assert path.exists(path.join("output", package_dir,
                                     "test_a_file.py")) == True


@pytest.mark.parametrize("package_dir",
                         [("package_dir"),
                          (path.join("deeply", "nested", "package"))])
def test_cli_generate_tests_wrong_filetype(package_dir):
    """Make sure we error if the file wasn't a python file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        file_path = path.join(package_dir, "a_file.txt")
        mock_existing_files(package_dir, "a_file.txt")
        result = runner.invoke(cli, [file_path, "-o", "output"])

        assert result.exit_code == 1


def test_cli_generate_tests_nonexistent():
    """Make sure we error if the given path doesn't exist."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["nonexist", "-o", "output"])
        assert result.exit_code == 1
