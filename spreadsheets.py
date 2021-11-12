import gspread


def get_test(sheet_name='Тест'):
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("Test_survey_bot")

    worksheet = sh.worksheet(sheet_name)
    return worksheet.get_all_records()


def get_all_tests():
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open("Test_survey_bot")
    return sh.worksheets()
