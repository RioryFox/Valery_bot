import requests
from datetime import datetime
import pytz
import json
from sql import *



token = '6540959298:AAHfEFnHEcXxglWseUdLSSGWRJ-oLhoYx8o'
URL = 'https://api.telegram.org/bot'
update_id = None


def send_document(chat_id, document_path, caption=None):
    url = f'https://api.telegram.org/bot{token}/sendDocument'
    params = {
        'chat_id': chat_id,
        'caption': caption
    }
    files = {
        'document': open(document_path, 'rb')
    }
    requests.post(url, params=params, files=files)


def listen(URL, token, offset=0):
    while True:
        try:
            request = requests.get(f'{URL}{token}/getUpdates?offset={offset}').json()
            return request['result']
        except Exception:
            time.sleep(1)
            tz = pytz.timezone('Europe/Moscow')
            moscow = datetime.now(tz)
            print(f'Error getting updates, {moscow}')


def send_message(chat_id, text, buttons=None, document_path=None):
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    if document_path is not None:
        url = f'https://api.telegram.org/bot{token}/sendDocument'
        params = {
            'chat_id': chat_id,
            'document': open(document_path, 'rb')
        }
    elif buttons is None:
        params = {
            'chat_id': chat_id,
            'text': text
        }
    else:
        inline = {
            'inline_keyboard': buttons
        }
        params = {
            'chat_id': chat_id,
            'text': text,
            'reply_markup': json.dumps(inline)
        }

    requests.get(url, params=params)


try:
    last_info = listen(URL, token)
except Exception:
    last_info = ''

while len(last_info) == 0:
    try:
        last_info = listen(URL, token)
        time.sleep(1)
    except Exception:
        time.sleep(1)

while True:
    try:
        last_update_info = last_info[len(last_info) - 1]['update_id']
        tz = pytz.timezone('Europe/Moscow')
        moscow = datetime.now(tz)
        print(f'----start work at: {moscow} - by Moscow time----')
        break
    except Exception:
        continue

create_tables()
print(new_password(1231231, 1, 323121))
key = None
users = []

while True:
    try:
        new_info = listen(URL, token, last_update_info)
        while len(new_info) == 0:
            new_info = listen(URL, token, last_update_info)
            time.sleep(1)
        now_update_info = new_info[len(new_info) - 1].get('update_id', None)
        if now_update_info > last_update_info:
            for elemen in new_info:
                try:
                    update_id = elemen.get('update_id', None)
                    if update_id > last_update_info:
                        msg = ''
                        if 'message' in elemen:
                            about_msg = elemen['message']
                            user_id = about_msg['from']['id']
                            chat_id = about_msg['chat']['id']
                            try:
                                teg_user = about_msg['from']['username']
                            except Exception:
                                teg_user = None
                            msg_id = about_msg['message_id']
                            first_name = about_msg['from']['first_name']
                            try:
                                last_name = about_msg['from']['last_name']
                            except Exception as error:
                                last_name = None
                            try:
                                msg = about_msg['text']
                            except Exception:
                                msg = ''
                            if msg == '':
                                try:
                                    msg = elemen['message']['caption']
                                except Exception:
                                    msg = ''
                        else:
                            about_msg = elemen['callback_query']
                            user_id = about_msg['from']['id']
                            msg_id = about_msg['message']['message_id']
                            try:
                                teg_user = about_msg['from']['username']
                            except Exception:
                                teg_user = None
                            first_name = about_msg['from']['first_name']
                            try:
                                last_name = about_msg['from']['last_name']
                            except Exception:
                                last_name = None
                            about_msg = about_msg['message']
                            chat_id = about_msg['chat']['id']
                            try:
                                data = elemen['callback_query']['data']
                                variants = elemen['callback_query']['message']['reply_markup']['inline_keyboard']
                                stop = None
                                for elements in variants:
                                    for string in elements:
                                        callback = string['callback_data']
                                        if callback == data:
                                            msg = string['text']
                                            stop = 'Y'
                                            break
                                    if stop is not None:
                                        break
                            except Exception:
                                msg = ''
                        is_admin = info_user(teg_user)
                        password = None
                        if f'Я не нашел данные о @{teg_user}' == is_admin:
                            msg = msg.replace(' ', '')
                            if 'old' == first_registration(user_id):
                                password = use_passowrd(user_id, msg)
                                if password != 'Y':
                                    error_password(user_id)
                            else:
                                send_message(user_id,
                                    'Привет, жду твой ключ доступа, который ты получил от администратора \nВНИМАНИЕ!!! У вас лишь 3 попытки верно ввести ключ, до тех пор, пока вы не авторизованы - ваши сообщения будут расцениваться как ключи!\n\nКлюч вводится сообщением без лишних файлов, символов или пробелов!')
                        if f'Я не нашел данные о @{teg_user}' != is_admin or password == 'Y':
                            status = reg_user(user_id, teg_user)
                            if status == 'new':
                                send_message(user_id, 'Привет! Я бот-помощник. Чтобы я смог Вам помочь, нажмите на пункт меню с темой Вашего вопроса 👇')
                                result = list(set(get_accuracy_info('вопросы', 'категориявопросов')))
                                use_buttons = []
                                buttons = []
                                for number in range(len(result) + 1):
                                    if number != len(result):
                                        if number > 0 and number % 2 == 0:
                                            buttons.append(use_buttons)
                                            use_buttons = []
                                        use_buttons.append(
                                            buttons_shablon(result[number][0], number))
                                    if number == len(result):
                                        if number > 0 and number % 2 == 0:
                                            buttons.append(use_buttons)
                                            use_buttons = []
                                        use_buttons.append(buttons_shablon('Сокращения', number))
                                if use_buttons:
                                    buttons.append(use_buttons)
                                send_message(user_id, 'Добро пожаловать в бота-помощника, что вас интересует?', buttons)
                                users.append(shablon(user_id))
                            else:
                                if len(users) == 0:
                                    users.append(shablon(user_id))
                                else:
                                    a = 0
                                    for a in range(0, len(users)):
                                        if users[a].get('user_id', None) == user_id:
                                            a = -1
                                            break
                                    if a != -1:
                                        users.append(shablon(user_id))
                                for conteiner in users:
                                    if conteiner['user_id'] == user_id:
                                        if msg == '/start' or msg == '⬅️' or msg.lower() == 'назад':
                                            if conteiner['глоссарий'] == '+':
                                                send_message(user_id, '❌Вы вышли из режима "сокращения"')
                                            elif conteiner['глоссарий'] == '-':
                                                send_message(user_id, '❌Вы вышли из режима "вопрос"')
                                            result = list(set(get_accuracy_info('вопросы', 'категориявопросов')))
                                            use_buttons = []
                                            buttons = []
                                            for number in range(len(result) + 1):
                                                if number != len(result):
                                                    if number > 0 and number % 2 == 0:
                                                        buttons.append(use_buttons)
                                                        use_buttons = []
                                                    use_buttons.append(
                                                        buttons_shablon(result[number][0], number))
                                                if number == len(result):
                                                    if number > 0 and number % 2 == 0:
                                                        buttons.append(use_buttons)
                                                        use_buttons = []
                                                    use_buttons.append(buttons_shablon('Сокращения', number))
                                            if use_buttons:
                                                buttons.append(use_buttons)
                                            send_message(user_id, 'Выберите режим работы бота:', buttons)
                                            conteiner['категориявопросов'] = None
                                            conteiner['вопрос'] = None
                                            conteiner['глоссарий'] = None
                                            conteiner['термин'] = None
                                        elif conteiner['глоссарий'] is None:
                                            if msg.lower() == 'сокращения':
                                                conteiner['глоссарий'] = '+'
                                                conteiner['категориявопросов'] = '-'
                                                result = select_column('сокращения', 'сокращение')
                                                use_buttons = []
                                                buttons = []
                                                for number in range(len(result) + 1):
                                                    if number != len(result):
                                                        if number > 0 and number % 4 == 0:
                                                            buttons.append(use_buttons)
                                                            use_buttons = []
                                                        use_buttons.append(
                                                            buttons_shablon(result[number][0], number))
                                                    if number == len(result):
                                                        if number > 0 and number % 3 == 0:
                                                            buttons.append(use_buttons)
                                                            use_buttons = []
                                                        use_buttons.append(buttons_shablon('⬅️', number))
                                                if use_buttons:
                                                    buttons.append(use_buttons)
                                                send_message(user_id, 'Какое сокращение вас интересует?', buttons)
                                            else:
                                                result = get_all_info('вопросы', 'вопрос', 'категориявопросов', msg)
                                                if result is not None and len(result) > 0:
                                                    conteiner['глоссарий'] = '-'
                                                    conteiner['категориявопросов'] = msg
                                                    use_buttons = []
                                                    buttons = []
                                                    save = f'Какой вопрос вас интересует в разделе {msg}:'
                                                    for number in range(len(result)+1):
                                                        if number != len(result):
                                                            save += f'\n{get_alphabet(number+1)} - {result[number][0]}'
                                                            if number > 0 and number % 3 == 0:
                                                                buttons.append(use_buttons)
                                                                use_buttons = []
                                                            use_buttons.append(buttons_shablon(f'{get_alphabet(number+1)}', number))
                                                        if number == len(result):
                                                            if number > 0 and number % 3 == 0:
                                                                buttons.append(use_buttons)
                                                                use_buttons = []
                                                            use_buttons.append(buttons_shablon('⬅️', number))
                                                    if use_buttons:
                                                        buttons.append(use_buttons)
                                                    send_message(user_id, save, buttons)
                                                else:
                                                    result = list(
                                                        set(get_accuracy_info('вопросы', 'категориявопросов')))
                                                    use_buttons = []
                                                    buttons = []
                                                    for number in range(len(result) + 1):
                                                        if number != len(result):
                                                            if number > 0 and number % 2 == 0:
                                                                buttons.append(use_buttons)
                                                                use_buttons = []
                                                            use_buttons.append(
                                                                buttons_shablon(result[number][0], number))
                                                        if number == len(result):
                                                            if number > 0 and number % 2 == 0:
                                                                buttons.append(use_buttons)
                                                                use_buttons = []
                                                            use_buttons.append(buttons_shablon('Сокращения', number))
                                                    if use_buttons:
                                                        buttons.append(use_buttons)
                                                    send_message(user_id, 'Пожалуйста, выберите категорию вопроса из списка:', buttons)
                                        else:
                                            if conteiner['глоссарий'] == '+' and conteiner['термин'] is None:
                                                result = get_info('сокращения', 'расшифровка', 'сокращение', msg)
                                                if result is not None:
                                                    send_message(user_id, f'{msg} - это {result[0]}')
                                                else:
                                                    send_message(user_id, 'Такого определения нет в глоссарии!\nЕсли вы ввели все данные корректно, то просим нажать на синее слово👇\n -> -> /start <- <- \nИ попробовать новь - это должно помочь, спасибо')
                                            elif conteiner['глоссарий'] == '-' and conteiner['вопрос'] is None:
                                                result = get_accuracy_info('вопросы', 'вопрос', ['категориявопросов'], [conteiner['категориявопросов']])
                                                if not msg.isdigit():
                                                    try:
                                                        maby_msg = de_alphabet(msg)
                                                        if maby_msg.isdigit():
                                                            msg = maby_msg
                                                    except Exception:
                                                        continue
                                                if msg.isdigit() and len(result) > 0:
                                                    try:
                                                        conteiner['вопрос'] = result[int(msg) - 1][0]
                                                    except Exception:
                                                        conteiner['вопрос'] = None
                                                    try:
                                                        result = get_accuracy_info('вопросы', 'ответ', ['категориявопросов', 'вопрос'], [conteiner['категориявопросов'], result[int(msg)-1][0]])
                                                    except Exception as error:
                                                        result = 'N'
                                                    if result is None or result == 'N' or len(result)>1 or conteiner['вопрос']  is None:
                                                        send_message(user_id, 'Введены некорректные данные!')
                                                        conteiner['вопрос'] = None
                                                    else:
                                                        maby_pdf = get_accuracy_info('вопросы', 'numberid',
                                                                                   ['категориявопросов', 'вопрос', 'ответ'],
                                                                                   [conteiner['категориявопросов'], conteiner['вопрос'], result[0][0]])
                                                        if len(maby_pdf) != 1:
                                                            maby_pdf = -1
                                                        else:
                                                            maby_pdf = maby_pdf[0][0]
                                                        if os.path.exists(f'{maby_pdf}.pdf'):
                                                            result = str(result[0][0]).replace(":)", "😃").replace(";)", "😉")
                                                            send_document(user_id, f'{maby_pdf}.pdf', f'Ответ: {result}')
                                                        else:
                                                            send_message(user_id, f'Ответ: {result[0][0]}')
                                                        if conteiner['вопрос'].lower() == 'назначение системы':
                                                            conteiner['вопрос'] = None
                                                elif len(result) > 0 and not msg.isdigit():
                                                    send_message(user_id, '😐Непредвиденная ошибка!\nПростите, просим нажать на синее слово👇\n -> -> /start <- <- \nИ попробовать новь - это должно помочь, спасибо')
                                                else:
                                                    send_message(user_id, 'Пожалуйста - укажите номер интересующего вас вопроса!')
                                            if conteiner['глоссарий'] is not None and conteiner['вопрос'] is not None:
                                                if '+' not in conteiner['вопрос']:
                                                    buttons = [
                                                        [
                                                            {
                                                                'text': 'Да',
                                                                'callback_data': 'button1'
                                                            },
                                                            {
                                                                'text': 'Нет',
                                                                'callback_data': 'button2'
                                                            }
                                                        ]
                                                    ]
                                                    send_message(user_id, 'Был ли наш ответ понятным и полезным❓', buttons)
                                                    conteiner['вопрос'] = '+' + conteiner['вопрос']
                                                if (msg.lower() == 'да' or msg.lower() == 'нет') and '+' == conteiner['вопрос'][0:1] and len(conteiner['вопрос']) > 1:
                                                    if msg.lower() == 'да':
                                                        try:
                                                            save_answer(conteiner)
                                                        except Exception as error:
                                                            print(error)
                                                        send_message(user_id,
                                                                     '😉Мы рады что смогли вам помочь!')
                                                        conteiner['категориявопросов'] = None
                                                        conteiner['вопрос'] = None
                                                        conteiner['глоссарий'] = None
                                                        conteiner['термин'] = None
                                                        result = list(
                                                            set(get_accuracy_info('вопросы', 'категориявопросов')))
                                                        use_buttons = []
                                                        buttons = []
                                                        for number in range(len(result) + 1):
                                                            if number != len(result):
                                                                if number > 0 and number % 2 == 0:
                                                                    buttons.append(use_buttons)
                                                                    use_buttons = []
                                                                use_buttons.append(
                                                                    buttons_shablon(result[number][0], number))
                                                            if number == len(result):
                                                                if number > 0 and number % 2 == 0:
                                                                    buttons.append(use_buttons)
                                                                    use_buttons = []
                                                                use_buttons.append(
                                                                    buttons_shablon('Сокращения', number))
                                                        if use_buttons:
                                                            buttons.append(use_buttons)
                                                        send_message(user_id, 'Выберите режим работы бота:', buttons)
                                                    elif msg.lower() == 'нет':
                                                        send_message(user_id,
                                                                     '😔Нам жаль что наш ответ вам не помог, напишите что нам следует изменить?')
                                                        conteiner['вопрос'] = ' - отзыв' + conteiner['вопрос']
                                                elif ' - отзыв' == conteiner['вопрос'][:len(' - отзыв')]:
                                                    conteiner['вопрос'] = msg + conteiner['вопрос']
                                                    try:
                                                        save_answer(conteiner)
                                                    except Exception as error:
                                                        print(error)
                                                    send_message(user_id, 'Спасибо за ваш ответ, обещаем исправить этот недочет😉')
                                                    conteiner['категориявопросов'] = None
                                                    conteiner['вопрос'] = None
                                                    conteiner['глоссарий'] = None
                                                    conteiner['термин'] = None
                                                    result = list(
                                                        set(get_accuracy_info('вопросы', 'категориявопросов')))
                                                    use_buttons = []
                                                    buttons = []
                                                    for number in range(len(result) + 1):
                                                        if number != len(result):
                                                            if number > 0 and number % 2 == 0:
                                                                buttons.append(use_buttons)
                                                                use_buttons = []
                                                            use_buttons.append(
                                                                buttons_shablon(result[number][0], number))
                                                        if number == len(result):
                                                            if number > 0 and number % 2 == 0:
                                                                buttons.append(use_buttons)
                                                                use_buttons = []
                                                            use_buttons.append(
                                                                buttons_shablon('Сокращения', number))
                                                    if use_buttons:
                                                        buttons.append(use_buttons)
                                                    send_message(user_id, 'Выберите режим работы бота:', buttons)

                                        break

                        last_update_info = update_id
                except Exception as error:
                    print(error)
                    try:
                        if update_id is not None:
                            last_update_info = update_id
                        continue
                    except Exception:
                        print(error)
                        continue
        time.sleep(1)
    except Exception as error:
        print(error)