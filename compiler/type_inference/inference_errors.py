class InferenceError(Exception):
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
