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
def llvm_gen(input_file, output_file):
    data_in = input_file.read()
    syntax_ast = get_syntax_ast(data_in)
    semantics_ast = get_semantics_ast(syntax_ast)
    code = get_code(semantics_ast)

    for l in code:
        output_file.write(l)
        output_file.write('\n')


@cli_entry.command()
@click.argument('input_file', type=click.File('r'))
@click.argument('output_path', type=click.Path())
def binary_gen(input_file, output_path):
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

    p_llvm_o = os.fdopen(r)
    tf = tempfile.NamedTemporaryFile(suffix=".o")

    llvm_proc = subprocess.run(f"llc -filetype=obj -", shell=True, check=True, stdin=p_llvm_o, stdout=tf)
    gcc_proc = subprocess.run(f"gcc -no-pie {tf.name} -o {output_path}", shell=True, check=True, stdin=tf)
