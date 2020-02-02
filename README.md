<div align="center" style="text-align:center">

<img align="center" width="400" src="https://i.imgur.com/gtn07cL.png">

<br>

Getting tired of manually writing unit test stubs for your Python code? Easy.

<img align="center" src="https://img.shields.io/pypi/v/pytestgen?style=flat-square">
<img align="center" src="https://img.shields.io/github/workflow/status/figglewatts/pytestgen/CI?style=flat-square">
<img align="center" src="https://img.shields.io/codecov/c/github/Figglewatts/pytestgen?style=flat-square">

</div>


## Example
```python
# file: example.py
def testable_func(arg_one, arg_two):
    pass

class AClass:
    def __init__(self, some, constructor, params):
        pass

    def testable_func_in_class(self, an_arg):
        pass
```

```bash
$ pytestgen example.py
```

```python
# file: test_example.py
import pytest

import example

@pytest.mark.parametrize(
    "arg_one,arg_two,expected",
    [
        # TODO: fill in test data for test_testable_func
        # pytest.param(, , id="")
    ]
)
def test_testable_func(arg_one, arg_two, expected):
    # TODO: create assertions for test_testable_func
    # example.testable_func(arg_one, arg_two)
    pass

@pytest.mark.parametrize(
    "instance,an_arg,expected",
    [
        # TODO: fill in test data for test_aclass_testable_func_in_class
        # pytest.param(example.AClass(some, constructor, params), , expected, id="")
    ]
)
def test_aclass_testable_func_in_class(instance, an_arg, expected):
    # TODO: write test for test_aclass_testable_func_in_class
    # TODO: create assertions for test_aclass_testable_func_in_class
    # instance.testable_func_in_class(an_arg)
    pass
```

## Installation
```bash
$ pip install pytestgen
```

## Usage
```bash
# generate tests for directory 'my_package' in 'tests/' directory
$ pytestgen my_package

# generate tests for some python files and directory 'the_package'
$ pytestgen my_module_a.py another_module.py the_package

# generate tests for directory 'cool_app' in 'cool_tests/' directory
$ pytestgen cool_app -o cool_tests

# generate tests for functions 'foo' and 'bar' in 'functionality.py'
$ pytestgen functionality.py -i foo -i bar
```

### Full usage text
```
Usage: pytestgen [OPTIONS] PATH...

  Generate pytest unit tests from your Python source code.

Options:
  -o, --output-dir PATH  The path to generate tests in.  [default: tests]
  -i, --include FUNC     Function names to generate tests for. You can use
                         this multiple times.
  -h, --help             Show this message and exit.
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
