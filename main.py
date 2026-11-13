# 나만의 퀴즈 게임 (Codyssey 미션 E1-2)
# 구조: Quiz(문제 하나) → QuizGame(게임 전체) → 도우미 함수 → 시작점


class Quiz:
    """퀴즈 한 문제: 질문, 보기 4개, 정답 번호(1~4)를 한 묶음으로 관리한다."""

    def __init__(self, question, choices, answer):
        self.question = question  # 질문 (str)
        self.choices = choices    # 보기 4개 (list of str)
        self.answer = answer      # 정답 번호 1~4 (int)

    def display(self, number):
        """문제 번호와 질문, 보기 4개를 출력한다."""
        print(f"[문제 {number}] {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답이면 True, 아니면 False."""
        return user_answer == self.answer


def create_default_quizzes():
    """처음 실행할 때 쓰는 기본 퀴즈 5개 (주제: 미션 1 복습 - 터미널·Docker·Git)."""
    return [
        Quiz("현재 작업 중인 폴더의 경로를 출력하는 명령어는?",
             ["ls", "pwd", "cd", "mkdir"], 2),
        Quiz("chmod 755를 적용했을 때 소유자(owner)가 가진 권한은?",
             ["읽기만", "읽기+쓰기", "읽기+쓰기+실행", "실행만"], 3),
        Quiz("docker run -p 8080:80 에서 8080은 어디의 포트인가?",
             ["컨테이너", "호스트(내 컴퓨터)", "Docker Hub", "이미지"], 2),
        Quiz("컨테이너를 삭제해도 데이터를 남기려면 무엇을 사용해야 하나?",
             ["Dockerfile", "docker logs", "Docker volume", "docker ps -a"], 3),
        Quiz("로컬의 commit 기록을 GitHub에 올리는 Git 명령어는?",
             ["git add", "git commit", "git push", "git pull"], 3),
    ]


class QuizGame:
    """게임 전체: 퀴즈 목록을 들고 있고, 메뉴의 각 기능을 method로 가진다."""

    def __init__(self):
        self.quizzes = create_default_quizzes()

    def run(self):
        """메뉴를 반복해서 보여주고, 고른 번호의 기능을 실행한다."""
        while True:
            show_menu()
            choice = read_number("선택: ", 1, 5)

            if choice == 1:
                self.play()
            elif choice == 2:
                print("[퀴즈 추가] 준비 중입니다.")
            elif choice == 3:
                print("[퀴즈 목록] 준비 중입니다.")
            elif choice == 4:
                print("[점수 확인] 준비 중입니다.")
            else:
                print("게임을 종료합니다.")
                break

    def play(self):
        """저장된 퀴즈를 차례로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return

        total = len(self.quizzes)
        correct = 0
        print(f"\n퀴즈를 시작합니다! (총 {total}문제)")

        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            user_answer = read_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("정답입니다!")
                correct += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

        score = correct * 100 // total
        print("=" * 40)
        print(f"결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print("=" * 40)


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
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")
