import sys
from pprint import pprint

import example.min_tree as example
import example.state_machine as state_example
import example.calc as calc_example


def display_help():
    pprint("Possible args -- test, example, help")
    pprint("test -- Run tests")
    pprint("exampletree -- run example Min Tree in example folder")
    pprint("examplestate -- run example State Machine in example folder")
    pprint("examplecalc -- run example Calc in example folder")
    pprint("help -- Diplsay this text")


if len(sys.argv) != 2:
    display_help()
else:
    first_arg = sys.argv[1]

    if first_arg == 'test':
        import subprocess
        subprocess.Popen("pytest")

    elif first_arg == 'exampletree':
        example.run_example()

    elif first_arg == 'examplestate':
        state_example.run_example()

    elif first_arg == 'examplecalc':
        calc_example.run_example()

    elif first_arg == 'help':
        display_help()
    else:
        display_help()
