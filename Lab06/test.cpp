#include <iostream>

using namespace std;

int main() {
    int a[8];
    int b[8];

    for (int i = 0; i < 8; i++) {
        a[i] = i;
        b[i] = i;
    }

    cout << a[8+32] << endl;

    return 0;
}