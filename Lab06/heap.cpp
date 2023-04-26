#include <stdlib.h>

int main(int argc, char **argv){
  int *array = new int[100];
  array[100] = 0; // BOOM
  int res = array[argc + 100];  // BOOM
  delete [] array;
  return res;
}
