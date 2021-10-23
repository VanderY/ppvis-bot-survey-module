import gspread


def choose_answer(test: list) -> list:
    answers = []
    for question in test:
        keys = list(question.keys())
        print(f"{question['Вопрос']}\n"
              f"1.{question['ответ 1']}\n"
              f"2.{question['ответ 2']}\n"
              f"3.{question['ответ 3']}\n"
              f"4.{question['ответ 4']}\n"
              f"Напишите вариант ответа: ")
        answer = {question['Вопрос']: input()}
        answers.append(answer)
    return answers


def get_test(sheet_name='Тест'):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("Test_survey_bot")

    worksheet = sh.worksheet(sheet_name)
    # answers = choose_answer(worksheet.get_all_records())
    return worksheet.get_all_records()


