#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct{
    int a;
    int b;
} rect;

rect* al(int size){
    return (rect*) malloc(sizeof(rect)*size);
}

void init(rect* p, int a, int b){
    p->a = a;
    p->b = b;

}

void both(int a, int b){
    rect* r = al(1);
    init(r,a,b);
}

int main(){
    rect r;
}
