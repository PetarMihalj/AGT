struct rectangle<T>{
    let a = T;
    let b = T;
}

fn area(r) -> T{
    type T = enable_if_resolve<r.T>;
    type _1 = enable_if<r==rectangle<T>>;

    return r.a * r.b;
}

fn main() -> i32{
    let a = in<i32>();
    let rec = rectangle<i32>(a, 3);
    let ar = area(rec);
    out(ar);
    return 0;
}