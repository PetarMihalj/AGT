## AGT programming language

AGT was developed in the course of one semester as my master thesis project.

AGT is a compiled programming language with a strong and static type system, with the following features:

- Lifetime semantics (initialization, copying and destruction of objects)
- Parametric Polymorphism
- Compile time compilation
- Custom operators

Detailed information can be found in this [file](https://github.com/PetarMihalj/AGT/blob/master/AGT_master_thesis.pdf).

# Installation guide

AGT reference compiler (AGTC) has been tested on Arch Linux (kernel version 5.12.5), along with LLVM11 and GCC11.

1. Ensure the requirements are satisfied
2. Clone the repo and position yourself in it
3. `pip install .`
4. Run the tests with `pytest e2e`
5. Use the compiler with `python3 -m agtc` (will list the options).
