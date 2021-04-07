struct rectangle<T>{
    let a = T;
    let b = T;
}

struct assert_equal<A,B>{
    type _1 = A == B;
    type _2 = i1 / _1;
}

fn __init__(RTP this, T a, T b){
    //limit __init__ only to rectangle<T>
    type _is_rt = assert_equal<RTP, @rectangle<T>>;      

    this!.a = a;
    this!.b = b;
}

fn povrsina(KV k) -> T{
    type T = KV.T;
    type _is_kv = assert_equal<kvadrat<T>, KV>;

    return k.a * k.b;
}

fn main(){
    let kv = kvadrat<i32>(52, 65i32); //52 i 65i32 su i32 literali
    let pov = povrsina(kv);
}
