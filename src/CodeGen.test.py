from bytecode import Bytecode, Instr


def dumps(lst, indent=2):
    print("[")
    for i in lst:
        print(" " * indent, i, ",", sep="")
    print("]")


# bytecode = Bytecode()


def func(d, e, f):
    a = 231
    return d + e + f


# def f(web, df, sadas, asda):
#     from random import randint

#     a = 23
#     print(randint())

#     def b(d, e, f):
#         a = 231
#         return d + e + f

#     print(b(1, 2, 3))

#     return 0
# c = Bytecode.from_code(f.__code__)

d = Bytecode(
    [
        Instr("LOAD_FAST", "g"),
        Instr("LOAD_FAST", "f"),
        Instr("BINARY_ADD"),
        Instr("LOAD_FAST", "e"),
        Instr("BINARY_ADD"),
        Instr("RETURN_VALUE"),
    ]
)

d.argcount = 3
d.argnames = ["g", "e", "f"]

d.name = "d"

b = Bytecode(
    [
        Instr("LOAD_CONST", 0),
        Instr("LOAD_CONST", ("random",)),
        Instr("IMPORT_NAME", "random"),
        Instr("IMPORT_FROM", "random"),
        Instr("STORE_FAST", "random"),
        Instr("POP_TOP"),
        Instr("LOAD_CONST", 23),
        Instr("STORE_FAST", "a"),
        Instr("LOAD_GLOBAL", "print"),
        Instr("LOAD_FAST", "random"),
        Instr("CALL_FUNCTION", 0),
        Instr("CALL_FUNCTION", 1),
        Instr("POP_TOP"),
        Instr("LOAD_CONST", d.to_code()),
        Instr("LOAD_CONST", "f.<locals>.b"),
        Instr("MAKE_FUNCTION", 0),
        Instr("STORE_FAST", "b"),
        Instr("LOAD_GLOBAL", "print"),
        Instr("LOAD_FAST", "b"),
        Instr("LOAD_CONST", 1),
        Instr("LOAD_CONST", 2),
        Instr("LOAD_CONST", 3),
        Instr("CALL_FUNCTION", 3),
        Instr("CALL_FUNCTION", 1),
        Instr("POP_TOP"),
        Instr("LOAD_CONST", 0),
        Instr("RETURN_VALUE"),
    ]
)

b.name = "b"

# dumps(c, indent=2)

# print("\n\n--------------------------------\n\n")

exec(b.to_code())
