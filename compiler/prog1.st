//
// simple example with recursion
//

struct kvadrat<T>{
    T a;
    T b;
}

fn __init__<T>(kvadrat<T>* this, T a, T b) -> T{
    this.a = a;
    this.b = b;
}

fn sum<T>(T a, T b) -> T{
    let a = T{}; 
    if (b==T{}){
        return a; 
    }
    return sum<T>(a+T{1},b-T{1});
}

fn main(){
    let kv = kvadrat{52, 65}; //52 i 65 su i32 literali
    let poluopseg = sum(kv.a, kv.b);
}


//
// computation example
//

struct fib<spec T = i1>{
    T t;
}

struct fib<spec T = i2>{
    T t;
}

struct fib<T>{
    add<sub<T, i1>.t, sub<T, i2>.t>.t t;
}

fn main(){
    let v = type_to_value<fib<i5>, i32>{};
}


//
// vector example
//

struct vector<V,A = allocator<V>>{
    V v;
}

fn __init__<V,A>(vector<V,A>* this, V value){
    (*this).v = value;
}

fn main(){
    let a = vector<i32, i128>{52};
}

//
// units example
//

struct kg{}

struct Wrapped<U, V>{
    V value;
}

fn __sub__<U,V>(Wrapped<U,V>* v1, Wrapped<U,V> v2) -> Wrapped<U,V>{
    return Wrapped<U,V>{v1.value - v2.value};
}

fn __init__<U,V>(Wrapped<U,V>* v1, V value){
    (*v1).value = value;
}

fn main(){
    let petar  = Wrapped<KG, i32>{85};
    let suzana = Wrapped<KG, i32>{60};
    let diff = petar - suzana;
    let a = <Wrapped<KG, i32*>*>{1};
}

