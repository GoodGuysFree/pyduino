#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import sys
import ast
from pprint import pprint

from generate_pass import GeneratePass
from symbol_pass import SymbolPass


def generate(source, outfile=None):
    if outfile is None:
        outfile = sys.stdout

    text = source.read()
    tree = ast.parse(text)

    lines = text.splitlines()
    symbols = SymbolPass(tree, lines)
    # symbols.report()

    GeneratePass(symbols, tree, outfile, lines)


def main():
    with open(sys.argv[1], "r") as source:
        generate(source)


if __name__ == "__main__":
    main()
