fn fib(n) -> i32{
    type _1 = enable_if<n==i32>;

    if (n<=2){
        return 1;
    }
    else{
        return fib(n-1)+fib(n-2);
    }
}

fn main() -> i32{
    let v = fib(7);
    return v;
}
