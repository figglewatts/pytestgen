from os.path import sep

import pytest

from pytestgen.load import PyTestGenInputSet, PyTestGenInputFile


@pytest.fixture
def test_input_set():
    def _make_input_set(with_output=False):
        return PyTestGenInputSet(
            f"test_data{sep}output" if with_output else "",
            [PyTestGenInputFile("file_a.py", "test_data")])

    return _make_input_set
