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

    this!.a = a;
    this!.b = b;
}

fn __copy__(p1, p2){
    type _1 = assert_equal<p1,@rectangle<i32>>;
    type _2 = assert_equal<p2,@rectangle<i32>>;

    __copy__(@(p1!.a), @(p1!.a));
    __copy__(@(p1!.b), @(p1!.b));
}

fn povrsina(kv) -> _inner{
    type _inner = kv.a;
    type _is_kv = assert_equal<kv, rectangle<_inner>>;

    return kv.a * kv.b;
}

fn main(){
    let kv = kvadrat<i32>(52, 65i32); //52 i 65i32 su i32 literali
    let pov = povrsina(kv);
}
