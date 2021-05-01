#include <stdlib.h>

int copy(int* a, int* b){
    *a = *b;
    return 1;
}

struct rect{
    int b;
    int a;
};

struct rect* alloc_i32(int size){
    struct rect* psInfo;
    int iSizeofStructure = (char*)(psInfo + 1) - (char*)(psInfo);
    return (struct rect*)malloc(iSizeofStructure * size);
}


int* m_func(char sz){
    return (int*) malloc(sizeof(int)*sz);
}
struct rect* test(struct rect* A, int off){
    return A+off;
}

int add(int a, int b){
    return a*b;
}

char addc(char a, char b){
    return a/b;
}

short adds(short a, short b){
    return a+b;
}

short subs(short a, short b){
    return a-b;
}

long long addl(long long a, long long b){
    return a%b;
}

int eq(int a, int b){
    return a==b;

}

void cpy(int* a, int* b){
    *a = *b;
}

int* fn_main(){
    int a = 3;
    a==a;
    return &a;
}

int main(){
    int* a = fn_main();
    struct rect b;
    int c = b.a;
}
