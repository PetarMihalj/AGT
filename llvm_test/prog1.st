struct kvadrat<T>{
    T a;
    T b;
}

void __init__(kvadrat* this, int a, int b){
    this.a = a;
    this.b = b;
}

void __mul__(int a, int b){

}

int main(){
    int a = 5;
    int b = 10;
    kvadrat<int> kv(a,b);
    return kv.a * kv.b;
}
