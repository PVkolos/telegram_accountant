from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no():
    tr_yes = InlineKeyboardButton(text='Да', callback_data='tr_yes')
    tr_no = InlineKeyboardButton(text='Нет', callback_data='tr_no')
    tr_exit = InlineKeyboardButton(text='Отмена', callback_data='tr_exit_p')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[tr_yes, tr_no, tr_exit]], row_width=3)
    return keyboard


def delete_sticker():
    delete = InlineKeyboardButton(text='Удалить стикер...', callback_data='tr_delete_st')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[delete]])
    return keyboard


def selection_sheets(title1, title2):
    sheet1 = types.InlineKeyboardButton(text=title1, callback_data='trq')
    sheet2 = types.InlineKeyboardButton(text=title2, callback_data='trw')
    return InlineKeyboardMarkup(inline_keyboard=[[sheet1, sheet2]])
