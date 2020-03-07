from __future__ import print_function

import argparse
import platform
import re
import sys

from . import convert_w, convert_u, convert_m, guess_converter

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert between Linux and Windows paths in WSL. "
            "If no converter is explicitely specified, an implicit one is "
            "deduced."))
    parser.add_argument("path", metavar="PATH")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-w", action="store_true",
        help=(
            "Print the Windows path equivalent to PATH, "
            "using backslashes"))
    group.add_argument(
        "-m", action="store_true",
        help=(
            "Print the Windows path equivalent to PATH, "
            "using forward slashes in place of backslashes"))
    group.add_argument(
        "-u", action="store_true",
        help="Print the Linux path equivalent to PATH")

    arguments = parser.parse_args()
    
    uname = platform.uname()
    if uname.system.lower() != "linux" or "microsoft" not in uname.release.lower():
        parser.error("wpc must be run inside WSL")

    converters = [
        x for x in vars(arguments)
        if x in ["w", "m", "u"] and getattr(arguments, x)]
    if not converters:
        converter = guess_converter(arguments.path)
    else:
        converter = globals()["convert_{}".format(converters[0])]

    print(converter(arguments.path))

if __name__ == "__main__":
    sys.exit(main())
