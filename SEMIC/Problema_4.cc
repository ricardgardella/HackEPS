#include <iostream>
#include <algorithm>
#include "sha1.h"

using namespace std;

	
int main() {
	string choice = "gGmMcC5%0=3·1!";
	while (next_permutation(choice.begin(), choice.end())) {

		cout << choice  << ": " << sha1(choice)<< endl;
		if (sha1(choice) == "b8e46064c5cb98321ab378f546d2641881b43563") {
			cout <<"PEDO" << endl;
			return 0;
		}
	}
}