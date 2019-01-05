#include <iostream>
using namespace std;

int howMany7(int val) {
    int count = 0;
    while (val > 0) {
        if (val%10 == 7) ++count;
        val /= 10;
    }
    return count;
}

int main() {
    int n, val, res, seconds;
    cin >> n;
    for (int i = 1; i <= n; ++i) {
        seconds = 1;
        cin >> val;
        while (val > 100) {
            res = (val % 10) * 2;
            val = val / 10;
            val -= res;
            ++seconds;
            seconds += howMany7(val);
        }
        cout << "Case #" << i << ": " << seconds << endl;
    }
}