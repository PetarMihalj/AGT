#!/bin/bash

python -m compiler.code_gen $1 | tee tmp | nl -ba -
lli tmp
es=$?

echo
echo "Exit status: $es"
