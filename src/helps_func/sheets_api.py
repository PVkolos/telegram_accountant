import asyncio
import os.path
import datetime

import gspread
# todo gspread_asyncio

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
# from gspread_formatting import *

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, '../credentials.json')
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
SAMPLE_RANGE_NAME = 'Записи бота'
glb = {'01': 'Январь', '02': 'Февраль', '03': 'Март', '04': 'Апрель', '05': 'Май', '06': 'Июнь', '07': 'Июль', '08': 'Август', '09': 'Сентябрь', '10': 'Октябрь', '11': 'Ноябрь', '12': 'Декабрь'}


async def modification_width(start, end, size, sheetName, spreadsheetId):
    client = gspread.authorize(credentials)
    ss = client.open_by_key(spreadsheetId)
    sheetId = ss.worksheet(sheetName)._properties['sheetId']
    body = {
        "requests": [
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",
                        "startIndex": start,
                        "endIndex": end
                    },
                    "properties": {
                        "pixelSize": size
                    },
                    "fields": "pixelSize"
                }
            }
        ]
    }
    ss.batch_update(body)


async def create_table(SAMPLE_SPREADSHEET_ID, arr=None):
    service = build('sheets', 'v4', credentials=credentials)
    req1, req2 = [], []
    req1.append({'addSheet': {'properties': {'title': 'Записи бота'}}})
    req2.append({'addSheet': {'properties': {'title': 'Категории и разделы'}}})
    body1 = {'requests': req1}
    body2 = {'requests': req2}
    try:
        service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body1).execute()
    except HttpError:
        pass
    try:
        service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body2).execute()
    except HttpError as e:
        pass
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    array = {'values': [['Дата и время записи', 'Год записи', 'Месяц', 'Кто записал', 'Раздел', 'Категория', 'Сумма', 'Примечание', 'Дата записи', 'Время записи']]}
    range_ = f'{"Записи бота"}!A1:J1'
    service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption='USER_ENTERED',
                   body=array).execute()
    await modification_width(0, 10, 150, 'Записи бота', SAMPLE_SPREADSHEET_ID)
    if not arr:
        array = {'values': [['Раздел', 'Категория', 'Ключевые слова (через запятую и пробел)'],
                            ['Доходы', 'Зп'], ['Доходы', 'Подарки'], ['Доходы', 'Сдача в аренду'],
                            ['Доходы', 'Сбережения'], ['Доходы', 'Инвестиции'], ["Желания", 'Кафе'], ["Желания", 'Подарок'],
                            ["Желания", 'Самообразование'], ["Желания", 'Путешествия'], ["Желания", 'Развлечения'],
                            ['Желания', 'Хобби'], ['Желания', 'Резерв'], ['Потребность', 'Гигиена'],
                            ["Потребность", 'Еда'], ['Потребность', 'Связь'], ['Потребность', 'Одежда'],
                            ['Расходы по обязательствам', 'Кредит'], ['Расходы по обязательствам', 'ЖКХ'],
                            ['Расходы по обязательствам', 'Транспорт налог'],
                            ['Расходы по обязательствам', 'Аренда жилья']
                            ]}
    else:
        array = {'values': []}
        array['values'].append(['Раздел', 'Категория', 'Ключевые слова (через запятую и пробел)'])
        for i in range(len(arr)):
            if i + 1 == 1:
                if arr[i] == 'Да':
                    array['values'].append(['Доходы', 'Зп'])
                else:
                    array['values'].append(['Доходы', 'Зп']); array['values'].append(['Доходы', 'Аванс'])
            if i + 1 == 2:
                if arr[i] == 'Нет': array['values'].append(['Доходы', 'Другие доходы'])
            if i + 1 == 3:
                if arr[i] == 'Да': array['values'].append(['Доходы', 'Сбережения'])
                array['values'].append(['Доходы', 'Подарки']);
                array['values'].append(['Доходы', 'Сдача в аренду']);
                array['values'].append(['Доходы', 'Инвестиции'])
            if i + 1 == 4:
                if arr[i] == 'Да': array['values'].append(["Желания", 'Забегаловки'])
                array['values'].append(["Желания", 'Подарок']);
                array['values'].append(["Желания", 'Самообразование']);
                array['values'].append(["Желания", 'Развлечения']);
                array['values'].append(["Желания", 'Хобби'])
            if i + 1 == 5:
                if arr[i] == 'Да': array['values'].append(["Желания", 'Путешествия'])
            if i + 1 == 6:
                if arr[i] == 'Да': array['values'].append(["Желания", 'Резерв'])
                array['values'].append(['Потребность', 'Гигиена']);
                array['values'].append(["Потребность", 'Еда']);
                array['values'].append(['Потребность', 'Связь']);
                array['values'].append(['Потребность', 'Одежда'])
            if i + 1 == 7:
                if arr[i] == 'Да': array['values'].append(['Расходы по обязательствам', 'Кредит']); array[
                    'values'].append(['Расходы по обязательствам', 'Ипотека'])
                array['values'].append(['Расходы по обязательствам', 'ЖКХ']);
                array['values'].append(['Расходы по обязательствам', 'Аренда жилья'])
            if i + 1 == 8:
                if arr[i] == 'Да': array['values'].append(['Расходы по обязательствам', 'Транспорт налог']); array[
                    'values'].append(['Расходы по обязательствам', 'Транспорт топливо'])
            if i + 1 == 9:
                if arr[i] == 'Да': array['values'].append(['Расходы по обязательствам', 'Долг'])
    range_ = f'{"Категории и разделы"}!A1'
    service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_, valueInputOption='USER_ENTERED',
                   body=array).execute()
    await modification_width(0, 3, 300, 'Категории и разделы', SAMPLE_SPREADSHEET_ID)
    await color(SAMPLE_SPREADSHEET_ID, 'Категории и разделы', 0.33, 0.65, 0.73, 0, 1, 0, 3)
    await color(SAMPLE_SPREADSHEET_ID, 'Записи бота', 0.33, 0.65, 0.73, 0, 1, 0, 10)


# async def color(spreadsheet_id, name_sheet, r, g, b, startR, endR, startC, endC):
#     service = build('sheets', 'v4', credentials=credentials)
#     spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
#     sheetList = spreadsheet.get('sheets')
#     id_sheet = 0
#     for sheet in sheetList:
#         if sheet['properties']['title'] == name_sheet:
#             id_sheet = int(sheet['properties']['sheetId'])
#     body = {'addBanding': {
#         'bandedRange': {
#             'range': {'sheetId': id_sheet, 'startRowIndex': startR, 'endRowIndex': endR, 'startColumnIndex': startC,
#                       'endColumnIndex': endC, },
#             'rowProperties': {
#                 'headerColor': {
#                     'red': r, 'green': g, 'blue': b, 'alpha': 1,
#                 },
#                 'firstBandColor': {
#                     'red': 0, 'green': 0, 'blue': 0, 'alpha': 0,
#                 },
#                 'secondBandColor': {
#                     'red': 0, 'green': 0, 'blue': 0, 'alpha': 0, }
#             },
#         },
#     },
#     }
#     body = {'requests': body}
#     service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

async def color(spreadsheet_id, name_sheet, red, green, blue, startR, endR, startC, endC):
    """Sets the background color of a range of cells in a Google Sheet."""

    service = build('sheets', 'v4', credentials=credentials)

    # Получаем ID листа
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheetList = spreadsheet.get('sheets')
    id_sheet = None
    for sheet in sheetList:
        if sheet['properties']['title'] == name_sheet:
            id_sheet = sheet['properties']['sheetId']
            break
    if id_sheet is None:
        print(f"Лист с именем '{name_sheet}' не найден.")
        return

    # Создаем тело запроса для batchUpdate
    rows = []
    for i in range(startR, endR):  # Итерируемся по строкам
        row_values = []
        for j in range(startC, endC):  # Итерируемся по столбцам
            row_values.append({
                'userEnteredFormat': {
                    'backgroundColor': {
                        'red': red,
                        'green': green,
                        'blue': blue,
                        'alpha': 1.0
                    }
                }
            })
        rows.append({'values': row_values})

    body = {
        'requests': [
            {
                'updateCells': {
                    'range': {
                        'sheetId': id_sheet,
                        'startRowIndex': startR,  # Google Sheets API использует 0-based indexing
                        'endRowIndex': endR,
                        'startColumnIndex': startC,
                        'endColumnIndex': endC,
                    },
                    'fields': 'userEnteredFormat.backgroundColor',
                    'rows': rows
                }
            }
        ]
    }

    # Выполняем запрос
    try:
      service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
    except Exception as e:
      print(f'Произошла ошибка: {e}')



async def read(name_sheet, SAMPLE_SPREADSHEET_ID, majorDimension='COLUMNS'):
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                         range=name_sheet,
                         majorDimension=majorDimension).execute()

    # result = service.batchGet(spreadsheetId=SAMPLE_SPREADSHEET_ID, ranges=[name_sheet]).execute()
    data_from_sheet = result.get('values', [])
    return data_from_sheet


async def table(spreadsheet_id):
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    return spreadsheet['properties']['title'], spreadsheet['spreadsheetUrl']


async def clear(sheet, SAMPLE_SPREADSHEET_ID):
    n = len(await read(sheet, SAMPLE_SPREADSHEET_ID, 'ROWS'))

    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet = service.spreadsheets().get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    sheetList = spreadsheet.get('sheets')
    id_sheet = 0
    for sheetе in sheetList:
        if sheetе['properties']['title'] == sheet:
            id_sheet = int(sheetе['properties']['sheetId'])

    body = [{
        "deleteDimension": {
            "range": {
                "sheetId": id_sheet,
                "dimension": "ROWS",
                "startIndex": n - 1,
                "endIndex": n
            }
        }
    },
           ],
    body = {'requests': body}
    service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body).execute()
    del service, body, sheet, sheetе, id_sheet, n, spreadsheet, sheetList


async def read_new(name_sheet, SAMPLE_SPREADSHEET_ID, majorDimension='ROWS'):
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    result = service.get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                         range=name_sheet,
                         majorDimension=majorDimension).execute()
    data_from_sheet = result.get('values', [])
    return data_from_sheet


async def write(date, name, razd, kat, summ, prim, sheet, SAMPLE_SPREADSHEET_ID):
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    array = {'values': [[date, date.split('-')[0], glb[date.split('-')[1]], name, razd, kat, summ, prim, glb[date.split('-')[1]], date.split('T')[1]]]}
    n = len(await read(sheet, SAMPLE_SPREADSHEET_ID, 'ROWS'))
    range_ = f'{sheet}!A{n + 1}:F{n + 1}'
    service.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                   range=range_,
                   valueInputOption='USER_ENTERED',
                   body=array).execute()
    try:
        if razd == 'Обязательства' or razd == 'Расходы по обязательствам':
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.92, 0.6, 0.6, n, n + 1, 6, 7)
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.92, 0.6, 0.6, n, n + 1, 4, 5)
        elif razd == 'Потребность':
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.79, 0.85, 0.97, n, n + 1, 6, 7)
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.79, 0.85, 0.97, n, n + 1, 4, 5)
        elif razd == 'Доходы':
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.58, 0.77, 0.49, n, n + 1, 6, 7)
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.58, 0.77, 0.49, n, n + 1, 4, 5)
        elif razd == 'Желания':
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.98, 0.8, 0.61, n, n + 1, 6, 7)
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.98, 0.8, 0.61, n, n + 1, 4, 5)
        else:
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.73, 0.73, 0.73, n, n + 1, 6, 7)
            await color(SAMPLE_SPREADSHEET_ID, sheet, 0.73, 0.73, 0.73, n, n + 1, 4, 5)
    except Exception:
        pass


async def write_come(sheet, what, kt, SAMPLE_SPREADSHEET_ID):
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    array = {'values': [[what, kt]]}
    range_ = f'{sheet}!A{1}:B{1}'
    service.append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                   range=range_,
                   valueInputOption='USER_ENTERED',
                   body=array).execute()


async def write_new(sheet, n, string, SAMPLE_SPREADSHEET_ID):
    service = build('sheets', 'v4', credentials=credentials).spreadsheets().values()
    array = {'values': [[string]]}
    range_ = f'{sheet}!C{n + 1}'
    service.update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                   range=range_,
                   valueInputOption='USER_ENTERED',
                   body=array).execute()


def deletsheet(spreadsheet_id):
    service = build('sheets', 'v4', credentials=credentials)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheetList = spreadsheet.get('sheets')
    id_sheet = 0
    for sheet in sheetList:
        if sheet['properties']['title'] == 'Аналитика':
            id_sheet = int(sheet['properties']['sheetId'])
    body = [{'updateCells': {'range': {'sheetId': id_sheet}, 'fields': 'userEnteredValue'}}]
    body = {'requests': body}
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()


async def analytic(spreadsheet_id):
    service = build('sheets', 'v4', credentials=credentials)
    req1 = []
    req1.append({'addSheet': {'properties': {'title': 'Аналитика'}}})
    body1 = {'requests': req1}
    try:
        client = gspread.authorize(credentials)
        ss = client.open_by_key(spreadsheet_id)
        sheetId = ss.worksheet('Аналитика')._properties['sheetId']
        body = {
            "requests": [
                {
                    "deleteRange": {
                        "range": {
                            "sheetId": sheetId
                        },
                        "shiftDimension": "ROWS"
                    }
                }
            ]
        }
        ss.batch_update(body)
    except Exception:
        pass

    try:
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=body1).execute()
        await modification_width(0, 15, 200, 'Аналитика', spreadsheet_id)
    except HttpError:
        pass

    # deletsheet(spreadsheet_id)
    r = await read_new('Категории и разделы', spreadsheet_id)
    body_values_ = []
    buttons_ = [' ']
    total_ = dict()
    for el in r:
        if el[0] not in buttons_ and el[0] != 'Раздел':
            buttons_.append(el[0])
            total_[el[0].capitalize()] = 0
    buttons_.append('Итого')
    body_values_.append(buttons_)

    sheet_ = await read('Записи бота', spreadsheet_id, 'ROWS')
    if len(sheet_) <= 1:
        return "Ваша таблица пуста, добавьте минимум одну запись.."

    users = set()
    for sh in sheet_[1:]:
        try:
            users.add(sh[3])
        except IndexError:
            pass
    users = list(users)
    users.append('Общий результат')
    final_results = []
    for user in users:
        sheet = []
        for el in sheet_:
            try:
                if el[3] == user or user == 'Общий результат': sheet.append(el)
            except IndexError:
                pass
        body_values = body_values_.copy()
        buttons = buttons_.copy()
        total = total_.copy()

        ms = {'1': 'январь', "2": "февраль", "3": "март", "4": "апрель", "5": "май", "6": "июнь", "7": "июль",
              "8": "август",
              "9": "сентябрь", "10": "октябрь", "11": "ноябрь", "12": "декабрь"}
        my_ms = []
        my_keys = {}
        summ = {'Доходы': 0, 'Расходы': 0}
        for i in range(1, len(sheet)):
            try:
                if sheet[i][0].split('-')[0] == str(datetime.datetime.now().year):
                    if ms[str(int(sheet[i][0].split('-')[1]))] not in my_ms:
                        my_ms.append(ms[str(int(sheet[i][0].split('-')[1]))])
                        my_keys[sheet[i][0].split('-')[1]] = {el.capitalize(): 0 for el in buttons[:-1] if el not in " Раздел"}
            except (IndexError, KeyError) as e:
                print('Error analitick, q.py ', e)
                return "❗️Возникла ошибка при проведении аналитики.❗️\nЕсть несколько возможных причин:\n" \
                       "1️⃣Вы отредактировали поле <b>Дата и время записи</b> для одной (или нескольких) вашей записи, поэтому бот не может выполнить аналитику.\n" \
                       "2️⃣Проверьте, нет ли записей снизу. Возможно вы удалили часть записей, а часть осталась разорваной от основной части. Не должно быть пустых строк\n\n" \
                       "Проверьте лист <b>Записи бота</b>, если вы ничего не редактировали, обратитесь в поддержку /support"
        my_ms.append('Всего')
        for el in sheet[1:]:
            if el[0].split('-')[0] == str(datetime.datetime.now().year):
                total[el[4].capitalize()] += int(el[6])
                my_keys[el[0].split('-')[1]][el[4].capitalize()] += int(el[6])
            if el[4] == 'Доходы':
                summ['Доходы'] += int(el[6])
            else:
                summ['Расходы'] += int(el[6])

        for i in range(13):
            if f'0{i + 1}' in my_keys:
                body_values.append([my_ms[my_ms.index(ms[str(i + 1)])], *list(my_keys[f'0{i + 1}'].values()),
                                    sum(list(my_keys[f'0{i + 1}'].values()))])
        body_values.append(['Всего', *list(total.values())])
        body_values.append([])
        if user == 'Общий результат':
            body_values.append(['Суммарные доходы', summ['Доходы'], '', 'Суммарные расходы', summ['Расходы']])
        else:
            body_values.append(['Доходы пользователя', summ['Доходы'], '', 'Расходы пользователя', summ['Расходы']])

        body_values.append([])
        body_values.append([])
        final_results.append([user])
        final_results += body_values
    body = {'values': final_results}
    range_ = f'{"Аналитика"}!A1'
    service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=range_, valueInputOption='USER_ENTERED',
                                               body=body).execute()
        # await color(spreadsheet_id, 'Аналитика', 0.33, 0.65, 0.73, 1, 2, 1, len(body_values[1]) - 1)
        # await color(spreadsheet_id, 'Аналитика', 0.33, 0.65, 0.73, 2, len(my_ms) + 1, 0, 1)
    return 'ok'


if __name__ == '__main__':
    modification_width(0, 10, 150, "Записи бота", "1U-TVGrXlnpTGvbT3oLjRiSkSBKwiZ0Oa_tyelXCEANM")