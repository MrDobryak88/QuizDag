import json
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Программа проверки знаний / Knowledge Testing Program")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Переменные
        self.questions = self.load_questions('questions.json')
        self.results = self.load_results('results.json')
        self.current_questions = []
        self.current_index = 0
        self.correct_count = 0
        self.username = None
        self.theme = "light"
        self.language = "ru"  # Русский по умолчанию

        # Словарь переводов
        self.translations = {
            "ru": {
                "welcome": "Добро пожаловать, {username}!",
                "select_topic": "Выберите тему теста:",
                "start_quiz": "Начать тест",
                "file_menu": "Файл",
                "exit": "Выход",
                "settings_menu": "Настройки",
                "toggle_theme": "Сменить тему",
                "add_test": "Добавить тест",
                "history": "История тестов",
                "new_test": "Новый тест",
                "enter_topic": "Введите название темы:",
                "topic_error": "Тема уже существует или не введена!",
                "add_question": "Добавление вопросов в {topic}",
                "multiple_choice": "Множественный выбор",
                "short_answer": "Краткий ответ",
                "save_question": "Добавить вопрос",
                "save_close": "Сохранить и закрыть",
                "question_error": "Вопросы не найдены для выбранной темы!",
                "question": "Вопрос {index} из {total}: ",
                "answer": "Ответить",
                "correct": "Правильно!",
                "incorrect": "Неправильно. Правильный ответ: {answer}",
                "no_answer": "Выберите или введите ответ!",
                "test_complete": "Тест завершен!",
                "correct_answers": "Правильных ответов: {correct} из {total}",
                "percentage": "Процент правильных ответов: {percent:.2f}%",
                "back": "Вернуться к началу",
                "retry": "Пройти тест заново",
                "close": "Закрыть",
                "history_title": "История тестов",
                "history_empty": "История тестов пуста.",
                "switch_lang": "Switch to English"
            },
            "en": {
                "welcome": "Welcome, {username}!",
                "select_topic": "Select quiz topic:",
                "start_quiz": "Start Quiz",
                "file_menu": "File",
                "exit": "Exit",
                "settings_menu": "Settings",
                "toggle_theme": "Toggle Theme",
                "add_test": "Add Test",
                "history": "Test History",
                "new_test": "New Test",
                "enter_topic": "Enter topic name:",
                "topic_error": "Topic already exists or not entered!",
                "add_question": "Adding questions to {topic}",
                "multiple_choice": "Multiple Choice",
                "short_answer": "Short Answer",
                "save_question": "Add Question",
                "save_close": "Save and Close",
                "question_error": "No questions found for the selected topic!",
                "question": "Question {index} of {total}: ",
                "answer": "Submit Answer",
                "correct": "Correct!",
                "incorrect": "Incorrect. Correct answer: {answer}",
                "no_answer": "Please select or enter an answer!",
                "test_complete": "Test Completed!",
                "correct_answers": "Correct answers: {correct} out of {total}",
                "percentage": "Percentage of correct answers: {percent:.2f}%",
                "back": "Back to Start",
                "retry": "Retry Quiz",
                "close": "Close",
                "history_title": "Test History",
                "history_empty": "Test history is empty.",
                "switch_lang": "Переключить на русский"
            }
        }

        # Вход в профиль
        self.login_window()

    def get_text(self, key, **kwargs):
        """Возвращает переведённый текст с подстановкой параметров."""
        text = self.translations[self.language].get(key, key)
        return text.format(**kwargs) if kwargs else text

    def load_questions(self, filename):
        """Загружает вопросы из файла JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data.get('topics', {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def load_results(self, filename):
        """Загружает историю результатов из файла JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
            return data.get('results', [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_questions(self):
        """Сохраняет вопросы в файл JSON."""
        try:
            with open('questions.json', 'w', encoding='utf-8') as file:
                json.dump({"topics": self.questions}, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save questions: {e}")

    def save_results(self):
        """Сохраняет результаты в файл JSON."""
        try:
            with open('results.json', 'w', encoding='utf-8') as file:
                json.dump({"results": self.results}, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save results: {e}")

    def login_window(self):
        """Окно входа в профиль."""
        login_win = tk.Toplevel(self.root)
        login_win.title("Login / Вход")
        login_win.geometry("300x150")
        login_win.resizable(False, False)
        login_win.transient(self.root)
        login_win.grab_set()

        ttk.Label(login_win, text=self.get_text("welcome").replace("{username}", "")).pack(pady=10)
        username_entry = ttk.Entry(login_win)
        username_entry.pack(pady=5)
        username_entry.focus()

        def submit_username():
            self.username = username_entry.get().strip()
            if self.username:
                login_win.destroy()
                self.create_menu()
                self.create_main_frame()
                self.apply_theme()
            else:
                messagebox.showwarning("Error", "Please enter a username!")

        ttk.Button(login_win, text="Login / Войти", command=submit_username).pack(pady=10)
        login_win.bind("<Return>", lambda event: submit_username())

    def create_menu(self):
        """Создает меню с настройками."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.get_text("file_menu"), menu=file_menu)
        file_menu.add_command(label=self.get_text("exit"), command=self.root.quit)

        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.get_text("settings_menu"), menu=settings_menu)
        settings_menu.add_command(label=self.get_text("toggle_theme"), command=self.toggle_theme)
        settings_menu.add_command(label=self.get_text("add_test"), command=self.add_new_test)
        settings_menu.add_command(label=self.get_text("history"), command=self.show_history)
        settings_menu.add_command(label=self.get_text("switch_lang"), command=self.toggle_language)

    def create_main_frame(self):
        """Создает основной фрейм для интерфейса."""
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill="both", expand=True)

        ttk.Label(self.main_frame, text=self.get_text("welcome", username=self.username), font=("Arial", 14)).pack(pady=10)
        ttk.Label(self.main_frame, text=self.get_text("select_topic")).pack(pady=5)
        self.topic_combo = ttk.Combobox(self.main_frame, values=list(self.questions.keys()) + ["All Topics / Все темы"])
        self.topic_combo.set("All Topics / Все темы")
        self.topic_combo.pack(pady=5)

        self.start_button = ttk.Button(self.main_frame, text=self.get_text("start_quiz"), command=self.start_quiz)
        self.start_button.pack(pady=10)

        self.quiz_frame = ttk.Frame(self.main_frame)
        self.result_frame = ttk.Frame(self.main_frame)

    def apply_theme(self):
        """Применяет выбранную тему оформления."""
        style = ttk.Style()
        if self.theme == "light":
            style.theme_use("clam")
            self.root.configure(bg="#f0f0f0")
            style.configure("TLabel", background="#f0f0f0", foreground="black")
            style.configure("TButton", background="#e0e0e0")
        else:
            style.theme_use("alt")
            self.root.configure(bg="#2e2e2e")
            style.configure("TLabel", background="#2e2e2e", foreground="white")
            style.configure("TButton", background="#444444", foreground="white")

    def toggle_theme(self):
        """Переключает тему оформления."""
        self.theme = "dark" if self.theme == "light" else "light"
        self.apply_theme()
        self.update_ui()

    def toggle_language(self):
        """Переключает язык интерфейса."""
        self.language = "en" if self.language == "ru" else "ru"
        self.update_ui()

    def update_ui(self):
        """Обновляет интерфейс после смены языка или темы."""
        self.root.title("Программа проверки знаний / Knowledge Testing Program")
        self.create_menu()
        self.main_frame.destroy()
        self.create_main_frame()
        self.apply_theme()

    def add_new_test(self):
        """Добавляет новый тест через диалоговое окно."""
        topic = simpledialog.askstring(self.get_text("new_test"), self.get_text("enter_topic"))
        if not topic or topic in self.questions:
            messagebox.showwarning("Error", self.get_text("topic_error"))
            return

        self.questions[topic] = []
        question_window = tk.Toplevel(self.root)
        question_window.title(self.get_text("add_question", topic=topic))
        question_window.geometry("500x400")

        question_list = scrolledtext.ScrolledText(question_window, width=60, height=15)
        question_list.pack(pady=10)

        def save_question():
            question_text = question_list.get("1.0", tk.END).strip()
            if not question_text:
                return

            q_type = type_var.get()
            if q_type == "multiple_choice":
                options = simpledialog.askstring("Options", "Enter options separated by commas (e.g., a, b, c):")
                correct = simpledialog.askstring("Correct Answer", "Enter the correct answer:")
                if options and correct:
                    question = {
                        "question": question_text,
                        "type": "multiple_choice",
                        "options": [opt.strip() for opt in options.split(",")],
                        "correct_answer": correct.strip()
                    }
            else:
                correct = simpledialog.askstring("Correct Answer", "Enter the correct answer:")
                if correct:
                    question = {
                        "question": question_text,
                        "type": "short_answer",
                        "correct_answer": correct.strip()
                    }
            self.questions[topic].append(question)
            question_list.delete("1.0", tk.END)
            messagebox.showinfo("Success", "Question added!")

        type_var = tk.StringVar(value="multiple_choice")
        ttk.Radiobutton(question_window, text=self.get_text("multiple_choice"), variable=type_var, value="multiple_choice").pack()
        ttk.Radiobutton(question_window, text=self.get_text("short_answer"), variable=type_var, value="short_answer").pack()

        ttk.Button(question_window, text=self.get_text("save_question"), command=save_question).pack(pady=5)
        ttk.Button(question_window, text=self.get_text("save_close"), command=lambda: [self.save_questions(), question_window.destroy()]).pack(pady=5)

    def start_quiz(self):
        """Начинает тест."""
        self.quiz_frame.destroy()
        self.result_frame.destroy()
        self.quiz_frame = ttk.Frame(self.main_frame)
        self.quiz_frame.pack(fill="both", expand=True)

        selected_topic = self.topic_combo.get()
        if selected_topic == "All Topics / Все темы":
            self.current_questions = [q for topic in self.questions.values() for q in topic]
        else:
            self.current_questions = self.questions.get(selected_topic, [])

        if not self.current_questions:
            messagebox.showwarning("Error", self.get_text("question_error"))
            return

        random.shuffle(self.current_questions)
        self.correct_count = 0
        self.current_index = 0
        self.show_question()

    def show_question(self):
        """Отображает текущий вопрос."""
        for widget in self.quiz_frame.winfo_children():
            widget.destroy()

        if self.current_index >= len(self.current_questions):
            self.show_results()
            return

        question = self.current_questions[self.current_index]
        ttk.Label(self.quiz_frame, text=self.get_text("question", index=self.current_index + 1, total=len(self.current_questions)) + question['question'], wraplength=700).pack(pady=10)

        if question['type'] == "multiple_choice":
            self.var = tk.StringVar(value="")
            for option in question['options']:
                ttk.Radiobutton(self.quiz_frame, text=option, variable=self.var, value=option).pack(anchor="w")
            ttk.Button(self.quiz_frame, text=self.get_text("answer"), command=self.check_multiple_choice).pack(pady=10)
        else:
            self.answer_entry = ttk.Entry(self.quiz_frame)
            self.answer_entry.pack(pady=10)
            ttk.Button(self.quiz_frame, text=self.get_text("answer"), command=self.check_short_answer).pack(pady=10)

    def check_multiple_choice(self):
        """Проверяет ответ на вопрос с множественным выбором."""
        question = self.current_questions[self.current_index]
        user_answer = self.var.get()
        correct_answer = question['correct_answer']
        if not user_answer:
            messagebox.showwarning("Error", self.get_text("no_answer"))
            return
        if user_answer == correct_answer:
            self.correct_count += 1
            messagebox.showinfo("Result", self.get_text("correct"))
        else:
            messagebox.showinfo("Result", self.get_text("incorrect", answer=correct_answer))
        self.current_index += 1
        self.show_question()

    def check_short_answer(self):
        """Проверяет ответ на вопрос с кратким ответом."""
        question = self.current_questions[self.current_index]
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = question['correct_answer'].strip().lower()
        if not user_answer:
            messagebox.showwarning("Error", self.get_text("no_answer"))
            return
        if user_answer == correct_answer:
            self.correct_count += 1
            messagebox.showinfo("Result", self.get_text("correct"))
        else:
            messagebox.showinfo("Result", self.get_text("incorrect", answer=correct_answer))
        self.current_index += 1
        self.show_question()

    def show_results(self):
        """Отображает результаты теста."""
        self.quiz_frame.destroy()
        self.result_frame = ttk.Frame(self.main_frame)
        self.result_frame.pack(fill="both", expand=True)

        percentage = (self.correct_count / len(self.current_questions)) * 100
        ttk.Label(self.result_frame, text=self.get_text("test_complete"), font=("Arial", 14)).pack(pady=10)
        ttk.Label(self.result_frame, text=self.get_text("correct_answers", correct=self.correct_count, total=len(self.current_questions))).pack(pady=5)
        ttk.Label(self.result_frame, text=self.get_text("percentage", percent=percentage)).pack(pady=5)

        result = {
            "username": self.username,
            "topic": self.topic_combo.get(),
            "percentage": percentage,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.results.append(result)
        self.save_results()

        ttk.Button(self.result_frame, text=self.get_text("back"), command=self.create_main_frame).pack(pady=5)
        ttk.Button(self.result_frame, text=self.get_text("retry"), command=self.start_quiz).pack(pady=5)

    def show_history(self):
        """Отображает историю тестов с графикой."""
        history_win = tk.Toplevel(self.root)
        history_win.title(self.get_text("history_title"))
        history_win.geometry("800x600")

        # Текстовая история
        history_text = scrolledtext.ScrolledText(history_win, width=70, height=10)
        history_text.pack(pady=10)

        if not self.results:
            history_text.insert(tk.END, self.get_text("history_empty") + "\n")
        else:
            for res in self.results:
                if res["username"] == self.username:
                    line = f"Topic: {res['topic']} | Percentage: {res['percentage']:.2f}% | Date: {res['date']}\n"
                    history_text.insert(tk.END, line)

        # Графика
        user_results = [res for res in self.results if res["username"] == self.username]
        if user_results:
            fig, ax = plt.subplots(figsize=(8, 4))
            topics = [res["topic"] for res in user_results]
            percentages = [res["percentage"] for res in user_results]  # Исправлено: hanuser_results -> user_results
            ax.bar(topics, percentages, color="skyblue")
            ax.set_xlabel("Topics" if self.language == "en" else "Темы")
            ax.set_ylabel("Percentage (%)" if self.language == "en" else "Процент (%)")
            ax.set_title("Test Results" if self.language == "en" else "Результаты тестов")
            plt.xticks(rotation=45, ha="right")

            canvas = FigureCanvasTkAgg(fig, master=history_win)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)

        ttk.Button(history_win, text=self.get_text("close"), command=history_win.destroy).pack(pady=5)

        def export_to_csv():
            import csv
            user_results = [res for res in self.results if res["username"] == self.username]
            with open(f"{self.username}_results.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Topic", "Percentage", "Date"])
                for res in user_results:
                    writer.writerow([res["topic"], res["percentage"], res["date"]])
            messagebox.showinfo("Export", "Results exported to CSV!")

        ttk.Button(history_win, text="Export to CSV / Экспорт в CSV", command=export_to_csv).pack(pady=5)
        ttk.Button(history_win, text=self.get_text("close"), command=history_win.destroy).pack(pady=5)



if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()