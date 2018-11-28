import sys

def display_help():
    print("showing help")

if len(sys.argv) != 2:
    display_help()
else:
    first_arg = sys.argv[1]

    if first_arg == 'test':
        import pytest
        pytest.main()

    elif first_arg == 'example':
        print("running example")

    elif first_arg == 'help':
        display_help()
    else:
        display_help()
