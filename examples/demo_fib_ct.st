//
// compile time computation example
//

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

fn ct_fib<T>() -> i32{
    type f = fib<T>;
    let value = type_to_value<f, i32>();
    return value;
}

fn main() -> i32{
    let v = ct_fib<i10>();
    return v;
}
