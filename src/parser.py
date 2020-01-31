#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import sys
import ast
from pprint import pprint

from symbol_pass import SymbolPass


def generate(source):
    tree = ast.parse(source.read())

    symbols = SymbolPass(tree)
    symbols.report()


def main():
    with open(sys.argv[1], "r") as source:
        generate(source)


if __name__ == "__main__":
    main()
