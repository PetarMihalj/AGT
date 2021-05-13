from subprocess import Popen, PIPE
import subprocess
from os import pipe
import os
import tempfile

import click

from .lexing import get_tokens
from .syntax_parsing import get_syntax_ast
from .semantics_parsing import get_semantics_ast
from .code_generation import get_code

# ---------------------------------------------------------------------

def tree_print_r(name, obj, prefix, ofile):
    if name is None:
        print(f"{prefix} ", end='', file=ofile)
    else:
        print(f"{prefix} {name} = ", end='', file=ofile)

    if hasattr(obj, "__dict__"):
        print(f"{type(obj).__name__}(", file=ofile)
        for k, v in obj.__dict__.items():
            if k not in ["linespan", "lexspan"]:
                tree_print_r(k, v, prefix+" - ", ofile)
        print(f"{prefix} )", file=ofile)
    elif type(obj) == list:
        print("[", file=ofile)
        for i in obj:
            tree_print_r(None, i, prefix+" - ", ofile)
        print(f"{prefix} ]", file=ofile)
    elif type(obj) == dict:
        print("{", file=ofile)
        for k,v in obj.items():
            tree_print_r(k, v, prefix+" - ", ofile)
        print(prefix+" }", file=ofile)
    else:
        print(f"{type(obj).__name__}({obj})", file=ofile)


def tree_print(obj, ofile):
    tree_print_r(None, obj, "", ofile)

# ---------------------------------------------------------------------

@click.group()
def cli_entry():
    pass


@cli_entry.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w', ))
def lex_gen(input_file, output_file):
    data_in = input_file.read()
    tokens = get_tokens(data_in)

    for l in tokens:
        output_file.write(str(l))
        output_file.write('\n')

@cli_entry.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w', ))
def syntax_gen(input_file, output_file):
    data_in = input_file.read()
    tree_syn = get_syntax_ast(data_in)
    tree_print(tree_syn, output_file)

@cli_entry.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w', ))
def semantics_gen(input_file, output_file):
    data_in = input_file.read()
    tree_syn = get_syntax_ast(data_in)
    tree_sem = get_semantics_ast(tree_syn)
    tree_print(tree_sem, output_file)


@cli_entry.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_file', type=click.File('w', ))
@click.option('--optimize', is_flag=True)
def llvm_gen(input_file, output_file, optimize):
    data_in = input_file.read()
    syntax_ast = get_syntax_ast(data_in)
    semantics_ast = get_semantics_ast(syntax_ast)
    code = get_code(semantics_ast)

    r,w = pipe()
    p_llvm_i = os.fdopen(w, 'w')
    for l in code:
        p_llvm_i.write(l)
        p_llvm_i.write('\n')
    p_llvm_i.close()

    if optimize:
        with os.fdopen(r, 'r') as fl:
            llvm_proc = subprocess.run(f"opt -S -O3 - -o -", shell=True, check=True, 
                    stdin=fl,
                    stdout=output_file
            )
    else:
        with os.fdopen(r, 'r') as fl:
            output_file.write(fl.read())


@cli_entry.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_path', type=click.Path())
def binary_gen(input_file, output_path):
    binary_gen_stub(input_file, output_path)

def binary_gen_stub(input_file, output_path):
    data_in = input_file.read()
    syntax_ast = get_syntax_ast(data_in)
    semantics_ast = get_semantics_ast(syntax_ast)
    code = get_code(semantics_ast)

    r,w = pipe()
    p_llvm_i = os.fdopen(w, 'w')
    for l in code:
        p_llvm_i.write(l)
        p_llvm_i.write('\n')
    p_llvm_i.close()

    with os.fdopen(r) as p_llvm_o:
        tf = tempfile.NamedTemporaryFile(suffix=".o")
        llvm_proc = subprocess.run(f"llc -O3 -filetype=obj -", shell=True, check=True, stdin=p_llvm_o, stdout=tf)
        gcc_proc = subprocess.run(f"gcc -no-pie {tf.name} -o {output_path}", shell=True, check=True, stdin=tf)

