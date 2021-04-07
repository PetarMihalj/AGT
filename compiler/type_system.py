from dataclasses import dataclass
from typing import Tuple
import re
from dataclasses import dataclass
import parser_rules as pr







# AUTO GENERATED TYPES


def match_and_ret(s: str, p: str):
    r = re.compile(p)
    m = r.match(s)
    if m is None:
        return None
    else:
        return m.group()


def smt_bool(t: pr.TypeExpression):
    if not isinstance(t, pr.TypeExpressionGetStruct):
        return None
    t: pr.TypeExpressionGetStruct
    if len(t.typeParameters) > 0:
        return None

    m = match_and_ret(t.name, r'bool|boolean')
    if m is None:
        return None
    return BoolType()


def smt_int(t: pr.TypeExpression):
    if not isinstance(t, pr.TypeExpressionGetStruct):
        return None
    t: pr.TypeExpressionGetStruct
    if len(t.typeParameters) > 0:
        return None

    m = match_and_ret(t.name, r'i([0-9]+)')
    if m is None:
        return None
    return IntType(m.group(1), True)


def check_all(t):
    smt_collection = [smt_int, smt_bool]
    for s in smt_collection:
        res = s(t)
        if res is not None:
            return res
    return None
