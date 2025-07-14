from datetime import datetime, timedelta
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from create import bot
from keyboards import reply, inline
from googleapiclient.errors import HttpError
from create import db
from helps_func import sheets_api
from states import states


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# ID рефера
def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None


async def welc(message):
    name = message.from_user.first_name
    await send(message.from_user.id, 'Доброго времени суток ' + name + ', вы начинаете работу с Telegram ботом, по ведению учета ваших доходов/расходов. ', reply.main_kb())
    await use_help(message)
    # subscription = db.get_sub_user(message.chat.id)
    # markup = types.InlineKeyboardMarkup()
    # but1 = types.InlineKeyboardButton(text='Да', callback_data='trial')
    # markup.add(but1)
    # if subscription[0][0] == 'no_subscription':
    #     await send(message.from_user.id, name + ', вы не приобрели подписку. Хотите начать пробный период?', markup)


async def send(who, text, markup=False):
    # try:
        if markup == 'menu':
            await bot.send_message(who, text, reply_markup=reply.main_kb())
        elif markup != 'menu' and markup:
            await bot.send_message(who, text, reply_markup=markup)
        else:
            await bot.send_message(who, text)
    # except Exception as e:
    #     print(f"ERR_SEND: \n{e}")
        # await send(who, text)


async def use_help(message):
    await send(message.from_user.id,
               # 'Одна из причин, почему бедные беднеют - они не ведут учет. (Игорь Рыбаков). Когда мы ведем учет нашего состояния, мы можем заметить наши слабые места в трате денег.\n\n'
               '🙌<b>Справка по пользованию ботом (подробная инструкация ниже)</b>🙌\nДанный бот предназначен для работы с google таблицами. \n\nДля начала работы '
               'вам необходимо: \n✅ Создать новую <a href="https://docs.google.com/spreadsheets/u/0/">google sheets таблицу</a> (или выбрать из ваших существующих) '
               '\n✅ Разрешить чтение и запись аккаунту <code>servis@new-project-336414.iam.gserviceaccount.com</code> (это бот).'
               '\n✅ Отправить команду боту такого вида:\n<code>/add_tables </code>\n\n'
               'Бот сам создаст листы <b>"Категории и разделы"</b> и <b>"Записи бота".</b> На лист <b>"Категории и разделы"</b> '
               'будут внесены основные категории и разделы, которые можно будет удалять, добавлять.\n\n'
               'Далее, принцип работы таков: вы вводите <u>название категории</u> (или ключевое слово), затем <u>сумму</u>, '
               'а затем <u>примечание</u> (если есть). Примечание добавляется через "-к". Пример:\n'
               '✅ <b>зп 10000 -к аванс</b>\n✅ <b>путешествия 123000</b>\n\n'
               'Если введенное вами слово незнакомо боту (если его нет в категориях и в ключевых словах), '
               'бот предложит вам добавить это слово либо как <u>категорию</u>, либо как <u>ключевое слово</u>. У каждой категории'
               ' может быть <u>любое количество</u> ключевых слов. Они указываются в листе <b>"Категории и разделы"</b> '
               'в столбце <b>"С"</b> через запятую и пробел.\n\n'
               'По умолчанию, бот создает 4 раздела <b>(Доходы, Желания, Расходы по обязательствам, Потребность)</b>, '
               'но их <u>можно добавлять</u>. Также, можно <u>добавлять и категории, и ключевые слова</u>. Категории и '
               'ключевые слова можно добавлять <u>прямиком из бота</u>.\n\n'
               '<a href="https://telegra.ph/Podrobnaya-instrukciya-po-ispolzovaniyu-bota-05-27-2">Очень подробно про использование бота (полная инструкция)</a>\n'
               # '\n\n✅ Реферальная система ✅\nКогда вы пригласите 5 человек, которые пройдут пробный период и купят любую подписку, вам будет предоставленна '
               # ' скидка в 4️⃣0️⃣% на <b>ВСЕ</b> подписки в течении всего времени! Для более подробной информации введите /referrals\n\n🔺🔺 Будущие планы '
               # 'разработчиков об этом боте вы можете посмотреть, введя команду /plans 🔺🔺\n\n Вопросы можно задать поддержке /support\n\n '
               '🔥🔥🔥<b>Удачного пользования!)</b>🔥🔥🔥')


async def set_table_prod(message, val=None):
    try:
        table = db.get_temp_info(message.from_user.id)
        await send(message.from_user.id, 'Дайте боту несколько секунд для создания листов и заполнения их информацией)')
        try:
            await sheets_api.create_table(table.split('; ')[1], val)
        except HttpError as e:
            if 'not have permission' in str(e):
                await send(message, 'Вы не предоствили боту права доступа для чтения и редактирования таблицы!\n'
                                                 '<u>servis@new-project-336414.iam.gserviceaccount.com</u>', markup='menu')
                return
            elif 'add alternating background colors' in str(e):
                pass
            else:
                await send(message, 'Возникла ошибка. Проверите корректность вашей ссылки.', markup='menu')
                return

        if table.split('; ')[0] == 'table_number: 2':
            db.update_link_table2(message.from_user.id, table.split('; ')[1])
        else:
            db.update_link_table(message.from_user.id, table.split('; ')[1])
        await send(message.from_user.id, 'Отлично, ваша google таблица была добавлена!', markup='menu')
        await my_category(message)
    except IndexError:
        await send(message.from_user.id, '❗️Вы ввели неверную ссылку.❗️\nhttps://docs.google.com/spreadsheets/d/..../edit/...\n'
                                         'Где многоточия - там ваши данные, которые для каждого индивидуальны')


async def my_category(message):
    category = await sheets_api.read('Категории и разделы', db.get_id_sheets(message.from_user.id), majorDimension='ROWS')
    mess = 'Ваши категории/разделы/ключевые слова на данный момент:'
    for el in category:
        if el:
            mess = mess + '\n' + ' - '.join(el)
    if len(mess.split('\n')) == 1:
        await send(message.from_user.id, 'Ваш лист "Категории и разделы" пуст', markup='menu')
    else:
        await send(message.from_user.id, mess, markup='menu')


async def check_comment(message):
    if '-к' not in message.text:  # Проверка, есть ли комментарии от пользователя в записи
        if message.text.split()[0].isdigit():  # Если первое слово в записи - число, то
            category = ' '.join([el for el in message.text.split()[1:]]).lower()  # Формируем категорию
            db.change_random('summ', message.text.split()[0], message.from_user.id)  # Запоминаем сумму
        else:  # Если первое слово в записи - не число, значит формируем категорию иначе
            category = ' '.join([el for el in message.text.split()[:-1]]).lower()  # Если нет комментариев, то все кроме последнего элемента в строке - категория
            db.change_random('summ', message.text.split()[-1], message.from_user.id)  # Запоминаем сумму
        db.change_random('comment', ' ', message.from_user.id)  # Запоминаем пустой комментарий
    else:  # Если комментарий есть, то:
        if message.text.split()[0].isdigit():  # Проверка, что первый элемент строки - число
            category = ' '.join([el for el in message.text.split(' -к ')[0].split()[1:]]).lower()  # Формируем категорию
            db.change_random('summ', message.text.split(' -к ')[0].split()[0], message.from_user.id)  # Запоминаем сумму
        else:
            category = ' '.join([el for el in message.text.split(' -к ')[0].split()[:-1]]).lower()  # Если есть, то делим строку на по комментарию, а дальше как и выше написанно
            db.change_random('summ', message.text.split(' -к ')[0].split()[-1],
                             message.from_user.id)  # Запоминаем сумму
        db.change_random('comment', message.text.split(' -к ')[-1],
                         message.from_user.id)  # Запоминаем не пустой комментарий
    db.change_random('category', category, message.from_user.id)  # Запоминаем категорию


async def check_sign_sum(chapter, summ):
    if chapter != 'Доходы' and int(summ) >= 0:
        correct_sum = int(summ) * -1
    elif chapter == 'Доходы' and int(summ) < 0:
        correct_sum = int(summ) * -1
    else:
        correct_sum = int(summ)
    return correct_sum


async def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


async def categories_match(message, tabular_data):
    for el in tabular_data:  # Перебор категорий и разделов с гугл таблицы
        if db.get_random('category', message.from_user.id) == el[1].lower():  # Если категория из сообщения = категории из таблицы, то
            db.change_random('chapter', el[0], message.from_user.id)  # В поле "Разделы" записываем раздел
            try:
                db.change_random('summ',
                                 await check_sign_sum(el[0], db.get_random('summ', message.from_user.id)),
                                 message.from_user.id)  # Меняем числовой знак сумме в зависимости от раздела (Расходы или Доходы)
            except ValueError as e:
                if 'int() with base 10' in str(e):  # Если была передана некорректная сумма
                    await send(message.from_user.id, "Введите корректную сумму", markup='menu')
            else:  # Выполнится, если все корректно
                try:
                    await sheets_api.write(str(await json_serial(datetime.now())),
                                           str(db.get_random('name', message.from_user.id)),
                                           db.get_random('chapter', message.from_user.id).capitalize(),
                                           db.get_random('category', message.from_user.id).capitalize(),
                                           str(db.get_random('summ', message.from_user.id)),
                                           db.get_random('comment', message.from_user.id), 'Записи бота',
                                           db.get_id_sheets(message.from_user.id)) # Записываем в гугл таблицу
                except HttpError as e:
                    if 'Unable to parse range: Записи бота' in str(e):
                        await send(message.from_user.id, '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                                         'переименовали лист <b>Записи бота</b>. Либо переименуйте (создайте) этот лист, '
                                                         'либо заново добавьте таблицу, бот сам создаст лист <b>Записи бота</b> \n'
                                                         '<u>Введите /add_tables для получения подробной информации</u>')
                        db.change_random('is_stop', 1, message.from_user.id) # Индикатор о завершении работы для текущего ввода
                        return
                comment = db.get_random("comment", message.from_user.id) if db.get_random("comment", message.from_user.id) != " " else "Нет комментария"
                await send(message.from_user.id, 'Раздел: ' + db.get_random('chapter', message.from_user.id) + '\n' 
                                                 'Категория: ' + db.get_random('category', message.from_user.id) + '\n' 
                                                 f'Сумма: {db.get_random("summ", message.from_user.id):,} ₽ \n' 
                                                 'Комментарий: ' + comment + '\n'
                                                 'Записано в таблицу!', markup='menu')
            db.change_random('is_stop', 1, message.from_user.id) # Индикатор о завершении работы для текущего ввода
            return


async def key_words_match(message, tabular_data):
    for el in tabular_data:
        if len(el) == 3:
            if db.get_random('category', message.from_user.id) in [element.lower() for element in el[2].split(', ')]: # Есть ли введенная категория в ключевых словах таблицы
                db.change_random('chapter', el[0].capitalize(), message.from_user.id) # Запоминаем раздел
                try:
                    db.change_random('summ',
                                     await check_sign_sum(db.get_random('chapter', message.from_user.id), db.get_random('summ', message.from_user.id)),
                                     message.from_user.id)  # Меняем числовой знак сумме в зависимости от раздела (Расходы или Доходы)
                except ValueError as e:
                    if 'int() with base 10' in str(e):  # Если была передана некорректная сумма
                        await send(message.from_user.id, "Введите корректную сумму", markup='menu')
                else:
                    comment = db.get_random('category', message.from_user.id) if db.get_random('comment', message.from_user.id) == ' ' else db.get_random('comment', message.from_user.id) # Если нет комментария, то категория станет комментарием
                    db.change_random('category', el[1].capitalize(), message.from_user.id) # Запоминаем категорию
                    try:
                        await sheets_api.write(str(await json_serial(datetime.now())),
                                               str(db.get_random('name', message.from_user.id)),
                                               db.get_random('chapter', message.from_user.id).capitalize(),
                                               db.get_random('category', message.from_user.id).capitalize(),
                                               str(db.get_random('summ', message.from_user.id)),
                                               comment, 'Записи бота',
                                               db.get_id_sheets(message.from_user.id))  # Записываем в гугл таблицу
                    except HttpError as e:
                        if 'Unable to parse range: Записи бота' in str(e):
                            await send(message.from_user.id,
                                       '❗️Не удалось внести запись.❗️\n Возможно вы удалили или '
                                       'переименовали лист <b>Записи бота</b>. Либо переименуйте (создайте) этот лист, '
                                       'либо заново добавьте таблицу, бот сам создаст лист <b>Записи бота</b> \n'
                                       '<u>Введите /add_tables для получения подробной информации</u>')
                        db.change_random('is_stop', 1, message.from_user.id) # Индикатор о завершении работы для текущего ввода
                        return

                    await send(message.from_user.id, 'Раздел: ' + db.get_random('chapter', message.from_user.id) + '\n' 
                                             'Категория: ' + db.get_random('category', message.from_user.id) + '\n' 
                                             f'Сумма: {db.get_random("summ", message.from_user.id):,} ₽\n' 
                                             'Комментарий: ' + comment + '\n'
                                             'Записано в таблицу!', markup='menu')
                db.change_random('is_stop', 1, message.from_user.id) # Индикатор о завершении работы для текущего ввода
                return


'''
db.change_random('what', '', message.from_user.id)
        db.change_random('summ', 0, message.from_user.id)
        db.change_random('name', message.from_user.first_name, message.from_user.id)
        db.change_random('chapter', '', message.from_user.id) # rz
        db.change_random('category', '', message.from_user.id) # ct
        db.change_random('comment', '', message.from_user.id) # km
        db.change_random('string', '', message.from_user.id)
        db.change_random('time_v', '', message.from_user.id)
'''


async def fuzzy_comparison(message: Message, tabular_data: list, state: FSMContext):
    variants = []
    # Делаем нечеткое сравнение, добавляем в список варианты
    for el in tabular_data[1:]:
        if db.get_random('category', message.from_user.id) in el[1].lower(): # Нечеткое сравнение по категориям
            variants.append(
                f'{el[1]} {db.get_random("summ", message.from_user.id)} '
                f'{" -к " + db.get_random("comment", message.from_user.id) if db.get_random("comment", message.from_user.id) != " " else ""}'
            )
        if len(el) == 3 and db.get_random('category', message.from_user.id) in el[2].lower():  # Нечеткое сравнение по ключевым словам
            variants.append(
                f'{el[1]} {db.get_random("summ", message.from_user.id)} '
                f'{" -к " + db.get_random("comment", message.from_user.id) if db.get_random("comment", message.from_user.id) != " " else ""}'
            )
        if db.get_random('category', message.from_user.id) in el[0].lower():  # Нечеткое сравнение по разделам
            for chapter in tabular_data[1:]:
                if chapter[0].lower() == el[0].lower():
                    variants.append(
                        f'{chapter[1]} {db.get_random("summ", message.from_user.id)} '
                        f'{" -к " + db.get_random("comment", message.from_user.id) if db.get_random("comment", message.from_user.id) != " " else ""}'
                    )
    # Если варианты из нечеткого сравнения есть, то предлагаем их пользователю
    variants = list(set(variants))
    if len(variants) > 0:
        await send(message.from_user.id, 'Возможно вы имели в виду:', markup=reply.auto_markup(variants))
        await state.set_state(states.New_Key_Word.new_key_word) # Запуск машины состояний
    else: # Если нет вариантов у нечеткого сравнения, предлагаем внести слово в новую категорию или ключевое слово
        await continuation(message, state)


# Вызывается, если пользователь выбрал добавить новую категорию или если не было вариантов нечеткого сравнения
async def continuation(message, state):
    try:
        await state.set_state(states.Write_Keys.step_one)
        await send(
            message.from_user.id,
            f'Добавить "{db.get_random("category", message.from_user.id)}" как новое ключевое слово или как новую категорию? ',
            markup=reply.new_category()
        )
        db.change_random("string", db.get_random("category", message.from_user.id), message.from_user.id)
    except Exception as e:
        print(e)
        await send(message.from_user.id, "Возникла ошибка, попробуйте отправить сообщение еще раз")


async def analytics(message):
    try:
        if db.get_id_sheets(message.from_user.id) and db.get_id_sheets(message.from_user.id) != 'none': # Проверка, что юзер указал ссылку на GOOGLE SHEETS
            tb_name = await sheets_api.table(db.get_id_sheets(message.from_user.id)) # Получение ссылки на таблицу
            await send(message.from_user.id, message.from_user.first_name + ", аналитика ваших записей может занять много времени.⏳ Когда аналитика окончится, "
                                                                            " бот пришлет вам сообщение об этом. Результаты появятся в вашей таблице на листе <b>Аналитика</b>. ")
            await message.answer_sticker(r'CAACAgIAAxkBAAEE0-9ij8pvp5_JRLKwrhvusHiZpP2XTAACIwADKA9qFCdRJeeMIKQGJAQ', reply_markup=inline.delete_sticker())
            id_sh = db.get_id_sheets(message.from_user.id) # Получение id google sheets юзера
            result = await sheets_api.analytic(id_sh)
            if result == 'ok':
                await send(message.from_user.id, "✅Аналитика завершена. Её вы можете найти <a href='" + tb_name[1] + "'>в своей google sheets таблице</a> на листе <b>Аналитика</b>")
            else: await send(message.from_user.id, result)
        else:
            await send(message.from_user.id, 'Вы не указали таблицу google sheets.\n'
                                                   'Чтобы указать таблицу для записей введите команду /add_tables')
    except Exception as e:
        if 'Requested entity was not found' in str(e):
            await send(message.from_user.id, '❗️Возможно, ваша талица была удалена. ❗️\nЗадайте боту новую таблицу. \n'
                                             'Подробнее - /add_tables')
            return
        if 'not have permission' in str(e):
            await send(message.from_user.id,
                       'Вы не предоствили боту права доступа для чтения и редактирования таблицы!\n'
                       '<u>servis@new-project-336414.iam.gserviceaccount.com</u>')
            return
        await send(message.from_user.id, 'Вышла ошибка при проведении аналитики. Попробуйте позже, или обратитесь в поддержку /support')
        print('Error analytic: ', e)