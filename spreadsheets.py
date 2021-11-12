from datetime import datetime

import gspread


def get_spreadsheet():
    gc = gspread.service_account(filename='credentials.json')
    return gc.open("Test_survey_bot")


def get_test(sheet_name='Тест'):
    sh = get_spreadsheet()

    worksheet = sh.worksheet(sheet_name)
    return worksheet.get_all_records()


def add_result_to_worksheet(test_name, user_data, result_list):

    sh = get_spreadsheet()

    try:
        sh.worksheet(test_name)
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(test_name, 0, 0)
        top_row = ["Студент", "Время"]
        for q in result_list:
            top_row.append(q["Вопрос"])
        top_row.append("Результат")
        ws.append_row(top_row)

    ws = sh.worksheet(test_name)

    correct_answers = 0
    boolean_answer_list = []

    for answer in result_list:
        if answer['is_correct']:
            correct_answers += 1
            boolean_answer_list.append("Верно")
        else:
            boolean_answer_list.append("Неверно")

    row = [user_data, str(datetime.now())]

    for ans in boolean_answer_list:
        row.append(ans)

    row.append(f"{correct_answers}/{len(result_list)}")

    ws.append_row(row)
