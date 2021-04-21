struct rectangle<T>{
    let a = T;
    let b = T;
}

struct assert_equal<A,B>{
    type _1 = A == B;
    type _2 = i1 / _1;
}

fn __init__(kvp, a, b){
    type _1 = assert_equal<kvp, @rectangle<a>>;      
    type _1 = assert_equal<kvp, @rectangle<b>>;      

    kvp!.a = a;
    kvp!.b = b;
}

fn __copy__(p1, p2){
    type _1 = assert_equal<p1,@rectangle<i32>>;
    type _2 = assert_equal<p2,@rectangle<i32>>;

    p1!.a = p2!.a;
    p1!.b = p2!.b;
}

fn area(kv) -> _inner{
    type _inner = kv.a;
    type _is_kv = assert_equal<kv, rectangle<_inner>>;

    return kv.a * kv.b;
}

fn main(){
    let rec = rectangle<i32>(52, 65i32); //52 and 65i32 are i32 literals
    let ar = area(rec);
}
