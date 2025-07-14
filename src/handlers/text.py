from datetime import datetime

from create import bot, db
from helps_func.works import send, my_category, check_comment, check_sign_sum, json_serial, categories_match, key_words_match, fuzzy_comparison
from keyboards import inline
from helps_func import sheets_api
from googleapiclient.errors import HttpError


# обработка текстового ввода пользователя
async def handler(message, state): # todo
    if message.text == 'Поддержать разработчика💰':
        await send(message.from_user.id, 'Бот полностью бесплатен для всех желающих, поэтому ваш вклад в него очень значим.💯\n\n'
                               f"<a href='https://www.donationalerts.com/r/pvkolosov'>Вы можете отправить любую сумму, нажав на этот текст</a>", 'menu')
    elif db.get_id_sheets(message.from_user.id) and db.get_id_sheets(message.from_user.id) != 'none':
        if message.text == 'Удалить последнюю запись':
            await delete_entry(message)
        elif message.text == 'Изменить таблицу по умолчанию':
            await change_table(message)
        elif message.text == 'Итого за месяц':
            await month(message)
        elif message.text == 'Мои категории и разделы':
            await my_category(message)
        elif message.text == 'Посмотреть последние 30 записей':
            await thirty_entries(message)
        elif message.text == 'Дата окончания подписки':
            pass
        else: # Хендлер для обработки сообщений с расходами/доходами
            if len(message.text.split()) > 1:
                await add_new_entry(message, state)
            else:
                await send(message.from_user.id, 'Сообщения из одного слова не обрабатываются. Если не знаете, как пользоваться ботом, воспользуйтесь помощью /help', markup='menu')
    else:
        await send(message.from_user.id, 'Вы не задали таблицу для записей. Введите команду:\n/add_tables')

async def month(message):
    now = str(datetime.now()) #
    mes = now.split()[0].split('-')[1]

    sheet = await sheets_api.read('Записи бота', db.get_id_sheets(message.from_user.id), 'ROWS')
    estimation = [int(cost[6]) for cost in sheet[1:] if int(cost[0].split('-')[1]) == int(mes)]
    if not len(estimation):
        await send(message.from_user.id,
                   'В этом месяце не делали записей, поэтому не могу ничего сказать🤷‍♂️', markup='menu')
        return
    summ = sum(estimation)
    await send(message.from_user.id, f'В этом месяце {"расходы превысили доходы" if summ < 0 else "доходы превысили расходы" if summ > 0 else "доходы ровно покрыли расходы"}.\nИтого за месяц: {summ:,} ₽', markup='menu')


async def change_table(message):
    tbl = await db.get_two_sheets(message.from_user.id)
    if not db.get_id_sheets(message.from_user.id):
        await send(message.from_user.id,
                   'Вы не задали ни одной таблицы. Добавьте основную таблицу /set_table', markup='menu')
    elif not tbl:
        await send(message.from_user.id,
                   'У вас только одна таблица. Если хотите добавить вторую, нажмите: /add_table_two', markup='menu')
    else:
        tbl1 = await sheets_api.table(db.get_sheets_one(message.from_user.id))
        tbl2 = await sheets_api.table(await db.get_two_sheets(message.from_user.id))

        await send(message.from_user.id, 'Какую таблицу выбираете? Бот будет делать записи и работать в выбранной таблице', markup=inline.selection_sheets(tbl1[0], tbl2[0]))

async def delete_entry(message):
    sheet = await sheets_api.read('Записи бота', db.get_id_sheets(message.from_user.id), 'ROWS')
    if len(sheet) != 1:
        r = sheet[-1]
        await sheets_api.clear('Записи бота', db.get_id_sheets(message.from_user.id))
        await send(message.from_user.id,
                   'Запись\n' + r[0] + ', ' + r[3] + ', ' + r[4] + ', ' + r[5] + ', ' + r[6] + '\nуспешно удалена', markup='menu')
        del sheet, r
    else:
        await send(message.from_user.id, 'В вашей таблице пусто, удалять нечего', markup='menu')


async def thirty_entries(message):
    rd = await sheets_api.read('Записи бота', db.get_id_sheets(message.from_user.id), 'ROWS')
    if len(rd) != 1:
        if (len(rd) - 30) >= 0:
            msg = ''
            for i in range(len(rd) - 30, len(rd)):
                try:
                    msg += (str(i) + ") " + rd[i][0] + ', ' + rd[i][3] + ', ' + rd[i][4] + ', ' +
                            rd[i][5] + ', ' + rd[i][6] + ', ' + rd[i][7] + '\n')
                except IndexError:
                    pass
            await send(message.from_user.id, msg, markup='menu')
        else:
            msg = ''
            for i in range(1, len(rd)):
                try:
                    msg += str(i + 1) + ") " + rd[i][0] + ' ' + rd[i][1] + ' ' + rd[i][2] + ' ' + \
                           rd[i][3] + ' ' + rd[i][4] + ' ' + rd[i][5] + '\n'
                except IndexError:
                    pass
            await send(message.from_user.id, msg, markup='menu')
    else:
        await send(message.from_user.id, 'В таблице пусто', markup='menu')


async def add_new_entry(message, state):
    try:
        tabular_data = await sheets_api.read_new('Категории и разделы', db.get_id_sheets(message.from_user.id)) # Список со строками из листа "Категории и разделы", заполняется ниже
    except HttpError as e:
        if 'Unable to parse range: Категории и разделы' in str(e):
            await send(message.from_user.id, '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                             'переименовали лист <b>Категории и разделы</b>. Либо переименуйте (создайте) этот лист, '
                                             'либо заново добавьте таблицу в бота, бот сам создаст лист <b>Категории и разделы</b> \n'
                                             '<u>Введите /add_tables для получения подробной информации</u>', markup='menu')
        elif 'Requested entity was not found' in str(e):
            await send(message.from_user.id, '❗️Возможно, ваша талица была удалена. ❗️\nЗадайте боту новую таблицу. \n'
                                             'Подробнее - /add_tables', markup='menu')
        elif 'not have permission' in str(e):
            await send(message.from_user.id,
                       'Вы не предоставили боту права доступа для чтения и редактирования таблицы!\n'
                       '<u>servis@new-project-336414.iam.gserviceaccount.com</u>', markup='menu')
        elif 'Internal error encountered' in str(e):
            await send(message.from_user.id, 'Ваша таблица временно не может быть прочтена. Попробуйте позже', markup='menu')
        else:
            await send(message.from_user.id, 'Произошла непредвиденная ошибка, попробуйте позже или сообщите админам (/support)', markup='menu')
        print("ошибка чтения таблицы, ", e)
    else:
        ''' задаем значения по умолчанию перед обработкой сообщения '''
        db.change_random('what', '', message.from_user.id)
        db.change_random('summ', 0, message.from_user.id)
        db.change_random('name', message.from_user.first_name, message.from_user.id)
        db.change_random('chapter', '', message.from_user.id)
        db.change_random('category', '', message.from_user.id)
        db.change_random('comment', '', message.from_user.id)
        db.change_random('string', '', message.from_user.id)
        db.change_random('time_v', '', message.from_user.id)

        await check_comment(message) # Формируем и запоминаем комментарий, сумму и категорию в зависимости от наличия комментария
        await categories_match(message, tabular_data) # Если категория из записи совпала с категорией в таблице, создаем запись

        if not db.get_random('is_stop', message.from_user.id): # Если прошлая функция не прервалась по ошибке или не записала в таблицу
            await key_words_match(message, tabular_data) # Если категория из записи совпала с ключевым словом в таблице, создаем запись

            if not db.get_random('is_stop', message.from_user.id):
                await fuzzy_comparison(message, tabular_data, state)
            else:
                db.change_random('is_stop', 0, message.from_user.id)
        else:
            db.change_random('is_stop', 0, message.from_user.id)
