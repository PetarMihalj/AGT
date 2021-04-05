# https://blog.witchoflight.com/2020/syntactic-unification/

from dataclasses import dataclass

@dataclass(frozen=True)
class Var:
    name: str

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
class Struct:
    name: str

    def __repr__(self):
        return self.name


def walk(env, term):
    while term in env:
        term = env[term]
    return term


def unify(a, b, env={}):
    a = walk(env, a)
    b = walk(env, b)
    if a == b:
        return env
    if isinstance(a, Var):
        return {**env, a: b}
    if isinstance(b, Var):
        return {**env, b: a}
    if isinstance(a, tuple) and isinstance(b, tuple):
        if len(a) != len(b):
            return None
        for (a, b) in zip(a, b):
            env = unify(a, b, env)
            if env is None:
                return None
        return env
    return None
