## Capstone Design Project

> Face Recognition Door Lock
>
> 2019.09 ~ 2020.06



#### Teammates & Role

- Park Joo Hyeong - Face Recognition Using Deep Learning
- Han Ji Ah - Firebase & Android Programming
- Seo Deuk Hwa - Python GUI Programming(Random Keypad)



#### My Role

- Door Lock Control Using `Raspberry Pi` and `Arduino`
- Raspberry Pi는 도어락의 얼굴인식 or 비밀번호 입력 성공 여부를 Arduino로 전달
- Arduino는 Raspberry Pi에서 전송된 데이터와 조도센서, 스위치의 정보에 따라 도어락 모터 제어



### Source Code

1. `pyqt.py` = Seo Deuk Hwa, Park Joo Hyeong
2. `functions.py` , `face_classification.py`  = Park Joo Hyeong



#### My Code

- `arduino_code.ino`
- `pyqt.py`
  - `check_password` function
    - `self.ser.write(str(int(self.pnp)).encode())` : Sends data to Arduino





