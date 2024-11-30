import os
import re
from zipfile import ZipFile


def extract_zip(zip, extract_dir):
    if not os.path.isdir("quiz"):
        with ZipFile("quiz-questions.zip", "r") as zipf:
            zipf.extractall("quiz")


def get_answer_and_questions(filename, code):
    with open("1vs1200.txt", "r", encoding="KOI8-R") as file:
        questions_and_answers = file.read()

        question_pattern = r"(Вопрос\s\d+:.*?)(?=Ответ:)"
        answer_pattern = r"(Ответ:.*?)(?=\n\n|$)"

        questions = re.findall(question_pattern, questions_and_answers, re.DOTALL)
        answers = re.findall(answer_pattern, questions_and_answers, re.DOTALL)

        questions = [q.replace("\n", " ").strip() for q in questions]
        answers = [a.replace("\n", " ").strip() for a in answers]
        questions_and_answes = dict(zip(questions, answers))
    return questions_and_answes


if __name__ == "__main__":
    extract_zip("quiz-questions.zip", "quiz")
    questions_and_answes = get_answer_and_questions("1vs1200.txt", "KOI8-R")
