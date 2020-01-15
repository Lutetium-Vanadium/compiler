def execute(code_obj):
    """
    Function to execute code objects.
    Kept separate due to use of namespace by the code object
    """
    exec(code_obj)
