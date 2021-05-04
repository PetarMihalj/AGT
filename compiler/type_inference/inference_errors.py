class InferenceError(Exception):
    pass


class TypeGenError(InferenceError):
    """
    This type of error is used by type generators 
    to indicate they haven't been successful
    """
    pass

class ChoiceSkipError(InferenceError):
    """
    This type of error is used by enable_if and enable_if_resolve
    to indicate they haven't been successful
    """
    pass

# crashing errors

class CrashingError(InferenceError):
    pass

class TypeExpressionError(CrashingError):
    pass

class RuntimeExpressionError(CrashingError):
    pass

class NameError(CrashingError):
    pass


