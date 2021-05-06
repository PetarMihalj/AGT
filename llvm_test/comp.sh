#!/bin/bash

clang -S -emit-llvm -O$2 $1 -o -
