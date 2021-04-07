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
// compile time computation example
//

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

func ct_fib<T>() -> i32{
    type f = fib<T>;
    let value = i32<f>(); 
    return value;
}

fn main(){
    let v = ct_fib<i5>();
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
