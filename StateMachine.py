from aiogram.utils.helper import Helper, HelperMode, ListItem


class StateMachine(Helper):
    mode = HelperMode.snake_case

    ANSWERING_TEST = ListItem()


if __name__ == '__main__':
    print(StateMachine.all())
