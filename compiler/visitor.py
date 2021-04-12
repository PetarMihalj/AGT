class Visitor():
    def __init__(self):
        self.dict = {}

    def add(self, cl):
        def callback(f):
            self.dict[cl] = f
        return callback

    def visit(self, obj, *vargs, **kwargs):
        return self.dict[type(obj)](obj, *vargs, **kwargs)
