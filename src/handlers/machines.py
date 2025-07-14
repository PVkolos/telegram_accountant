from datetime import datetime

from googleapiclient.errors import HttpError
from helps_func.works import send, check_sign_sum, json_serial, dotdict
from states.states import One_Table, ChangeTable, Write_Keys
from keyboards import reply, inline
from aiogram.fsm.context import FSMContext
from create import db
from helps_func import works, sheets_api
from .text import handler


async def set_table(message, state: FSMContext):
    table = 'изменить основную таблицу' if (db.get_id_sheets(message.from_user.id) and db.get_sheets_one(message.from_user.id) != 'none') else 'добавить основную таблицу'
    await send(message.from_user.id, f'Вы решили {table}. Для этого вам нужно:\n1️⃣. Предоставьте в вашей '
                                     'таблице доступ этому аккаунту на <b>редактирование</b>: <u>servis@new-project-336414.iam.gserviceaccount.com</u>\n'
                                     '2️⃣. Отправьте ссылку на вашу таблицу этому боту в следующем сообщении.', reply.abolition_kb())
    await state.set_state(One_Table.link_sheets_one)


async def link_sheets_one(message, state):
    try:
        if message.text == 'Отмена':
            await state.clear()
            await send(message.from_user.id, 'Хорошо, запись остановлена', markup='menu')
        else:
            tableId = message.text.split("/d/")[1].split("/edit")[0]
            if tableId in [await db.get_two_sheets(message.from_user.id), db.get_sheets_one(message.from_user.id)]:
                await send(message.from_user.id,
                           'Обратите внимание, что эта таблица уже задана вами. Если вы продолжите процесс, листы "Записи бота" и "Категории и разделы" не сохранятся!')

            db.change_temp_info(f'table_number: 1; {tableId}', message.from_user.id)

            await send(message.from_user.id,
                       'Хотите ли вы настроить вашу таблицу индивидуально под вас? Будут изменены некоторые разделы.', markup=inline.yes_no())
            await state.clear()
    except Exception:
        await send(message.from_user.id,
                   '❗️Вы ввели неверную ссылку.❗️\nhttps://docs.google.com/spreadsheets/d/..../edit/...\n'
                   'Ссылка на таблицу выглядит подобным образом')


async def businessman(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message.from_user.id, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(businessman=message.text)
        # globalVar[message.from_user.id] = [message.text]
        await send(message.from_user.id, 'У вас один источник дохода?', reply.table_modification())
        await state.set_state(ChangeTable.source)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def source(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(source=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'У вас есть сбережения, которыми вы пользуетесь?', reply.table_modification())
        await state.set_state(ChangeTable.savings)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def savings(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(savings=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'Вы посещаете кафе, рестораны или прочие забегаловки?', reply.table_modification())
        await state.set_state(ChangeTable.cafe)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def cafe(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(cafe=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'Вы путешествуете?', reply.table_modification())
        await state.set_state(ChangeTable.traveling)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def traveling(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(traveling=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'Вы откладываете часть доходов резервом?', reply.table_modification())
        await state.set_state(ChangeTable.reserve)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def reserve(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(reserve=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'У Вас есть кредиты или ипотеки?', reply.table_modification())
        await state.set_state(ChangeTable.credit)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def credit(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(credit=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'У Вас есть автомобиль?', reply.table_modification())
        await state.set_state(ChangeTable.car)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def car(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(car=message.text)
        # globalVar[message.from_user.id].append(message.text)
        await send(message.from_user.id, 'У Вас есть долги?', reply.table_modification())
        await state.set_state(ChangeTable.debt)
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def debt(message, state):
    if message.text == 'Стоп':
        await state.clear()
        await send(message, 'Хорошо, запись данных приостановлена.', markup='menu')
    elif message.text in ['Да', 'Нет']:
        await state.update_data(debt=message.text)
        await send(message.from_user.id, 'Спасибо за информацию, сейчас бот записывает ее в Вашу таблицу...')
        await works.set_table_prod(message, [values for values in await state.get_data()])
        await state.clear()
    else:
        await send(message.from_user.id, 'Выберете предложенный вариант ответа', reply.table_modification())


async def link_two_sheets(message, state):
    try:
        if message.text == 'Отмена':
            await state.clear()
            await send(message.from_user.id, 'Хорошо, запись остановлена. Информацию о ваших таблицах вы можете узнать командой /my_table', markup='menu')
        else:
            tableId = message.text.split("/d/")[1].split("/edit")[0]
            if tableId in [await db.get_two_sheets(message.from_user.id), db.get_sheets_one(message.from_user.id)]:
                await send(message.from_user.id,
                           'Обратите внимание, что эта таблица уже задана вами. Если вы продолжите процесс, листы "Записи бота" и "Категории и разделы" не сохранятся!')

            db.change_temp_info(f'table_number: 2; {tableId}', message.from_user.id)

            await send(message.from_user.id,
                       'Хотите ли вы настроить вашу таблицу индивидуально под вас? Будут изменены некоторые разделы.',
                       markup=inline.yes_no())
            await state.clear()
    except Exception as e:
        print(e)
        await send(message.from_user.id,
                   '❗️Вы ввели неверную ссылку!\n https://docs.google.com/spreadsheets/d/..../edit/...\n'
                   'Ссылка на таблицу выглядит подобным образом')


# Редирект сюда, если пользователь нажал на один из вариантов нечеткого сравнения
async def new_key_word(message, state: FSMContext):
    await state.clear()
    if message.text == 'Добавить новую категорию или ключевое слово✅':
        await works.continuation(message, state)
    elif message.text == 'Отмена':
        await send(message.from_user.id, 'Хорошо, вы можете вернуться к работе с ботом в любой момент', markup='menu')
    else: # Если пользователь нажал не на технические кнопки, а на один из вариантов, обрабатываем его как полноценную запись
        await handler(message, state)


async def step_one_write_key(message, state: FSMContext):
    # Если нет вариантов, то берем все разделы и предлагаем в любой из них добавить то, что мы ввели
    if message.text == 'Нет, отмена':
        await send(message.from_user.id, 'Хорошо, вы можете вернуться к работе с ботом в любой момент', markup='menu')
        await state.clear()
    else:
        if message.text != 'Категория' and message.text != 'Ключевое слово':
            await state.clear()
            await handler(message, state)
            return
        tabular_data = await sheets_api.read_new('Категории и разделы', db.get_id_sheets(message.from_user.id))
        db.change_random('temp', message.text, message.from_user.id)
        # globalVar[message.from_user.id]['time_v'] = message.text
        if message.text == 'Категория':
            buttons = list(set([el[0] for el in tabular_data[1:]]))
            # db.change_random('what', db.get_random('category', message.from_user.id), message.from_user.id)
            try:
                await state.set_state(Write_Keys.step_two)
                await send(message.from_user.id,
                                       f'В какой раздел хотите добавить "{db.get_random("category", message.from_user.id)}"?', markup=reply.auto_markup(buttons, is_=False))
            except Exception:
                await send(message.from_user.id, "Возникла ошибка, попробуйте отправить сообщение еще раз", markup='menu')
        elif message.text == 'Ключевое слово':
            buttons = [f'{el[0]} - {el[1]}' for el in tabular_data[1:]]
            try:
                await state.set_state(Write_Keys.step_two)
                await send(message.from_user.id,
                                       f'В какую категорию хотите добавить ключевое слово "{db.get_random("category", message.from_user.id)}"?', markup=reply.auto_markup(buttons, is_=False))
            except Exception:
                await send(message.from_user.id, "Возникла ошибка, попробуйте отправить сообщение еще раз", markup='menu')


async def step_two_write_key(message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        await send(message.from_user.id, 'Хорошо, вы можете вернуться к работе с ботом в любой момент', markup='menu')
    else:
        tabular_data = await sheets_api.read_new('Категории и разделы', db.get_id_sheets(message.from_user.id))
        if db.get_random('temp', message.from_user.id) == 'Категория':
            for i in range(len(tabular_data)):
                if tabular_data[i][0] == message.text:
                    # Если есть такой раздел, то читаем из таблицы "Категории и разделы" столбец с этим разделом
                    db.change_random('chapter', tabular_data[i][0], message.from_user.id)
                    try:
                        await sheets_api.write_come('Категории и разделы', db.get_random('chapter', message.from_user.id), db.get_random("category", message.from_user.id).capitalize(), db.get_id_sheets(message.from_user.id))
                    except HttpError as e:
                        if 'Unable to parse range: Категории и разделы' in str(e):
                            await send(message.from_user.id, '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                                             'переименовали лист <b>Категории и разделы</b>. Либо переименуйте (создайте) этот лист, '
                                                             'либо заново добавьте таблицу в бота, бот сам создаст лист <b>Категории и разделы</b> \n'
                                                             '<u>Введите /add_tables для получения подробной информации</u>')
                        await state.clear()
                        return
                    else:
                        if (str(db.get_random('summ', message.from_user.id))[0] == '-' and str(db.get_random('summ', message.from_user.id))[1:].isdigit()) or str(db.get_random('summ', message.from_user.id)).isdigit():
                            summ = await check_sign_sum(db.get_random('chapter', message.from_user.id), db.get_random('summ', message.from_user.id))
                            try:
                                await sheets_api.write(str(await json_serial(datetime.now())), str(db.get_random('name', message.from_user.id)), db.get_random('chapter', message.from_user.id),
                                                       db.get_random('category', message.from_user.id), str(summ),
                                                       db.get_random('comment', message.from_user.id), 'Записи бота', db.get_id_sheets(message.from_user.id))
                            except HttpError as e:
                                if 'Unable to parse range: Записи бота' in str(e):
                                    await send(message.from_user.id, '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                                                     'переименовали лист <b>Записи бота</b>. Либо переименуйте (создайте) этот лист, '
                                                                     'либо заново добавьте таблицу в бота, бот сам создаст лист <b>Записи бота</b> \n'
                                                                     '<u>Введите /add_tables для получения подробной информации</u>')
                            else:
                                await send(message.from_user.id, 'Раздел: ' + db.get_random('chapter', message.from_user.id) + '\n' 
                                                         'Категория: ' + db.get_random('category', message.from_user.id) + '\n' 
                                                         f'Сумма: {summ:,} ₽\n' 
                                                         'Комментарий: ' + db.get_random('comment', message.from_user.id) + '\n'
                                                         'Записано в таблицу!', markup='menu')

                            await state.clear()
                            return
                        else:
                            await send(message.from_user.id, "Категория была добавлена, но запись нет. Введите корректную сумму!", markup='menu')
                            await state.clear()
                            return

            await send(message.from_user.id, f'Раздела "{message.text}" нет в вашей таблице, выберите из предложенного списка')
        elif db.get_random('temp', message.from_user.id) == 'Ключевое слово':
            for i in range(len(tabular_data)):
                try:
                    db.change_random('category', message.text, message.from_user.id)
                    if tabular_data[i][1] == message.text.split(' - ')[1]:
                        if len(tabular_data[i]) == 2: await sheets_api.write_new('Категории и разделы', i, db.get_random('string', message.from_user.id).capitalize(), db.get_id_sheets(message.from_user.id))
                        else:
                            try:
                                await sheets_api.write_new('Категории и разделы', i,
                                                tabular_data[i][2] + ', ' + db.get_random('string', message.from_user.id),
                                                db.get_id_sheets(message.from_user.id))
                            except HttpError as e:
                                if 'Unable to parse range: Категории и разделы' in str(e):
                                    await send(message.from_user.id,
                                               '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                               'переименовали лист <b>Категории и разделы</b>. Либо переименуйте (создайте) этот лист, '
                                               'либо заново добавьте таблицу в бота, бот сам создаст лист <b>Категории и разделы</b> \n'
                                               '<u>Введите /add_tables для получения подробной информации</u>')
                                await state.clear()
                                return
                        db.change_random('category', tabular_data[i][1], message.from_user.id)
                        db.change_random('chapter', tabular_data[i][0], message.from_user.id)
                        if (str(db.get_random('summ', message.from_user.id))[0] == '-' and str(db.get_random('summ', message.from_user.id))[1:].isdigit()) or str(db.get_random('summ', message.from_user.id)).isdigit():
                            summ = await check_sign_sum(db.get_random('chapter', message.from_user.id),
                                                    db.get_random('summ', message.from_user.id))
                            try:
                                await sheets_api.write(str(await json_serial(datetime.now())),
                                                       str(db.get_random('name', message.from_user.id)),
                                                       db.get_random('chapter', message.from_user.id),
                                                       db.get_random('category', message.from_user.id), str(summ),
                                                       db.get_random('comment', message.from_user.id), 'Записи бота',
                                                       db.get_id_sheets(message.from_user.id))
                            except HttpError as e:
                                if 'Unable to parse range: Записи бота' in str(e):
                                    await send(message.from_user.id,
                                               '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                               'переименовали лист <b>Записи бота</b>. Либо переименуйте (создайте) этот лист, '
                                               'либо заново добавьте таблицу в бота, бот сам создаст лист <b>Записи бота</b> \n'
                                               '<u>Введите /add_tables для получения подробной информации</u>')
                            else:
                                await send(message.from_user.id, 'Раздел: ' + db.get_random('chapter', message.from_user.id) + '\n' 
                                                             'Категория: ' + db.get_random('category', message.from_user.id) + '\n' 
                                                             f'Сумма: {summ:,} ₽\n' 
                                                             'Комментарий: ' + db.get_random('comment', message.from_user.id) + '\n'
                                                             'Записано в таблицу!', markup='menu')
                                await state.clear()
                                return
                        else:
                            await send(message.from_user.id,
                                       "Ключевое слово было добавлено, но запись нет. Введите корректную сумму!", markup='menu')
                            await state.clear()
                            return
                except IndexError:
                    break
            await send(message.from_user.id,
                           f'Категории "{db.get_random("category", message.from_user.id)}" нет в вашей таблице, выберите из предложенного списка')


async def text_message_support(message, state):
    await state.clear()
    if message.text == 'Отмена':
        await send(message.from_user.id, 'Бот всегда готов к вашим командам', markup='menu')
    else:
        await send(1229555610, f'Поступило предложение от {message.from_user.id}-@{message.from_user.username}:\n{message.text}')
        await send(message.from_user.id, 'Благодарим за обратную связь!', markup='menu')


async def state_voice(message, state):
    msg = {'text': await state.get_data()['text']}
    await state.clear()
    msg = dotdict(msg)
    msg.from_user = dotdict({'id': message.from_user.id, 'first_name': message.from_user.first_name})
    if message.text == 'Верно':
        await handler(msg, state)
        await send(1229555610, f'Пользователь {message.from_user.id}, {message.from_user.username} пользовался голосовым вводом')
    elif message.text == 'Неверно':
        await send(message.from_user.id, 'Просим прощения за неудобства. Вы можете обратиться к поддержке /support')
    elif message.text == 'Отмена':
        await send(message.from_user.id, 'Вы можете вернуться к работе с ботом в любое время')
