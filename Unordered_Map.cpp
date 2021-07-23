#include <iostream>
#include <unordered_map>

using namespace std;

int main(){
    unordered_map<int, int> umap;

    // 비어있는지 확인
    if (umap.empty()){
        cout << "unordered_map is empty" << endl;
    }

    // 요소 추가
    umap.insert({4,5});
    umap.insert(make_pair(5,6));
    umap[8] = 10;

    // 전체 요소 출력
    for(auto num : umap){
        cout << num.first << " and " << num.second << endl;
    }

    // 크기 구하기
    cout << "umap size is " << umap.size() << endl;

    // 특정 key에 대한 value 구하기
    auto val = umap.find(8);
    cout << "value of 8 is " << val->second << endl;
    cout << "val->first is " << val->first << endl;

    // 특정 요소 지우기
    for(pair<int,int> pmap : umap){
        if (pmap.first == 5){
            umap.erase(5);
        }
    }

    for(auto num : umap){
        cout << num.first << " and " << num.second << endl;
    }
}