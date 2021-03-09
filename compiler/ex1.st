int main(){

}

int fib(var n, var f1, var f2){
    if (n==1) return f1;
    return fib(n-1, f2, f1+f2);
}

