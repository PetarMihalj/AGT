#!/bin/bash

python -m compiler.code_gen $1 | tee tmp
lli tmp
es=$?

echo
echo "Exit status: $es"
