//
// compile time computation example
//

struct fib<T>{
    type _1 = enable_if<T == i1>;
    type t = i1;
}
struct fib<T>{
    type _1 = enable_if<T == i2>;
    type t = i1;
}

struct fib<T>{
    type _1 = enable_if<T != i1>;
    type _2 = enable_if<T != i2>;
    type t = fib<T-i1>.t+fib<T-i2>.t;
}

fn ct_fib<T>() -> i32{
    type f = fib<T>.t;
    let value = type_to_value<f, i32>();
    return value;
}

fn main(){
    let v = ct_fib<i5>();
}
