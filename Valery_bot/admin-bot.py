import requests
import time
from datetime import datetime
import pytz
import json
import os
from sql import get_admins, new_in_sql, new_password, info_user, give_admin, remove_admin, get_last_comment, get_acurancy_comment


token = '6339742908:AAHnBzVbs4adue4M9B75mOLUe-pZQUipR5o'
URL = 'https://api.telegram.org/bot'
update_id = None
key = None


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
    else:
        if buttons is None:
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
                        give_admin(teg_user)
                        is_admin = info_user(teg_user)
                        if is_admin == f'@{teg_user} - администратор':
                            if msg != '':
                                if msg.lower() == 'stop':
                                    key = msg
                                elif len(msg) > len('добавить ') and msg[:len('добавить ')].lower() == 'добавить ':
                                    msg = msg[len('добавить '):]
                                    msg = msg.replace('@', '')
                                    resultat = give_admin(msg)
                                    send_message(user_id, resultat)
                                elif len(msg) > len('удалить ') and msg[:len('удалить ')].lower() == 'удалить ':
                                    msg = msg[len('удалить '):]
                                    msg = msg.replace('@', '')
                                    resultat = remove_admin(teg_user)
                                    send_message(user_id, resultat)
                                elif len(msg) > len('осмотреть ') and msg[:len('осмотреть ')].lower() == 'осмотреть ':
                                    msg = msg[len('осмотреть '):]
                                    msg = msg.replace('@', '')
                                    resultat = info_user(msg)
                                    send_message(user_id, resultat)
                                elif len(msg) > len('создать ключ ') and msg[:len('создать ключ ')].lower() == 'создать ключ ':
                                    send_message(user_id, new_password(user_id, msg.replace('создать ключ ', ''), update_id))
                                elif msg == '/fail' or msg == '/all':
                                    send_message(user_id, 'Ожидайте...')
                                    try:
                                        get_acurancy_comment(msg)
                                        send_document(user_id,
                                                      'output.xlsx',
                                                      'Вот ваш файл :)')
                                    except Exception as error:
                                        send_message(user_id, error)
                                    os.remove('output.xlsx')
                            elif msg == '':
                                try:
                                    about_msg = elemen['message']
                                    file_id = about_msg['document']['file_id']
                                    file_name = about_msg['document']['file_name']
                                except Exception:
                                    file_name = None
                                    file_id = None
                                if file_id is not None and ('.xlsx' in file_name or '.pdf' in file_name):
                                    send_message(user_id,
                                                 '⏳Обновляем сведения для пользователей.\n❗️Процесс может занять от нескольких секунд, до нескольких минут в зависимости от веса файла.')
                                    try:
                                        download_url = f'https://api.telegram.org/bot{token}/getFile?file_id={file_id}'
                                        download_response = requests.get(download_url)
                                        file_info = download_response.json()
                                        file_path = file_info['result']['file_path']
                                        download_url = f'https://api.telegram.org/file/bot{token}/{file_path}'
                                        download_response = requests.get(download_url)
                                        if '.xlsx' in file_path:
                                            file_name = 'bd.xlsx'
                                        with open(file_name, 'wb') as file:
                                            file.write(download_response.content)
                                        if '.xlsx' in file_name:
                                            send_message(user_id,
                                                         'Успешная передача информации в базу обновления, вы можете продолжить общение со мной или дождаться результата операции :)')
                                        elif '.pdf' in file_name:
                                            send_message(user_id,
                                                         'Успешная передача информации в общий доступ, вы можете продолжить общение со мной :)')
                                    except Exception as error:
                                        send_message(user_id, f'Ошибка обновления сведений для пользователей: {error}')
                            if os.path.exists('bd.xlsx'):
                                result = new_in_sql()
                                if result == 'Y':
                                    while True:
                                        try:
                                            if os.path.exists('bd.xlsx'):
                                                os.remove('bd.xlsx')
                                            if os.path.exists('questions.db'):
                                                os.remove('questions.db')
                                            os.rename('ninfo.db', 'questions.db')
                                            break
                                        except Exception as error:
                                            continue
                                    admins = get_admins()
                                    for administrator in admins:
                                        administrator = administrator[0]
                                        send_message(administrator,
                                                     'Я успешно обновил сведения, которые недавно получил - все прошло гладко :)')
                                elif result == 'N':
                                    while True:
                                        try:
                                            if os.path.exists('bd.xlsx'):
                                                os.remove('bd.xlsx')
                                            break
                                        except Exception as error:
                                            continue
                                    send_document(user_id,
                                                  'error.gif',
                                                  '❌Произошла ошибка сохранения новых данных, пользователи имеют на руках устаревшие данные!\n❗️Проблема может быть вызвана новым оформлением файла exel, отправьте файл в старом формате или обратитесь к специалисту!')
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
        comments = get_last_comment()
        if comments != 'N' and len(comments) > 0:
            for comment in comments:
                ceta, question, result, commentary, status, worktime = comment
                admins = get_admins()
                for admin in admins:
                    send_message(admin[0],
                                 f'Получено новое предложение по улучшению!\nКатегория: {ceta}\nВопрос: {question}\nПредложение: {commentary}\nВремя отправки отзыва: {worktime}')

        time.sleep(1)
        if key is not None:
            break
    except Exception as error:
        print(error)