//
// compile time computation example
//

// if they arent equal, division by _1 crashes
// this nondeterministic branch

struct assert_equal<A,B>{
    type _1 = A == B;
    type _2 = i1 / _1;
}

struct assert_not_equal<A,B>{
    type _1 = A != B;
    type _2 = i1 / _1;
}

struct fib<T>{
    type _1 = assert_equal<T, i1>;
    type t = i1;
}
struct fib<T>{
    type _1 = assert_equal<T, i2>;
    type t = i1;
}

struct fib<T>{
    type _1 = assert_not_equal<T, i1>;
    type _2 = assert_not_equal<T, i2>;
    type t = fib<T-i1>.t+fib<T-i2>.t;
}

// notice the i32 parametrized constructor
// that one creates an i32 with default value equal to parameter
fn ct_fib<T>() -> i32{
    type f = fib<T>.t;
    let value = i32<f>();
    return value;
}

fn main(){
    main();
    let v = ct_fib<i5>();
}
