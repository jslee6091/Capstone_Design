#include <iostream>
#include <typeinfo>

using namespace std;

int main(int argc, char* argv[]){
    std::cout << "hello world" << std::endl;
    int number;
    // cin과 cout은 std를 선언해주거나 std::cout 이렇게 사용해야 한다.
    cin >> number;
    cout << number << "\n";
    printf("hello!!\n");
    cout << 5/2 << endl;
    cout << typeid(6/4).name() << endl;
    return 0;
}
