## AGT programming language

AGT was developed as my master thesis project.

AGT is a compiled programming language with a strong and static type system, with the following features:

- Lifetime semantics (initialization, copying and destruction of objects)
- Parametric polymorphism
- Compile time compilation
- Custom operators

Detailed information on AGT (including examples) can be found in my [master thesis](https://github.com/PetarMihalj/AGT/blob/master/AGT_master_thesis.pdf).

# Example program

This program will compute 12th Fibonacci number in compile time.

```
struct fib<T> -> i1{
    type _ = enable_if<T == i1>;
}
struct fib<T> -> i1{
    type _ = enable_if<T == i2>;
}

struct fib<T> -> R{
    type _ = enable_if<T != i1>;
    type _ = enable_if<T != i2>;
    type R = fib<T-i1>+fib<T-i2>;
}

fn main() -> i32{
    out(type_to_value<fib<i12>, i32>());
    return 0;
}
```

Output: `144`

Other examples can be found in `e2e` folder.

# Installation guide

AGT reference compiler (AGTC) has been tested on Arch Linux (kernel version 5.12.5), along with LLVM11 and GCC11.

1. Ensure the requirements are satisfied
2. Clone the repo and position yourself in it
3. `pip install .`
4. Run the tests with `pytest e2e`
5. Use the compiler with `python3 -m agtc` (will list the options).
