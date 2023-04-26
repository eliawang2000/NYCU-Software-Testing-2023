#include <iostream>
#include <cstdlib>

using namespace std;
int num[5]; 
int main() {
    
    for (int i = 0; i <= 5; i++) {
        num[i] = i; // i = 5, BOOM
    }

    cout << num[6] << endl; // BOOM

    return 0;
}