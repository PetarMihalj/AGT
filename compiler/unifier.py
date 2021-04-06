# https://blog.witchoflight.com/2020/syntactic-unification/

from dataclasses import dataclass
import parser_rules as pr
import typesystem as ts


def unify_struct(source, target, env):
    if type(source) != type(target):
        return False
    if type(source) == pr.IdTypeIdentifier:
        if pr.IdTypeIdentifier.name in env:



if __name__ == '__main__':
    source = pr.IdParametersTypeIdentifier(
        pr.IdTypeIdentifier("vector"),
        [pr.IdTypeIdentifier("i32")]
    )
    target = pr.IdParametersTypeIdentifier(
        pr.IdTypeIdentifier("vector"),
        [pr.IdTypeIdentifier("A")]
    )

    env = {
        "i32": ts.IntType(32, True),
    }
