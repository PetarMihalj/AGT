struct kvadrat<T>{
    T a;
    i32 b;
}

void __init__(kvadrat* this, int a, int b){
    this.a = a;
    this.b = b;
}

//this is a comment

T sum<T>(T a, T b){
    return a+b;
}

void __mul__(int* a, int** b){

}

/*
this is a multiline comment
and we cache it

*/

int main(){
    i32 a = 5i32;
    i32 b = 10i32;
    i32* A = heap_alloc();
    //i32[5] a;
    //i32 a[5];
    A[3];
    sum<int>(2,3);
    kvadrat<int> kv(a,b);
    return kv.a * kv.b;
}
