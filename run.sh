#!/bin/bash

for example in "$@"
do

python -m compiler.code_gen $example | tee tmp > /dev/null #| nl -ba -

echo ""
echo ""
echo ""
echo "---------------------"
echo "Program: $example"
cat tmp
echo ""
echo "---------------------"
echo "Program: $example"
echo ""
cat $example
echo "---------------------"
echo ""

lli tmp
es=$?
echo
echo "Exit status: $es"
read -p "Press any key to continue"
echo "---------------------"
#rm tmp


done

