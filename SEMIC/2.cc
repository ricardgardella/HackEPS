#include <iostream>
#include <vector>
#include <cmath>

#include "bigint.cc"

using namespace std;

typedef vector<bigint> VBI;

int main() {
    int n = 5;
    bigint count = 0;

    VBI Vk(n + 1, 0);
    VBI* current = &Vk;

    VBI Vk_1(n + 1, 0);
    Vk_1[0] = 1;
    VBI* previous = &Vk_1;

    VBI* aux;

    for (int k = 1; k <= n; ++k) {
        cout << "k: " << k << " -> ";
        for (int j = 1; j <= n; ++j) {
            (*current)[j] = (*previous)[j - 1] + (j - k >= 0 ? (*current)[j - k] : 0);
            cout << (*current)[j];
        } cout << endl;
        count += (*current)[n];
        
        aux = current;
        current = previous;
        previous = aux;
    }
    cout << "Case #10000000: " << count << endl;
 
    // cout << "Case #10000000: " << pow(1.0/(4.0*n*sqrt(3)), M_PI*sqrt(2*n/3.0)) << endl;
}