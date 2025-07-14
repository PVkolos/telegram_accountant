from aiogram.filters.state import StatesGroup, State


class State_Voice(StatesGroup): # todo
    text = State()


class Pool(StatesGroup): # todo
    quest = State()
    vars = State()


class Write_Keys(StatesGroup): # Ввод нового ключевого слова
    step_one = State()
    step_two = State()


class Support(StatesGroup): # МС для отправки сообщения от пользователя к админу
    text_message = State()


class Admin(StatesGroup): # МС для отправления сообщения от админа пользователям todo
    text = State()
    photo = State()


class New_Key_Word(StatesGroup): # Машина состояний для создания нового ключевого слова или категории
    new_key_word = State()


class Two_Table(StatesGroup): # Машина состояний для добавления второй таблицы
    link = State()


class One_Table(StatesGroup): # Машина состояний для добавления первой таблицы
    link_sheets_one = State()


class ChangeTable(StatesGroup): #  Машина состояний для редактирования таблицы под пользователя
    businessman = State()
    source = State()
    savings = State()
    cafe = State()
    traveling = State()
    reserve = State()
    credit = State()
    car = State()
    debt = State()