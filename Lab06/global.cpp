#include <stdlib.h>
int global_array[10];
int main(int argc, char **argv){
//   return global_array[argc + 100];  // BOOM
    global_array[10] = 0; // out-of-bounds write
    int x = global_array[11]; // out-of-bounds read
    return 0;
}