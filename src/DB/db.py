from datetime import datetime
import sqlite3
import os.path

# import requests


class DataBase:
    def __init__(self, db_name="user.db"):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, db_name)
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.connection.cursor()

    """Проверка на наличие пользователя в бд"""
    def check_user_on_db(self, id):
        with self.connection:
            result = self.cursor.execute("select id from users where tg_id = ?", (id,)).fetchall()
            return bool(len(result))

    """Добавление пользователя в бд"""
    def add_user(self, id, username):
        with self.connection:
            self.cursor.execute("insert into users (tg_id, username) values (?, ?)", (id, username,)).fetchall()
            self.connection.commit()
            # requests.post(f'http://pavell.pythonanywhere.com/add_user', json={'tg_id': id})

    """Получение текущей гугл таблицы пользователя"""
    def get_id_sheets(self, id):
        with self.connection:
            up_to_date = self.cursor.execute("select def_table from users where tg_id = ?", (id,)).fetchall()
            result = self.cursor.execute(f"select {up_to_date[0][0]} from users where tg_id = ?", (id,)).fetchall()
            if result:
                return result[0][0]
            else:
                return None

    """Получение гугл первой таблицы пользователя"""
    def get_sheets_one(self, tg):
        with self.connection:
            result = self.cursor.execute(f"select id_sheets from users where tg_id = ?", (tg,)).fetchall()
            return result[0][0]

    """Получение подписки пользователя"""
    def get_sub_user(self, id):
        with self.connection:
            result = self.cursor.execute("select type_sub from users where tg_id = ?", (id,)).fetchall()
            if result[0][0] == 'endless':
                return result
            # else:
            #     r = requests.post(f'http://pavell.pythonanywhere.com/get_sub_info', json={'tg_id': id})
            #     if r.json()['type'] == 'endless':
            #         self.update_info_sub(id, r.json()['type'])
            #         return [[r.json()['type']]]
            # return result

    """Изменение информации про подписку"""
    def update_info_sub(self, id, type_sub):
        with self.connection:
            if type_sub == 'trial': requests.post(f'http://pavell.pythonanywhere.com/trial', json={'tg_id': id})
            self.cursor.execute("update users set type_sub = ? where tg_id = ?", (type_sub, id,)).fetchall()

    """Изменение информации про дату окончания подписки"""
    def update_info_sub_date(self, id, date, one=False):
        with self.connection:
            if one: requests.post(f'http://pavell.pythonanywhere.com/update_date', json={'tg_id': id, 'date': str(date)})
            self.cursor.execute("update users set date = ? where tg_id = ?", (date, id,)).fetchall()

    """Получение даты окончания подписки"""
    def get_date_sub(self, id):
        with self.connection:
            result = self.cursor.execute("select date from users where tg_id = ?", (id,)).fetchall()
            if (datetime.now().today() <= datetime.strptime(result[0][0].strip(), '%Y-%m-%d %H:%M:%S.%f')) or self.get_sub_user(id)[0][0] == 'endless':
                return result
            else:
                r = requests.post(f'http://pavell.pythonanywhere.com/get_sub_info', json={'tg_id': id})
                if (datetime.now().today() <= datetime.strptime(r.json()['date'].strip(), '%Y-%m-%d %H:%M:%S.%f')) or (r.json()['type'] == 'endless'):
                    self.update_info_sub_date(id, r.json()['date'])
                    self.update_info_sub(id, r.json()['type'])
                    return [[r.json()['date']]]
            return result

    """Проверка. использовался ли уже пробный период"""
    def check_is_trial(self, id):
        with self.connection:
            result = self.cursor.execute("select trial from users where tg_id = ?", (id,)).fetchall()
            return True if result[0][0] == 'falsee' else False

    """Изменение значения trial"""
    def update_trial(self, id):
        with self.connection:
            result = self.cursor.execute("update users set trial = 'truee' where tg_id = ?", (id,)).fetchall()
            return result

    """Изменение ссылки на google sheets пользователя"""
    def update_link_table(self, id, link):
        with self.connection:
            self.cursor.execute("update users set id_sheets = ? where tg_id = ?", (link, id,)).fetchall()

    """Добавление реферала пользователю"""
    def add_referal(self, id_who, id_whom):
        with self.connection:
            self.cursor.execute("insert into referals (id_who, id_whom) values (?, ?)", (id_who, id_whom,)).fetchall()

    """"Проверка на присутствие пользователя в списке приглашенных"""
    def check_refer(self, id):
        with self.connection:
            result = self.cursor.execute("select id_who from referals where id_whom = ?", (id,)).fetchall()
            return not bool(len(result))

    """Получение списка рефералов"""
    async def get_list_referrals(self, id):
        with self.connection:
            result = self.cursor.execute("select id_whom from referals where id_who = ?", (id,)).fetchall()
            return result

    """Получение статуса рефералов"""
    def get_status_ref(self, ls):
        with self.connection:
            ct = {'купили подписку': 0, 'врмененную подписку': 0, 'не активировали': 0}
            for refer in ls:
                result = self.cursor.execute("select type_sub from users where tg_id = ?", (int(refer[0]),)).fetchall()
                if result[0][0] in ['endless', 'year', 'month']: ct['купили подписку'] += 1
                elif result[0][0] == 'trial': ct['врмененную подписку'] += 1
                elif result[0][0] == 'no_subscription': ct['не активировали'] += 1
            return ct

    """Получение списка всех пользователей, для рассылки сообщений от админа"""
    async def get_all_user(self):
        with self.connection:
            users = self.cursor.execute("select tg_id from users").fetchall()
            return users

    """Получение пользователей, для админа (список юзерсов, для проверки бд)"""
    async def get_all_user_for_check_admin(self):
        with self.connection:
            users = self.cursor.execute("select tg_id, type_sub, id_sheets, date, username from users").fetchall()
            return users

    """Получение второй таблицы пользователя"""
    async def get_two_sheets(self, tg_id):
        with self.connection:
            result = self.cursor.execute("select sheets2 from users where tg_id = ?", (tg_id,)).fetchall()
            return result[0][0]

    """Изменение ссылки на google sheets2 пользователя"""
    def update_link_table2(self, id, link):
        with self.connection:
            self.cursor.execute("update users set sheets2 = ? where tg_id = ?", (link, id,)).fetchall()

    """Изменение дефолтной таблицы пользователя"""
    def update_def_table(self, id, wht):
        with self.connection:
            self.cursor.execute("update users set def_table = ? where tg_id = ?", (wht, id,)).fetchall()

    """Получение дефолтной таблицы пользователя"""
    def get_def_table(self, id):
        with self.connection:
            result = self.cursor.execute("select def_table from users where tg_id = ?", (id,)).fetchall()
            return result[0][0]

    '''Изменение информации временной переменной'''
    def change_temp_info(self, text, tg_id):
        with self.connection:
            self.cursor.execute("update users set temp = ? where tg_id = ?", (text, tg_id,)).fetchall()

    """Получение временной переменной пользователя"""
    def get_temp_info(self, tg_id):
        with self.connection:
            result = self.cursor.execute("select temp from users where tg_id = ?", (tg_id,)).fetchall()
            return result[0][0]

    '''Изменение заданного поля'''
    def change_random(self, field, new_value, tg_id):
        with self.connection:
            self.cursor.execute(f"update users set {field} = ? where tg_id = ?", (new_value, tg_id,)).fetchall()

    '''Получение значения заданного поля'''
    def get_random(self, field, tg_id):
        with self.connection:
            result = self.cursor.execute(f"select {field} from users where tg_id = ?", (tg_id,)).fetchall()
            return result[0][0]
