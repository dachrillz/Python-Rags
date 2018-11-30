import sys
from pprint import pprint

import example.min_tree as example


def display_help():
    pprint("Possible args -- test, example, help")
    pprint("test -- Run tests")
    pprint("example -- run example file in example folder")
    pprint("help -- Diplsay this text")


if len(sys.argv) != 2:
    display_help()
else:
    first_arg = sys.argv[1]

    if first_arg == 'test':
        import pytest

        pytest.main()

    elif first_arg == 'example':
        example.run_example()

    elif first_arg == 'help':
        display_help()
    else:
        display_help()
