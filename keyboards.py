from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_answers_keyboard(question: dict, question_number: int) -> InlineKeyboardMarkup:
    answers_kb = InlineKeyboardMarkup(row_width=2)
    answers = []
    keys = list(question.keys())
    next_question = question_number + 1
    for answer in keys:
        if answer.startswith("ответ"):
            answers.append(InlineKeyboardButton(f"{question[answer]}", callback_data=f"question;"
                                                                                     f"{next_question};"
                                                                                     f"{answer}"))
    answers_kb.add(*answers)
    return answers_kb
