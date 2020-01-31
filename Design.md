Design Document
===============
Purpose
-------
The purpose of this project is to create a translator from a subset of Python language to
C in a form that will be usable in the [Arduino](https://www.arduino.cc/) IDE to compile
and download a sketch to an Arduino board.

Concept
-------

Use Python's [Abstract Syntax Tree - AST](https://docs.python.org/3/library/ast.html)
parser, and write a simple mechanism to walk the tree, and generate C code.

Design
------

The code will implement two different tree-walking classes, effectively becoming a 2-pass
translator. The first one will be in charge of creating a symbol table that will be used
by the second pass to emit local variable declarations at the head of functions.

### Scope

During each pass, a simple list will be used keep track of the current scope.
The list begins empty, and when a function is entered, we append the function name to the
list. When the function ends, we remove that function name from the end of the list.
A scope is then simply the names of the scope elements, in a list. It representation
will use the standard `::` to connect elements. For example, consider this code fragment:

    #!/usr/bin/python
    var1 : int = 0
    
    def func(arg1: int):
        result = var1 + arg1
        return result
        
Here are the fully qualified scoped-names of the symbols in the above fragment:

    | Code Line            | Symbol  | Scoped Symbol  |
    |----------------------|---------|----------------|
    | var1 : int = 0       | var1    | var1           |
    | def func(arg1: int): | func    | func           |
    | def func(arg1: int): | arg1    | func::arg1     |
    | result = var1 + arg1 | result  | func::result   |

### Variable Types - First Pass
In the first implementation, only integers will be supported. During the first pass,
we take extra care to notice assignments, function arguments, as well as annotated
assignments and annotated function arguments. We record the variable and its
type from the annotation, as well as the scope where it is defined. If we encounter the
`global` keyword, those variables are checked to see they exist in the global scope
and if they do, we do not add them as new variables in the function's scope.

By the end of the first pass, we should have a dictionary, whose key is a scope (the
global scope will use the empty string as the key), and the value is the list of symbols
known at this scope. This list of symbols will include the symbol's complete scope, so
that a global variable will appear un-scoped in this list.

### Handling Variables with Unknown Types
Hopefully, we write good code and annotate our types. However, we can find the type from the
type of the value being assigned, in assignments. For function arguments, we know about the 
argument on top but if it is not annotated, we will add the type in a lazy fashion, at a
later time, i.e. when we see the first assignment to the variable.

### Second Pass - Generation
During the second pass, the first AST element we encounter is the Module. This lets us
add C `#include` directives, and emit declarations for all global variables. In this pass
we also track the scope we're in, in the same way as we do in the first pass.

The rest is TBW.
