# Codyssey Mission E1-2 — 나만의 퀴즈 게임

## 1. 프로젝트 개요

Python으로 만든 터미널 퀴즈 게임이다. 메뉴에서 번호를 고르면 퀴즈 풀기, 문제 추가, 목록 확인, 최고 점수 확인을 할 수 있다.

퀴즈 주제는 미션 1에서 배운 터미널·Docker·Git 복습으로 정했다. 이미 배운 내용을 문제로 만들면 퀴즈 게임을 만들면서 이전 미션도 같이 복습할 수 있기 때문이다. 기본 문제는 5개다.

- 환경: macOS, Apple Silicon, VS Code, 터미널
- 확인한 버전: Python 3.14.7, Git 2.50.1
- Python 3.10 이상에서 실행하며, 외부 라이브러리는 사용하지 않는다.
- 저장소: https://github.com/godmooner/codyssey-mission2

## 2. 실행 방법

`main.py`가 있는 폴더에서 실행한다.

```bash
python3 main.py
```

| 번호 | 기능 |
| --- | --- |
| 1 | 등록된 퀴즈를 순서대로 풀고 결과 확인 |
| 2 | 질문, 선택지 4개, 정답 번호를 입력해서 문제 추가 |
| 3 | 등록된 문제의 번호와 질문 확인 |
| 4 | 최고 점수 확인 |
| 5 | 저장 후 종료 |

## 3. 수행 체크리스트

- [x] 메뉴 출력, 번호 선택, 종료
- [x] 빈 입력, 문자 입력, 범위 밖 숫자 처리
- [x] `Quiz`, `QuizGame` 클래스로 역할 나누기
- [x] 기본 퀴즈 5개 작성
- [x] 퀴즈 풀기, 추가, 목록, 최고 점수 확인
- [x] `state.json` 저장·불러오기
- [x] 파일이 없거나 손상되었을 때 기본 데이터로 실행
- [x] Ctrl+C, 입력 중단, 파일 읽기·쓰기 오류 처리
- [x] `feature-play` 브랜치에서 작업한 뒤 `main`에 병합
- [x] 의미 있는 커밋 10개 이상 확인
- [x] 별도 폴더에서 clone 후 변경·push, 원래 폴더에서 pull
- [x] 제출용 스크린샷 정리

## 4. 코드 흐름 공부 메모

### 4.1 시작점과 게임 준비

```python
if __name__ == "__main__":
```

이게 `main.py`를 실행하면 파이썬이 `__name__`에 `"__main__"`이라는 값을 넣음. 그래서 조건이 만족되어서 다음 코드로 넘어감. 쉽게 말해 아래 게임 시작 코드가 실행됨.

이어서 `game = QuizGame()`이 실행되고, `QuizGame`의 `__init__()`을 돌림.

```python
def __init__(self):
    self.quizzes = create_default_quizzes()
    self.best_score = None
    self.load()
```

**create_default_quizzes()**

얘는 그냥 질문, 선택지, 정답 번호를 넣은 `Quiz` 객체 5개를 목록에 담아서 결과로 주는 함수.

여기서 기본 문제를 만들기 때문에 `QuizGame()`을 호출할 때 별도로 넘길 값이 필요 없다.

여기까지 하면 `self.quizzes`에 문항 5개가 들어가 있는 상태다. 이후 `self.load()`로 저장된 파일을 확인한다. 정상적인 파일이 있으면 이전에 저장한 문제와 점수를 불러오고, 없으면 기본 문제를 그대로 사용한다.

이어서 `game = QuizGame()` 아래 있는 `game.run()`이 실행된다.

여기에 `try-except`가 붙는 이유는 유저가 Ctrl+C 같은 입력을 넣었을 때 예외 처리를 해주기 위함이다. 입력이 중단되면 가능한 범위에서 저장하고 종료한다.

### 4.2 run() — 메뉴 선택

기본적으로 `객체.메서드()` 이런 식으로 하면 객체에 이전에 정의한 메서드를 적용한다는 것이다.

`run()`은 입력을 받아서 그에 해당하는 화면으로 보내주는 역할을 한다.

유저가 선택할 수 있는 화면을 보여주는 `show_menu()`와, 입력한 번호를 저장하는 `choice = read_number("선택: ", 1, 5)`가 있다.

**show_menu()**

말 그대로 그냥 `print`로만 구성되어 문자만 표시해주는 화면이다.

**read_number()**

범위 내의 정수가 있을 때만 `int`로 된 번호를 통과시키고, 비어 있는 입력, 문자로 된 입력, 범위 밖의 입력을 받았을 때 안내 메시지를 출력하고 다시 입력받는 역할을 한다.

이후 정상적인 입력이 들어왔다면 선택한 번호에 따라 `self.play()`, `self.add_quiz()` 같은 메서드로 넘어간다. 각 기능이 끝나면 다시 메뉴로 돌아오고, 5번이면 종료한다.

여기서 `self`는 지금 메서드를 실행하고 있는 객체다. `self.quizzes`는 이 게임의 문제 목록이고, `self.play()`는 이 게임의 퀴즈 풀기 기능이다.

### 4.3 play() — 1. 퀴즈 풀기

우선 `self.quizzes`에 들어온 정보가 있는지부터 확인한다. 없으면 안내 후 리턴, 있으면 통과.

`correct = 0`으로 정의해서 맞은 문제를 세는 카운트로 사용한다.

`self.quizzes`에 있는 문제들을 `enumerate`를 이용해서 번호와 `Quiz` 객체로 하나씩 뽑아낸다.

```python
for number, quiz in enumerate(self.quizzes, start=1):
```

`start=1`은 문제 번호를 1부터 붙이기 위한 것이다. 없으면 0번부터 시작한다. 첫 번째 문제만 푼다는 뜻은 아니다.

각 퀴즈를 `quiz.display(number)`를 이용해서 출력한다.

**display()**

문제 번호와 질문, 선택지 4개를 출력해주는 메서드다. `print(f"...{변수}...")` 문법을 활용해서 만들었다.

이후 입력을 받는데, 여기서도 처음 메뉴에서와 마찬가지로 `read_number()`를 사용해서 입력 검사와 예외 처리를 한 차례 거친다. 숫자 입력을 받는 모든 곳에 적용한다고 생각하면 된다.

이후 간단한 `quiz.is_correct(user_answer)`로 맞았는지 확인한다. 맞으면 카운트를 더하고, 틀리면 정답 번호를 알려준다.

현재는 `user_answer == quiz.answer`로 직접 비교해도 같은 결과다. `quiz.answer`는 저장된 정답 값을 읽는 것이고, `quiz.is_correct(...)`는 메서드를 실행하는 것이다. 둘 다 점으로 접근하지만 메서드를 실행할 때는 괄호를 붙인다.

모든 문제를 풀면 최종 맞춘 개수를 백 점 만점으로 환산해서 출력한다.

```python
score = correct * 100 // total
```

### 4.4 add_quiz() — 2. 퀴즈 추가

새로운 문제를 추가하기 위해서는 `question`, `choices`, `answer`에 해당하는 각각의 값을 입력받아서 `Quiz(question, choices, answer)`로 묶어준 뒤, 기존 퀴즈 묶음이었던 `self.quizzes`에 `append`해주면 된다.

```python
self.quizzes.append(Quiz(question, choices, answer))
```

먼저 문제 객체를 만들고, 그다음 목록에 추가한다. 추가가 끝나면 `self.save()`로 저장한다.

**read_text()**

빈 문자열을 입력하면 값을 입력할 때까지 계속해서 물어본다. 앞뒤 공백도 제거한다.

정답 번호는 `read_number()`로 받아서 문자열이 아니라 정수로 저장한다.

### 4.5 list_quizzes() — 3. 퀴즈 목록

퀴즈의 목록을 확인하기 위해 번호와 `question`을 출력한다.

`display()`는 선택지까지 전부 출력한다는 점에서 차이점이 있다.

문제가 없으면 안내 후 `return`한다. 게임 전체가 종료되는 것이 아니라 목록 보기만 끝나고 메뉴로 돌아간다.

### 4.6 show_score() — 4. 점수 확인

`QuizGame`에 `self.best_score = None`이라는 속성을 추가했다. 아직 퀴즈를 풀지 않았다는 뜻이다. 풀었는데 0점인 경우와 구별하려고 `None`을 사용했다.

```python
if self.best_score is None or score > self.best_score:
```

이 조건으로 최고 기록을 갱신한다. 처음 푼 경우이거나 이전 점수보다 높으면 기록을 바꾸고 저장한다.

`or`는 앞의 조건이 참이면 뒤의 조건을 확인하지 않는다. 그래서 첫 플레이에서는 숫자와 `None`을 비교하지 않고 넘어간다.

`show_score()`에서는 `best_score`를 출력한다. 아직 기록이 없으면 먼저 퀴즈를 풀어보라는 안내가 나온다.

### 4.7 save() — 파일에 저장

기존에는 프로그램을 끄면 추가한 문제와 점수가 사라졌다. 실행 중인 객체 안에만 들어 있었기 때문이다.

`save()`는 문제마다 질문, 선택지, 정답 번호를 꺼내서 딕셔너리로 바꾼다. 그리고 문제 목록과 최고 점수를 `data` 하나에 묶는다.

```python
data = {
    "quizzes": quizzes,
    "best_score": self.best_score,
}
```

딕셔너리는 키와 값을 짝지어 저장한다. 여기서는 `"quizzes"`와 `"best_score"`가 값을 찾는 이름표인 키다. 첫 번째 값에는 문제 딕셔너리들의 목록이 들어가고, 두 번째 값에는 최고 점수가 들어간다.

`data["quizzes"][0]["question"]`이라고 쓰면 문제 목록에서 첫 번째 문제를 꺼내고, 그 문제의 질문을 읽는다.

이 데이터를 `json.dump()`로 `state.json`에 쓴다. JSON은 데이터를 파일에 담는 형식이다. UTF-8로 저장하고, 한글은 그대로 표시되도록 설정했다.

문제 추가, 최고 점수 갱신, 종료할 때 저장한다. 저장 중 오류가 나면 안내 메시지를 출력한다.

### 4.8 load() — 파일에서 불러오기

`load()`는 `json.load()`로 파일의 내용을 읽는다.

읽어 온 문제는 딕셔너리 상태이므로 질문, 선택지, 정답 번호를 꺼내서 다시 `Quiz(...)`로 묶는다. 그래야 `display()`, `is_correct()` 같은 메서드를 사용할 수 있다.

`__init__()` 안의 `self.load()`는 이 메서드를 새로 만드는 코드가 아니라, 이미 정의한 메서드를 호출하는 코드다. 게임을 만들 때 이전 데이터를 준비해두려고 여기서 호출한다.

파일이 없으면 기본 문제로 시작한다. 파일이 손상됐거나 형식이 잘못됐으면 안내 후 기본 데이터를 사용한다.

## 5. 파일 구조와 저장 데이터

| 파일·폴더 | 역할 |
| --- | --- |
| `main.py` | 퀴즈 게임 코드 |
| `README.md` | 실행 방법과 공부 기록 |
| `.gitignore` | Git에 올리지 않을 파일 설정 |
| `state.json` | 실행 중 생성되는 문제 목록·최고 점수 |
| `Screenshot/` | 제출용 화면 캡처 |

`state.json`은 `main.py`와 같은 폴더에 저장된다. 저장 시점에 파일이 생성되며, 다시 저장하면 현재 데이터로 바뀐다. 개인 실행 데이터라서 Git에는 올리지 않는다.

아래는 문제 하나만 넣어 본 저장 형태의 예시다. 실제 기본 문제는 5개다.

```json
{
  "quizzes": [
    {
      "question": "현재 작업 중인 폴더의 경로를 출력하는 명령어는?",
      "choices": ["ls", "pwd", "cd", "mkdir"],
      "answer": 2
    }
  ],
  "best_score": null
}
```

`null`은 JSON에서 값이 없음을 나타낸다. Python으로 읽어 오면 `None`이 된다.

## 6. Git 실습

기능 하나를 만들고 확인한 뒤 커밋하는 방식으로 진행했다.

퀴즈 풀기는 `feature-play` 브랜치에서 작업하고, `main`에 병합했다.

```bash
git checkout -b feature-play
git add main.py
git commit -m "Feat: 퀴즈 풀기 기능 구현 및 QuizGame 클래스 도입"
git checkout main
git merge --no-ff feature-play -m "Merge: 퀴즈 풀기 기능 병합"
git push origin main
```

**배운 점**

- `commit`: 선택한 변경 내용을 하나의 기록으로 남긴다.
- `branch`: 기존 작업에서 가지를 나누어 작업한다.
- `merge`: 다른 브랜치의 작업을 합친다. `--no-ff`로 병합 기록을 남겼다.
- `origin`: GitHub 저장소에 붙인 이름이다. 현재 `main`은 `origin/main`과 연결되어 있어 `git push`만으로도 올릴 수 있다.

**clone·pull 실습**

별도 폴더에 `clone`해서 README를 한 줄 수정하고 commit·push한 다음, 원래 폴더에서 `pull`로 가져왔다. 원래 폴더에도 수정한 내용이 반영되는 것을 확인했다.

- `clone`: 저장소를 별도 폴더로 복제한다.
- `pull`: 원격 저장소의 변경을 현재 폴더로 가져온다.

## 7. 제출용 스크린샷

실행 화면은 `Screenshot/` 폴더에 모았다. 파일 이름을 누르면 캡처를 볼 수 있다.

| 파일 이름 | 확인한 내용 |
| --- | --- |
| [env.png](Screenshot/env.png) | Python·Git 버전과 Git 작성자 설정 |
| [add-quiz.png](Screenshot/add-quiz.png) | 문제를 입력한 뒤 추가 완료 메시지 |
| [list.png](Screenshot/list.png) | 추가한 문제가 포함된 목록 |
| [play.png](Screenshot/play.png) | 잘못된 번호 재입력, 퀴즈 풀이와 최종 결과 |
| [score.png](Screenshot/score.png) | 최고 점수 갱신 |
| [git-graph.png](Screenshot/git-graph.png) | 기능 개발을 마친 시점의 분기·병합 기록 |

개발 환경 확인은 터미널에서 아래 명령으로 할 수 있다.

```bash
python3 --version
git --version
git config --get user.name
```

Git 기록은 아래 명령으로 확인한다.

```bash
git log --oneline --graph --all
git rev-list --count HEAD
```
