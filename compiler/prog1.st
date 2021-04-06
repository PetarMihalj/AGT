//
// simple example with recursion
//

struct kvadrat<T>{
    let a = T;
}

fn __init__<KVTP, T, A>(KVTP this, T a, T b){
    type _is_kvtp = (KVTP!).T == kv;
    
    this.a = a;
    this.b = b;
}

fn sum<T>(T a, T b) -> T{
    return sum<T>(a+T(1),b-T(1));
}

fn main(){
    let kv = kvadrat(52, 65); //52 i 65 su i32 literali
    let poluopseg = sum(kv.a, kv.b);
}

//
// computation example
//

struct fib<T>{
    type _1 = assert<T, i1>;
    let t = i1;
}
struct fib<T>{
    type _1 = assert<T, i2>;
    let t = i1;
}

struct fib<T>{
    type t = add<sub<T, i1>.t, sub<T, i2>.t>.t;
}

fn main(){
    let v = t_to_value<fib<i5>, i32>();
}


//
// vector example
//


// signature cant contain field indexing
struct vector<V,A>{
    let v = V;
}

fn __init__<V,A>(A this, V value){
    (this!).v = value;
}

fn main(){
    let a = vector<i32, i128>(52);
}

//
// units example
//

struct kg{;}

struct Wrapped<U, V>{
    let value = V;
}

fn __sub__<U,V>(WUV v1, WUV v2) -> WUV{
    return WUV(v1.value - v2.value);
}

fn __init__<U,V>(WUV v1, V value){
    (v1!).value = value;
}

fn main(){
    let petar  = Wrapped<kg, i32>(85);
    let suzana = Wrapped<kg, i32>(60);
    let diff = petar - suzana;
}
