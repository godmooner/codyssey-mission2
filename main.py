# 나만의 퀴즈 게임 (Codyssey 미션 E1-2)
# 흐름: 메뉴 보여주기 → 번호 입력받기 → 고른 기능 실행 → 다시 메뉴 (5번이면 종료)


def main():
    """게임 전체 흐름을 담당한다."""
    while True:
        show_menu()
        choice = read_number("선택: ", 1, 5)

        if choice == 1:
            print("[퀴즈 풀기] 준비 중입니다.")
        elif choice == 2:
            print("[퀴즈 추가] 준비 중입니다.")
        elif choice == 3:
            print("[퀴즈 목록] 준비 중입니다.")
        elif choice == 4:
            print("[점수 확인] 준비 중입니다.")
        else:
            print("게임을 종료합니다.")
            break


def show_menu():
    """메뉴 화면을 출력한다."""
    print("=" * 40)
    print("나만의 퀴즈 게임")
    print("=" * 40)
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 점수 확인")
    print("5. 종료")
    print("=" * 40)


def read_number(prompt, min_value, max_value):
    """min_value ~ max_value 사이의 정수가 들어올 때까지 다시 묻는다."""
    while True:
        text = input(prompt).strip()

        # 1) 빈 입력
        if text == "":
            print("입력이 비어 있습니다. 숫자를 입력하세요.")
            continue

        # 2) 숫자로 바꿀 수 없는 입력 (예: abc)
        try:
            number = int(text)
        except ValueError:
            print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        # 3) 범위 밖 숫자 (예: 메뉴에서 9)
        if number < min_value or number > max_value:
            print(f"잘못된 입력입니다. {min_value}-{max_value} 사이의 숫자를 입력하세요.")
            continue

        return number


# 이 파일을 직접 실행했을 때의 시작점
if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
