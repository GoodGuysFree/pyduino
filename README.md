pytoc
=====

Intro
-----
A rudimentary Python-to-C converter for Arduino projects.

Usage
-----
Use chmod +x on parser.py, then run ./parser.py with test.py as argument

Known Limitations
=================
Partial list of limitations:

1. No string variable support, only constants
1. No dictionary support
1. Lists and tuples only work when all elements are of the same type
1. if / else, and for / while do not work yet
1. Advanced operators like += / -= don't work
1. Boolean support is in its infancy
1. Many more not known yet
