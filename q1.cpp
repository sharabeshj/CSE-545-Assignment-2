#include<iostream>
using namespace std;

string encrypt(string plainText, int shift) {
    string encryptText = "";
    for (int i=0; i<plainText.length(); i++) {
        encryptText += char(int(plainText[i] + shift - 65)%26 + 65); // Handling upper case characters
    }
    return encryptText;
}

int main() {
    string plainText = "SAMPLETEXT";
    int shift = 4;
    cout<<"Plain Text : "<<plainText<<endl;
    cout<<"Shift : "<<shift<<endl;
    cout<<"Encrypted Text : "<<encrypt(plainText, shift);
    return 0;
}