from create import bot, db
from aiogram import types, Dispatcher, Router, F
from aiogram.filters import Command
from helps_func.works import extract_unique_code, welc, send, set_table_prod
from helps_func import sheets_api
from . import text
from . import commands
# from .voice_handler import voice
from states.states import One_Table, ChangeTable, Two_Table, New_Key_Word, Write_Keys, Support, State_Voice
from . import machines
from keyboards import reply
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType

router = Router()


async def start(message):
    # Выделение id рефера
    unique_code = extract_unique_code(message.text)
    if unique_code and unique_code != message.from_user.id and db.check_refer(
            message.from_user.id) and not db.check_user_on_db(message.from_user.id):
        db.add_referal(unique_code, message.from_user.id)
    # Добавление в БД
    if not db.check_user_on_db(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.username)
    # Приветствие
    await welc(message)


# Обработка текстовых сообщений
async def text_message(message, state: FSMContext):
    await text.handler(message, state)


async def process_callback_kb1btn1(callback_query: types.CallbackQuery, state: FSMContext):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
    if code == 'q':
        tbl1 = await sheets_api.table(db.get_sheets_one(callback_query.from_user.id))
        await send(callback_query.from_user.id, f'Вы выбрали таблицу: {tbl1[0]}\nТеперь все записи и операции будут производиться в ней')
        db.update_def_table(callback_query.from_user.id, 'id_sheets')
    elif code == 'w':
        tbl1 = await sheets_api.table(await db.get_two_sheets(callback_query.from_user.id))
        await send(callback_query.from_user.id, f'Вы выбрали таблицу: {tbl1[0]}\nТеперь все записи и операции будут производиться в ней')
        db.update_def_table(callback_query.from_user.id, 'sheets2')
    # if code == 'l':
    #     if db.check_is_trial(callback_query.from_user.id):
    #         await bot.send_message(callback_query.from_user.id, text='Пробный пероид длится 7 дней. Время пошло. '
    #                                                         'Введите команду /help для получения справки по боту')
    #         db.update_info_sub(callback_query.from_user.id, 'trial')
    #         db.update_info_sub_date(callback_query.from_user.id, datetime.now().today() + timedelta(days=7), one=True)
    #         db.update_trial(callback_query.from_user.id)
    #     else:
    #         await bot.answer_callback_query(callback_query.id, text='Нельзя приобрести пробную подписку дважды!')
    elif code == 't':
        try:
            await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id - 1)
        except: pass
        await callback_query.message.delete()
    elif code == 's':
        await callback_query.message.delete()
        await send(callback_query.from_user.id, 'Хорошо, бот задаст вам пару вопросов.')

        await send(callback_query.from_user.id, 'Вы предприниматель?', reply.table_modification())
        await state.set_state(ChangeTable.businessman)
    elif code == 'o':
        await callback_query.message.delete()
        await send(callback_query.from_user.id, 'Ок, ваша таблица настроенна по умолчанию')
        await set_table_prod(callback_query)
    elif code == 'p':
        await callback_query.message.delete()


async def voice_handler(message):
    await send(message.from_user.id, 'Приносим свои извинения, голосовой ввод пока не работает')


# отлавливание любого поведения пользователя
def register_client_handlers(dp: Dispatcher):
    dp.message.register(start, Command(commands=["start", "run"]))
    dp.message.register(commands.commands, F.text.startswith('/'))
    # dp.message.register(voice.voice_message_handler, F.content_type == ContentType.VOICE)
    dp.message.register(voice_handler, F.content_type == ContentType.VOICE)
    dp.message.register(machines.link_sheets_one, One_Table.link_sheets_one)
    dp.message.register(machines.businessman, ChangeTable.businessman)
    dp.message.register(machines.source, ChangeTable.source)
    dp.message.register(machines.savings, ChangeTable.savings)
    dp.message.register(machines.cafe, ChangeTable.cafe)
    dp.message.register(machines.traveling, ChangeTable.traveling)
    dp.message.register(machines.reserve, ChangeTable.reserve)
    dp.message.register(machines.credit, ChangeTable.credit)
    dp.message.register(machines.car, ChangeTable.car)
    dp.message.register(machines.debt, ChangeTable.debt)
    dp.message.register(machines.link_two_sheets, Two_Table.link)
    dp.message.register(machines.new_key_word, New_Key_Word.new_key_word)
    dp.message.register(machines.step_one_write_key, Write_Keys.step_one)
    dp.message.register(machines.step_two_write_key, Write_Keys.step_two)
    dp.message.register(machines.text_message_support, Support.text_message)
    dp.message.register(machines.state_voice, State_Voice.text)
    dp.message.register(text_message, F.text)
    dp.callback_query.register(process_callback_kb1btn1, F.data)