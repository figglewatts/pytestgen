"""output.py

Used for getting/organising outputs for pytestgen.

Author:
    Figglewatts <me@figglewatts.co.uk>
"""

from os import path


def find_test_file(src_file_path: str, output_dir: str) -> str:
    """Given a source file path and output test directory, figure
    out if there's an existing test file for this source file.

    Args:
        src_file_path (str): The source file path.
        output_dir (str): The directory to create tests in.

    Returns:
        str: The name of the test file if it was found, or None if not.
    """
    src_filename = path.basename(src_file_path)
    src_dir = path.dirname(src_file_path)
    test_name = path.join(output_dir, src_dir, f"test_{src_filename}")
    if not path.exists(test_name):
        return None

    return test_name