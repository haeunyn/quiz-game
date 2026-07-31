import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = int(answer)

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

class QuizGame:
    def __init__(self, filename="state.json"):
        self.filename = filename
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            self.set_default_data()
            return

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz(q["question"], q["choices"], q["answer"]) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", 0)
                print(f"\n💻 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)\n")
        except Exception:
            print("\n⚠️ 파일이 손상되었습니다. 기본 데이터로 초기화합니다.\n")
            self.set_default_data()

    def set_default_data(self):
        default_quizzes = [
            Quiz("마블 시네마틱 유니버스에서 타노스가 모은 인피니티 스톤의 개수는?", ["4개", "5개", "6개", "7개"], 3),
            Quiz("영화 '인터스텔라'에서 주인공이 방문하지 않은 행성은?", ["밀러 행성", "만 행성", "에드먼즈 행성", "화성"], 4),
            Quiz("Python의 창시자는?", ["Guido", "Linus", "Bjarne", "James"], 1),
            Quiz("영화 '기생충'의 감독은?", ["박찬욱", "봉준호", "김기덕", "이창동"], 2),
            Quiz("대한민국의 수도는?", ["부산", "인천", "서울", "대구"], 3)
        ]
        self.quizzes = default_quizzes
        self.best_score = 0
        self.save_data()

    def save_data(self):
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score
        }
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def play_quiz(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.\n")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)\n" + "-"*30)
        correct_count = 0

        for idx, q in enumerate(self.quizzes, 1):
            print(f"\n[문제 {idx}]\n{q.question}\n")
            for c_idx, choice in enumerate(q.choices, 1):
                print(f"{c_idx}. {choice}")
            
            while True:
                user_ans = input("\n정답 입력: ").strip()
                if user_ans.isdigit() and 1 <= int(user_ans) <= len(q.choices):
                    break
                print("⚠️ 올바른 번호를 입력해 주세요.")

            if int(user_ans) == q.answer:
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print("❌ 오답입니다!")

        score = int((correct_count / len(self.quizzes)) * 100)
        print("="*35)
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {correct_count}문제 정답! ({score}점)")
        
        if score > self.best_score:
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score
            self.save_data()
        print("="*35 + "\n")

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = input("문제를 입력하세요: ").strip()
        choices = []
        for i in range(1, 5):
            choices.append(input(f"선택지 {i}: ").strip())
        
        while True:
            ans = input("정답 번호 (1-4): ").strip()
            if ans in ["1", "2", "3", "4"]:
                break
            print("⚠️ 1에서 4 사이의 숫자를 입력하세요.")

        self.quizzes.append(Quiz(question, choices, int(ans)))
        self.save_data()
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def list_quizzes(self):
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n" + "-"*30)
        for idx, q in enumerate(self.quizzes, 1):
            print(f"[{idx}] {q.question}")
        print("-"*30 + "\n")

    def show_score(self):
        print(f"\n🏆 최고 점수: {self.best_score}점\n")

    def run(self):
        while True:
            print("====================================")
            print("      🎯 나만의 퀴즈 게임 🎯      ")
            print("====================================")
            print("1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료")
            print("====================================")
            
            choice = input("선택: ").strip()
            if choice == "1":
                self.play_quiz()
            elif choice == "2":
                self.add_quiz()
            elif choice == "3":
                self.list_quizzes()
            elif choice == "4":
                self.show_score()
            elif choice == "5":
                print("\n게임을 종료합니다. 이용해 주셔서 감사합니다!\n")
                break
            else:
                print("\n⚠️ 잘못된 입력입니다. 1-5 사이의 숫자를 입력하세요.\n")

if __name__ == "__main__":
    game = QuizGame()
    game.run()