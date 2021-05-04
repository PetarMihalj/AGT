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


class TypeExpressionError(InferenceError):
    pass

class RuntimeExpressionError(InferenceError):
    pass

class NameError(InferenceError):
    pass


