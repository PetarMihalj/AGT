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


int main(){
    int ps = sizeof(char*);
    int* a = (int*) malloc(sizeof(int) * 3);
    free(a);
    int b=5;
    int c=10;
    int d =copy(&b, &c);

    struct rect r;
    

}
