struct kvadrat<T>{
    T a;
    T b;
}

fn __init__<T>(kvadrat<T>* this, T a, T b) -> T{
    this.a = a;
    this.b = b;
}

//this is a comment


fn sum<T>(T a, T b) -> T{
    if (b==T{}){
        return a; 
    }
    return sum<T>(a+T{1},b-T{1});
}

fn __mul__(int a, int b){

}

/*
this is a multiline comment
and we cache it

*/

fn main(){
    let a = i32{5i32};
    let b = i32{10i32};
    let A = heap_alloc<i32>{};
    //i32[5] a;
    //i32 a[5];
    A[3];
    sum(2,3);
    let kv = kvadrat{a,b};
    return kv.a * kv.b;
}
