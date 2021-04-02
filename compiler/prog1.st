struct kvadrat{
    T a;
    i32 b;
}

void __init__(kvadrat* this, int a, int b){
    this.a = a;
    this.b = b;
}

//this is a comment

T sum(T a, T b){
    return a+b;
}

void __mul__(int* a, int** b){

}

/*
this is a multiline comment
and we cache it

*/

int main(){
    let a = i32{5i32};
    i32 b = 10i32;
    i32* A = heap_alloc();
    //i32[5] a;
    //i32 a[5];
    A[3];
    sum(2,3);
    kvadrat kv(a,b);
    return kv.a * kv.b;
}
