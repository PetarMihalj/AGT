struct rectangle<T>{
    let a = T;
    let b = T;
}


fn area(kv) -> _inner{
    type _inner = kv.a;
    type _is_kv = enable_if<kv== rectangle<_inner>>;

    return kv.a * kv.b;
}

fn main(){
    let rec = rectangle<i32>(52, 65i32); //52 and 65i32 are i32 literals
    let ar = area(rec);
}
