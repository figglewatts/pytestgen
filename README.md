# pytestgen

Generate pytest tests from your Python source files.

```
Usage: pytestgen [OPTIONS] PATH...

  Generate pytest unit tests from your Python source code.

  Examples:
      # generate tests for directory 'my_package' in 'tests/' directory
      $ pytestgen my_package

      # generate tests for some python files and directory 'the_package'
      $ pytestgen my_module_a.py another_module.py the_package

      # generate tests for directory 'cool_app' in 'cool_tests/' directory
      $ pytestgen cool_app -o cool_tests

      # generate tests for functions 'foo' and 'bar' in 'functionality.py'
      $ pytestgen functionality.py -i foo -i bar

Options:
  -o, --output-dir PATH  The path to generate tests in.  [default: tests]
  -i, --include FUNC     Function names to generate tests for. You can use
                         this multiple times.
  -h, --help             Show this message and exit.
```