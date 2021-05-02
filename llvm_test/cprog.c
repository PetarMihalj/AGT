#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void fr(int* a){
    free(a);
}

int main(){
    int* a = malloc(sizeof(int)*5);
    int* b = 0;
    fr(a);
}
