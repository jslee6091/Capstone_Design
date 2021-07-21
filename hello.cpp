#include <iostream>

using namespace std;

int main(int argc, char* argv[]){
    std::cout << "hello world" << std::endl;
    int number;
    // cin과 cout은 std를 선언해주거나 std::cout 이렇게 사용해야 한다.
    cin >> number;
    cout << number << "\n";
    printf("hello!!\n");
    return 0;
}
