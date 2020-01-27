#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import sys
import ast
from pprint import pprint

from first_pass import FirstPass
from second_pass import SecondPass


def main():
    with open("test.py", "r") as source:
        tree = ast.parse(source.read())

    # First step - generate symbol tables, etc.
    #print("=== First Pass ===")
    first_pass = FirstPass()
    first_pass.visit(tree)
    #print("### Second Pass ###")
    second_pass = SecondPass(first_pass)
    second_pass.visit(tree)


if __name__ == "__main__":
    main()
