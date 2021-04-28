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
    let a = in<i32>();
    a=5;
    let rec = rectangle<i32>(52, 65i32); //52 and 65i32 are i32 literals
    let ar = area(rec);
    let t = heap_alloc<rectangle<i32>>(1, 5);
    //heap_free(t);
    let tred = cast<i16>(32);
    rectangle<i32>(5, 3);
}
