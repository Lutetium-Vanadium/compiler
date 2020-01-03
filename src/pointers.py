from _ctypes import PyObj_FromPtr

# Dereferences the pointer
def ptrVal(ptr):
    return PyObj_FromPtr(ptr)


# Makes a pointer reference
def ptr(obj):
    return id(obj)


# 'pointer' are essentially ints, this gives a better idea for the function arg types
pointer = int
