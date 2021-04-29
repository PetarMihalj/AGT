#include <stdlib.h>

int copy(int* a, int* b){
    *a = *b;
    return 1;
}

struct rect{
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
void test(){

}

int* fn_main(){
    int a = 3;
    test();
    return &a;
}

int main(){
    int* a = fn_main();
}
