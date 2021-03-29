#include <bits/stdc++.h>
using namespace std;

template <typename T>
T sum(int n, T acc){
    if (n==0)  return acc;
    return sum(n-1, acc+n);
}

int main(){
    cout << sum(5,0ll) << endl;
}
