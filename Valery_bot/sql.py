import sqlite3
import os
import pandas as pd
import hashlib
import time
import random

def create_tables():
    find = """
    CREATE TABLE IF NOT EXISTS users(
    userid INTEGER,
    teguser TEXT,
    admin TEXT
    );
    CREATE TABLE IF NOT EXISTS accesser(
    userid INTEGER,
    trys INTEGER
    );
    """
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.executescript(find)
    find = """
        CREATE TABLE IF NOT EXISTS checker(
        code TEXT,
        manyuse INTEGER
        );
        CREATE TABLE IF NOT EXISTS reviews(
        questioncategory TEXT,
        question TEXT,
        result INTEGER,
        comment TEXT,
        mark TEXT,
        Timestamp DATE DEFAULT (datetime('now','localtime'))
        );
        """
    with sqlite3.connect('check.db') as db:
        cursor = db.cursor()
        cursor.executescript(find)



def reg_user(user_id, teg_user):
    find = 'SELECT teguser FROM users WHERE userid = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [user_id])
        alpha = cursor.fetchone()
        if alpha is None:
            find = 'INSERT INTO users (userid, teguser, admin) VALUES (?, ?, ?)'
            cursor.execute(find, [user_id, teg_user, 'no'])
            return 'new'
        elif teg_user != alpha[0]:
            find = 'UPDATE users SET teguser =? WHERE userid = ?'
            cursor.execute(find, [teg_user, user_id])
            db.commit()
        return 'old'

def give_admin(teg_user):
    find = 'SELECT admin FROM users WHERE teguser = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [teg_user])
        alpha = cursor.fetchone()
        if alpha is not None:
            if alpha[0] != 'no':
                return f'@{teg_user} уже является администратором!'
            find = ('UPDATE users SET admin = ? WHERE teguser = ?')
            cursor.execute(find, ['yes', teg_user])
            db.commit()
            return 'Добавил в список администраторов'
        return f'Я не нашел такого пользователя\nПусть @{teg_user} отправит мне любое сообщение'

def remove_admin(teg_user):
    find = 'SELECT admin FROM users WHERE teguser = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [teg_user])
        alpha = cursor.fetchone()
        if alpha is None:
            return f'Я не нашел такого администратора по тегу\nПусть @{teg_user} отправит мне любое сообщение'
        elif alpha[0] == 'no':
            return f'@{teg_user} не был администратором'
    find = 'UPDATE users SET admin = ? WHERE teguser = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, ['no', teg_user])
        db.commit()
    return 'Удалил из списка администраторов'

def info_user(teg_user):
    find = 'SELECT admin FROM users WHERE teguser = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [teg_user])
        alpha = cursor.fetchone()
        if alpha is not None:
            if alpha[0] != 'no':
                return f'@{teg_user} - администратор'
            return f'@{teg_user} - пользователь'
        return f'Я не нашел данные о @{teg_user}'
            


def get_admins():
    find = 'SELECT userid FROM users WHERE admin = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, ['yes'])
        alpha = cursor.fetchall()
        return alpha


def new_in_sql():
    try:
        try:
            os.remove('ninfo.db')
        except Exception:
            pass
        with pd.ExcelFile('bd.xlsx') as xls:
            sheets = xls.sheet_names
            for sheet in sheets:
                xls_df = pd.read_excel(xls, sheet_name=sheet)  # Use different variable name to avoid overwriting xls
                columns = []
                for column in xls_df.columns:
                    column = str(column)
                    column = column.replace('№', 'numberid')
                    column = column.replace(' ', '')
                    column = column.lower()
                    if len(column) > 18:
                        column = column[:17]
                    columns.append(column)
                budy = []
                for index, row in xls_df.iterrows():
                    use = row.tolist()
                    budy.append(use)
                sheet = str(sheet)
                sheet = sheet.replace(' ', '')
                sheet = sheet.replace('№', 'namerid')
                sheet = sheet.lower()
                if len(sheet) > 18:
                    sheet = sheet[:17]
                find = f'CREATE TABLE IF NOT EXISTS {sheet} ('
                for posission in range(0, len(columns)):
                    if posission != len(columns)-1:
                        find += f'{columns[posission]} TEXT, '
                    else:
                        find += f'{columns[posission]} TEXT);'
                with sqlite3.connect('ninfo.db') as db:
                    cursor = db.cursor()
                    cursor.executescript(find)
                    db.commit()
                for new in budy:
                    find = f'INSERT INTO {sheet} ('
                    for posission in range(0, len(columns)):
                        if posission != len(columns) - 1:
                            find += f'{columns[posission]}, '
                        else:
                            find += f'{columns[posission]}) VALUES ({"?, "*(len(columns)-1)}?)'
                    with sqlite3.connect('ninfo.db') as db:
                        cursor = db.cursor()
                        cursor.execute(find, new)
                        db.commit()
                xls_df.to_excel('bd.xlsx', index=False)
        xls_df.to_excel('bd.xlsx', index=False)
    except Exception as error:
        print(error)
        return 'N'
    return 'Y'


def shablon(user_id):
    lol = {'user_id': user_id,
           'категориявопросов': None,
           'вопрос': None,
           'глоссарий': None,
           'термин': None
           }
    return lol


def buttons_shablon(text, number):
    lol = {
        'text': f'{text}',
        'callback_data': f'button{number+1}'
    }
    return lol


def select_column(table, column):
    find = f'SELECT {column} from {table}'
    with sqlite3.connect('questions.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [])
        alpha = cursor.fetchall()
        return alpha

def get_info(table, column, where, use_it):
    find = f'SELECT {column} from {table} where {where} = ?'
    with sqlite3.connect('questions.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [use_it])
        alpha = cursor.fetchone()
        return alpha


def get_all_info(table, column, where, use_it):
    find = f'SELECT {column} from {table} where {where} = ?'
    with sqlite3.connect('questions.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [use_it])
        alpha = cursor.fetchall()
        return alpha

def get_accuracy_info(table, column, where_mass = None, use_it_mass = None):
    find = f'SELECT {column} FROM {table}'
    if where_mass is not None and use_it_mass is not None:
        if len(where_mass) != len(use_it_mass):
            return 'длина поиска != входным данным'
        find += ' WHERE '
        for i in range(0, len(where_mass)):
            if i != len(where_mass)-1:
                find +=f'{where_mass[i]} = ? AND '
            else:
                find += f'{where_mass[i]} = ?'
    if use_it_mass is None:
        use_it_mass = []
    with sqlite3.connect('questions.db') as db:
        cursor = db.cursor()
        cursor.execute(find, use_it_mass)
        alpha = cursor.fetchall()
        return alpha


def get_alphabet(number):
    alphabet = '0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟'
    number = str(number)
    newnumber = ''
    if not number.isdigit():
        return "N"
    if number != '10' and '-' not in number:
        for count in number:
            count = (int(count))*3
            newnumber += alphabet[count:count+3]
    elif number == '10':
        count = (int(number))*3
        newnumber += alphabet[count:count+4]
    else:
        newnumber = 'N'
    return newnumber

def de_alphabet(input_string):
    try:
        result = ''
        alphabet = '0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟'
        for i in range(0, len(input_string), 3):
            emoji_start = input_string[i:i + 3]
            emoji = alphabet.find(emoji_start) // 3
            if 0 <= emoji <= 10:
                result += str(emoji)
            else:
                return 'Invalid emoji'
        return result
    except Exception:
        return 'Error'


def new_password(user_id, many, update_id):
    while True:
        try:
            input_string = f"{time.time()}{str(user_id)}{str(random.randint(0, 9999999))}{str(update_id)}"
            hash_object = hashlib.sha256(input_string.encode())
            key_auth = hash_object.hexdigest()
            find = 'SELECT manyuse FROM checker WHERE code = ?'
            with sqlite3.connect('check.db') as db:
                cursor = db.cursor()
                cursor.execute(find, [key_auth])
                alpha = cursor.fetchone()
            if alpha is None:
                find = 'INSERT INTO checker (code, manyuse) VALUES (?, ?)'
                with sqlite3.connect('check.db') as db:
                    cursor = db.cursor()
                    cursor.execute(find, [key_auth, many])
                    db.commit()  # Commit the changes
                    return key_auth
        except Exception as e:
            print("Ошибка:", e)
            return 'ERROR'


def use_passowrd(user_id, code):
    find = 'SELECT trys FROM accesser WHERE userid = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [user_id])
        alpha = cursor.fetchone()
    if alpha is not None:
        alpha = alpha[0]
        if alpha < 1:
            return 'N'
    else:
        return 'N'
    find = 'SELECT manyuse FROM checker WHERE code = ?'
    with sqlite3.connect('check.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [code])
        alpha = cursor.fetchone()
    if alpha is None:
        return 'N'
    alpha = int(alpha[0])
    if alpha < 1:
        return 'EU'
    find = 'UPDATE checker SET manyuse = ? WHERE code = ?'
    with sqlite3.connect('check.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [alpha-1, code])
        db.commit()
        return 'Y'


def first_registration(userid):
    find = 'SELECT trys FROM accesser WHERE userid = ?'
    with sqlite3.connect('info.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [userid])
        alpha = cursor.fetchone()
    if alpha is None:
        find = 'INSERT INTO accesser (userid, trys) VALUES (?, ?)'
        with sqlite3.connect('info.db') as db:
            cursor = db.cursor()
            cursor.execute(find, [userid, 3])
            db.commit()
        return 'new'
    return 'old'


def error_password(userid):
    find = 'UPDATE accesser SET trys = trys - ? WHERE userid = ?'
    with sqlite3.connect('check.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [1, userid])
        db.commit()


def save_answer(conteiner):
    questioncategory = conteiner['категориявопросов']
    question = conteiner['вопрос'][conteiner['вопрос'].find('+')+1:]
    if conteiner['вопрос'][:conteiner['вопрос'].find('+')] == '':
        result = 1
        comment = 'None'
    else:
        result = 0
        comment = conteiner['вопрос'][:conteiner['вопрос'].find(' - отзыв+')]
    find = 'INSERT INTO reviews (questioncategory, question, result, comment, mark) VALUES (?, ?, ?, ?, ?)'
    with sqlite3.connect('check.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [questioncategory, question, result, comment, 'N'])
        db.commit()


def get_last_comment():
    find = "SELECT * FROM reviews WHERE comment != 'None' AND mark = 'N'"
    with sqlite3.connect('check.db') as db:
        cursor = db.cursor()
        cursor.execute(find, [])
        alpha = cursor.fetchall()
    if len(alpha) > 0:
        find = 'UPDATE reviews SET mark = ? WHERE questioncategory = ? AND question = ? AND result = ? AND comment = ? AND mark = ?'
        for update in alpha:
            questioncategory, question, result, comment, mark, worktime = update
            with sqlite3.connect('check.db') as db:
                cursor = db.cursor()
                cursor.execute(find, ['Y', questioncategory, question, result, comment, mark])
                db.commit()
        return alpha
    return 'N'

def get_acurancy_comment(many):
    try:
        like_how = []
        columns = ['Категория вопроса', 'Вопрос', 'Комментарий пользователя']
        if many == '/all':
            columns.append('Результат')
            what = 'questioncategory, question, comment, result'
            many = ''
        else:
            columns.append('Время получения')
            what = 'questioncategory, question, comment, Timestamp'
            many = 'WHERE result = ?'
            like_how = [0]
        with sqlite3.connect('check.db') as db:
            find = f'SELECT {what} FROM reviews {many}'
            cursor = db.cursor()
            cursor.execute(find, like_how)
            data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        df.to_excel('output.xlsx', index=False)
    except Exception as error:
        print(error)