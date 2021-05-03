class InferenceError(Exception):
    pass


class TypeGenError(InferenceError):
    """
    This type of error is used by type generators 
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


# choice errors

class ChoiceSkipError(InferenceError):
    pass
