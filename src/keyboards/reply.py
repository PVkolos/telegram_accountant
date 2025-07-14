from aiogram import types


def main_kb():
    items_main_kb = [
        [types.KeyboardButton(text="Поддержать разработчика💰")],
        [types.KeyboardButton(text="Удалить последнюю запись"), types.KeyboardButton(text="Изменить таблицу по умолчанию")],
        [types.KeyboardButton(text="Итого за месяц"), types.KeyboardButton(text="Мои категории и разделы")],
        # [types.KeyboardButton(text="Дата окончания подписки")],
        [types.KeyboardButton(text="Посмотреть последние 30 записей")],
    ]

    keyboard = types.ReplyKeyboardMarkup(
            keyboard=items_main_kb,
            resize_keyboard=True,
            input_field_placeholder="Меню"
    )
    return keyboard


def abolition_kb():
    item_abolition_kb = [
        [types.KeyboardButton(text='Отмена')]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=item_abolition_kb,
        resize_keyboard=True,
        input_field_placeholder='Добавление таблицы'
    )
    return keyboard


def table_modification():
    item_abolition_kb = [
        [types.KeyboardButton(text='Да')],
        [types.KeyboardButton(text='Нет')],
        [types.KeyboardButton(text='Стоп')]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=item_abolition_kb,
        resize_keyboard=True,
        input_field_placeholder='Ответ на вопрос выше'
    )

    return keyboard

def auto_markup(*args, step=1, is_=True):
    if is_:
        item_abolition_kb = [
            [types.KeyboardButton(text='Добавить новую категорию или ключевое слово✅')],
            [types.KeyboardButton(text='Отмена')],
        ]
    else: item_abolition_kb = [[types.KeyboardButton(text='Отмена')]]
    # for i in range(0, len(args[0]), step)
    for arg in args[0]:
        item_abolition_kb.append([types.KeyboardButton(text=arg)])

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=item_abolition_kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите предложенный вариант'
    )
    return keyboard


def new_category():
    item_abolition_kb = [
        [types.KeyboardButton(text='Ключевое слово'), types.KeyboardButton(text='Категория')],
        [types.KeyboardButton(text='Нет, отмена')],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=item_abolition_kb,
        resize_keyboard=True,
        input_field_placeholder='Выберите предложенный вариант'
    )
    return keyboard


def support():
    item_abolition_kb = [
        [types.KeyboardButton(text='Отмена')]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=item_abolition_kb,
        resize_keyboard=True,
        input_field_placeholder='Предложение или жалоба'
    )
    return keyboard


def voice_input():
    item_abolition_kb = [
        [types.KeyboardButton(text='Отмена')],
        [types.KeyboardButton(text='Верно')],
        [types.KeyboardButton(text='Неверно')]
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=item_abolition_kb,
        resize_keyboard=True,
        input_field_placeholder='Голосовой ввод'
    )
    return keyboard