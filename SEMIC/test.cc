#include <string>
#include <iostream>
#include "sha1.h"
using namespace std;

void brute_force( string str, string res ) {
      
      if (sha1(res) == "b8e46064c5cb98321ab378f546d2641881b43563") {
		cout << "Match found: "  << res << endl;
            return;
      }
      for( int i = 0; i < str.length(); i++ )
            brute_force( string(str).erase(i,1), res + str[i] );
}

int main( int argc, char **argv) {
      string str = "gGmMcC5031";
      brute_force( str, "" );  
      return 0;
}