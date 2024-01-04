
import time
import pyautogui

# def main():
#     print("클릭 이벤트를 감지하고 좌표를 출력합니다. 종료하려면 Ctrl+C를 누르세요.")
#     try:
#         while True:
#             time.sleep(5)
#             x, y = pyautogui.position()
#             print(f'현재 마우스 위치: x={x}, y={y}', end='\r')
#     except KeyboardInterrupt:
#         print('프로그램을 종료합니다.')

# if __name__ == "__main__":
#     main()



#계정선택버튼

#add account

#add a new account

#생성

#주소복사 클릭

#메모장클릭

#엔터

#ctrl v

# 클릭할 좌표 리스트
click_coordinates = [
    (2915, 387),
    (2856, 1948),
    (2797, 408),
    (3051, 542),
    (2876, 472),
    (1692, 26)
]

def main():
    try:
        print("클릭할 좌표를 순서대로 클릭합니다. 프로그램을 종료하려면 Ctrl+C를 누르세요.")
        time.sleep(1)  # 1초 동안 대기
        for x, y in click_coordinates:
            pyautogui.click(x, y)
            print(f'클릭한 좌표: x={x}, y={y}')
            time.sleep(1)  # 클릭 사이에 1초의 딜레이 추가

        pyautogui.press('enter')
        time.sleep(1)  # 1초 대기

        # 붙여넣기 (Ctrl + V)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1) 
    except KeyboardInterrupt:
        print('프로그램을 종료합니다.')

if __name__ == "__main__":
    for i in range(200):
        main()