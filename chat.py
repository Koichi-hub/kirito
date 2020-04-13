import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import wikipedia
import googletrans
import os
import COVID19Py
import requests

wikipedia.set_lang("RU")

token_lol = os.environ.get('token_bot_bot')
vk = vk_api.VkApi(token=str(token_lol))

vk._auth_token()

vk.get_api()

group_lol = os.environ.get('group_id_id')
longpoll = VkBotLongPoll(vk, group_id=group_lol)

print('Bot start')


def write_msg(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': get_random_id()})


def per(peer_id, message):
    write_msg(peer_id, googletrans.Translator().translate(message, dest='ru').text)


def covid(peer_id, message):
    covid19 = COVID19Py.COVID19()
    country = message.lower()
    if country == 'сша' or country == 'америка':
        loc = covid19.getLocationByCountryCode('US')[0]
        b = [loc['country'], loc['country_population'], [loc['latest'][key] for key in loc['latest']]]
        country = f'страна {b[0]}, с населением {b[1]} человек\nзаражено - {b[2][0]}\nумерло - {b[2][1]}'
        write_msg(peer_id, country)
    elif country == 'италия':
        loc = covid19.getLocationByCountryCode('IT')[0]
        b = [loc['country'], loc['country_population'], [loc['latest'][key] for key in loc['latest']]]
        country = f'страна {b[0]}, с населением {b[1]} человек\nзаражено - {b[2][0]}\nумерло - {b[2][1]}'
        write_msg(peer_id, country)
    elif country == 'россия':
        loc = covid19.getLocationByCountryCode('RU')[0]
        b = [loc['country'], loc['country_population'], [loc['latest'][key] for key in loc['latest']]]
        country = f'страна {b[0]}, с населением {b[1]} человек\nзаражено - {b[2][0]}\nумерло - {b[2][1]}'
        write_msg(peer_id, country)
    else:
        loc = covid19.getLatest()
        b = [loc[key] for key in loc]
        country = f'В мире\nзаражено - {b[0]}\nумерло - {b[1]}'
        write_msg(peer_id, country)


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:
                
                if event.obj.text == '.covid19':
                    write_msg(event.obj.peer_id, 'Вам доступны США, Италия, Россия')
                    write_msg(event.obj.peer_id, 'Введите страну:')
                    for event in longpoll.listen():
                        covid(event.obj.peer_id, event.obj.text)
                        break

                if event.obj.text == '.перевод':
                    write_msg(event.obj.peer_id, 'Введите текст)')
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:
                            per(event.obj.peer_id, event.obj.text)
                            break

                if event.obj.text == '.погода':
                    pog = os.environ.get('pog')
                    response = requests.get(str(pog))
                    response = response.json()
                    b = [response['name'], response['sys']['country'], response['weather'][0]['main'],
                         int(response['main']['temp']) - 273, response['wind']['speed']]

                    write_msg(event.obj.peer_id,
                              f'В городе {b[0]}, {b[1]}, сейчас - {b[2]}, температура - {b[3]}, скорость ветра - {b[4]}')

                if event.obj.text.lower() == '.команды':
                    write_msg(event.obj.peer_id,
                              '.погода, .перевод, .вики, .чат, .covid19')

                if event.object.text.lower() == '.чат':
                    if event.obj.from_id == 379076419:
                        info_chat = vk.method('messages.getConversationMembers', {'peer_id': event.obj.peer_id})[
                            'profiles']
                        key_key = ['id', 'first_name', 'last_name', 'sex', 'screen_name']
                        info_user = [[] * len(info_chat) for i in range(len(info_chat))]
                        for i in range(len(info_chat)):
                            for key in info_chat[i].keys():
                                if key in key_key:
                                    info_user[i].append(info_chat[i][key])
                        a = ''
                        for i in info_user:
                            a += '{0}\n'.format(i)
                        vk.method('messages.send', {'user_id': 379076419,
                                                    'message': 'информация о участниках:\n' + a, 'random_id': 0})
                    else:
                        write_msg(event.obj.peer_id, 'у тебя нет доступа')

                if event.obj.text.lower() == '.вики':
                    write_msg(event.obj.peer_id, 'введите запрос')
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:
                            if len(event.obj.text) > 50:
                                write_msg(event.obj.peer_id, 'уменьши сообщение)')
                                break
                            try:
                                write_msg(event.obj.peer_id,
                                          'Вот что я нашел: \n' + str(wikipedia.summary(event.obj.text)[:500]))
                                break
                            except wikipedia.exceptions.DisambiguationError:
                                write_msg(event.obj.peer_id, 'запрос не выполнен')
                                break

    except Exception as E:
        print(Exception)
