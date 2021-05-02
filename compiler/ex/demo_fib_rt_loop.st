fn fib(n) -> i32{
    type _1 = enable_if<n==i32>;
    let f1 = 1;
    let f2 = 1;
    let fb = 0;

    for (n=n-1;n>!0; n=n-1;){
        fb = f2;
        f2 = f1 + f2;
        f1 = fb;
    }
    return f1;
}

fn main() -> i32{
    let n = in<i32>();
    let f = fib(n);
    out(f);
    return 0;
}
