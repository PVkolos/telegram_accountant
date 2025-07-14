from googleapiclient.errors import HttpError
from helps_func.works import send, use_help, analytics
from keyboards import reply
from . import machines
from create import db
from states.states import Two_Table, Support
from helps_func import sheets_api


async def commands(message, state):
    if message.text == '/set_table':
        await set_table(message, state)
    if message.text == '/add_table_two':
        await add_table_two(message, state)
    if message.text == '/add_tables':
        await add_tables(message)
    if message.text == '/help':
        await use_help(message)
    if message.text == '/referrals':
        await referrals(message)
    if message.text == '/plans':
        await plans(message)
    if message.text == '/support':
        await support(message, state)
    if message.text == '/my_table':
        await my_table(message)
    if message.text == '/analytics':
        await analytics(message)


async def my_table(message):
    try:
        if db.get_id_sheets(message.from_user.id) and db.get_id_sheets(message.from_user.id) != 'none':
            tb_name_1 = await sheets_api.table(db.get_id_sheets(message.from_user.id))
            tb_def = db.get_def_table(message.from_user.id)
            table = 'Дополнительная'
            if tb_def == 'id_sheets': table = 'Основная'
            if table == 'Основная':
                if await db.get_two_sheets(message.from_user.id):
                    tb_name_2 = await sheets_api.table(await db.get_two_sheets(message.from_user.id))
                    text = ('Также у вас задана дополнительная таблица - '
                            f'\n<b><a href="{tb_name_2[1]}">' + str(tb_name_2[0])) + '</a></b>\n'
                else:
                    text = 'Дополнительная таблица у вас не задана. Вы можете задать ее командой /add_table_two\n'
            else:
                tb_name_2 = await sheets_api.table(db.get_sheets_one(message.from_user.id))
                text = ('Также у вас задана основная таблица - '
                            f'\n<b><a href="{tb_name_2[1]}">' + str(tb_name_2[0]))
            await send(message.from_user.id, "Ваша таблица, в которой бот делает записи:"
                                             f"\n<b><a href='{tb_name_1[1]}'>" + str(tb_name_1[0]) + f"</a></b> ({table})\n"
                                                                                                     + text +
                                             "Если хотите поменять ссылку на таблицу, можете ввести команду /add_tables\n"
                                             "Если хотите поменять таблицу по умолчанию для записей, введите <code>Изменить таблицу по умолчанию</code>")
        else:
            await send(message.from_user.id, 'Вы не указали таблицу google sheets.\n'
                                                                            'Чтобы указать таблицу для записей введите команду /add_tables')
    except HttpError as e:
        if 'Requested entity was not found' in str(e):
            await send(message.from_user.id, '❗️Возможно, ваша талица была удалена. ❗️\nЗадайте боту новую таблицу. \n'
                                             'Подробнее - /add_tables', markup='menu')
        else:
            await send(message.from_user.id,
                   'Произошла непредвиденная ошибка, попробуйте позже или сообщите админам /support', markup='menu')
        print("ошибка чтения таблицы-1, ", e)


async def support(message, state):
    await send(message.from_user.id, 'В следующем сообщении как можно подробнее текстом опишите ваше предложение или вашу жалобу.', markup=reply.support())
    await state.set_state(Support.text_message)


async def referrals(message):
    ref = await db.get_list_referrals(message.from_user.id)
    # data = db.get_status_ref(ref)
    # await send(message.from_user.id, 'Обратите внимание - на данный момент бот бесплатен для всех, но приглашайте друзей в бота '
    #                                  'по вашей реферальной ссылке, возможно бот станет платным и количество ваших рефералов будет играть роль!')

    await send(message.from_user.id, 'Обратите внимание - на данный момент бот бесплатен для всех, но приглашайте друзей в бота '
                                     'по вашей реферальной ссылке, возможно бот станет платным и количество ваших рефералов будет играть роль!'
                                     "\n🧍 Вы пригласили " + str(len(ref)) + " человек."
                                     # "\nИз них: \n✅ Купили подписку " + str(data['купили подписку']) +
                                     # "\n⚠️Проходят врмененную подписку " + str(data['врмененную подписку']) + "\n❗️Даже не активировали пробную подписку: " + str(data['не активировали']) +
                                     "\n\nВаша реферальная ссылка: <u>https://t.me/testing_youtube_bot?start=" + str(message.from_user.id) + "</u>\n\n"
                                        # "❗️<b>Напоминаем</b>❗️\nКогда вы пригласите 5 человек, которые пройдут пробный пероид и купят любую подписку, вам будет предоставлена"
                                        # " скидка в 4️⃣0️⃣% на <b>ВСЕ</b> подписки в течении всего времени!\nЕсли говорить точнее, то ежемесячная подписка"
                                        # " будет стоить 60 рублей, годовая подписка - 480, а бесконечная - 2100. "
               , markup='menu')


async def plans(message):
    await send(message.from_user.id, 'На данный момент бот полностью переписан на новый фреймворк, идет отладка и тестирование старого функционала.'
                                '\n\n⚠️Мы знаем, что у вас точно есть предложения по улучшению бота! \nПишите их нам с помощью команды /support  ⚠️', markup='menu')


async def set_table(message, state):
    await machines.set_table(message, state)


async def add_table_two(message, state):
    if not db.get_sheets_one(message.from_user.id) or db.get_sheets_one(message.from_user.id) == 'none':
        await send(message.from_user.id, 'Сначала задайте основную таблицу командой /set_table', markup='menu')
        return
    table = 'добавить вторую таблицу' if not (await db.get_two_sheets(message.from_user.id)) else 'изменить вторую таблицу'
    await send(message.from_user.id, f'Вы решили {table}. Для этого вам нужно:\n1️⃣. Предоставьте в вашей '
                                     'таблице доступ этому аккаунту на <b>редактирование</b>: <u>servis@new-project-336414.iam.gserviceaccount.com</u>\n'
                                     '2️⃣. Отправьте ссылку на вашу таблицу этому боту в следующем сообщении.',
               markup=reply.abolition_kb())

    await state.set_state(Two_Table.link)


async def add_tables(message):
    tb_def = db.get_def_table(message.from_user.id)
    if (not db.get_sheets_one(message.from_user.id) or db.get_sheets_one(message.from_user.id) == 'none') and not (await db.get_two_sheets(message.from_user.id)):
        text = 'не используется никакая'
        table2 = 'Сначала задайте основную таблицу командой /set_table, а затем вам будет предоставлена возможность добавить вторую таблицу.'
    elif tb_def == 'id_sheets':
        text = 'используется основная'
        table2 = 'Если вы хотите изменить основную таблицу, нажмите /set_table\n'
        if await db.get_two_sheets(message.from_user.id):
            table2 += 'У вас также задана дополнительная таблица, переключиться на нее вы можете, отправив текст <code>Изменить таблицу по умолчанию</code>\n\n'
        else:
            table2 += 'Дополнительная таблица у вас не задана. Задать ее вы можете командой /add_table_two\n\n'
        table2 += 'Если вы хотите получить название и ссылку вашей текущей таблицы, нажмите /my_table\n'
    elif tb_def == 'sheets2':
        text = 'используется дополнительная'
        table2 = 'Если вы хотите изменить дополнительную таблицу, нажмите /add_table_two\n'
        table2 += 'У вас также задана основная таблица, переключиться на нее вы можете, отправив текст <code>Изменить таблицу по умолчанию</code>\n'
        table2 += 'Если вы хотите изменить основную таблицу, нажмите /set_table\n\n'
        table2 += 'Если вы хотите получить название и ссылку вашей текущей таблицы, нажмите /my_table\n'

    await send(message.from_user.id, f'Сейчас {text} таблица\n{table2}', markup='menu')
