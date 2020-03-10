import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import datetime
import random
import wikipedia
import os
wikipedia.set_lang("RU")

token_lol = os.environ.get('token_bot_bot')
vk = vk_api.VkApi(token=str(token_lol))

vk._auth_token()

vk.get_api()

group_lol = os.environ.get('group_id_id')
longpoll = VkBotLongPoll(vk, group_id=group_lol)

print('Bot start')

who = ['никем', 'рабочим с завода', 'сотрудником макдональдса', 'офисным клерком']
act = ['все останеться как есть', 'жизнь измениться к лучшему', 'жизнь измениться к худшему']


def write_msg(peer_id, message):
    vk.method('messages.send', {'peer_id': peer_id, 'message': message, 'random_id': get_random_id()})


while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:

                if len(event.obj.text) > 50:
                    write_msg(event.obj.peer_id, 'уменьши сообщение)')
                    break

                if event.object.text.lower() == '.время':
                    write_msg(event.object.peer_id, 'сегодня ' + str(datetime.date.today()) + ' сейчас ' +
                              str(datetime.datetime.today().strftime("%H:%M:%S")))

                if event.object.text.lower() == '.яинфа':
                    info = vk.method('users.get', {'user_ids': event.object.from_id, 'fields': 'sex'})[0]
                    info_1 = ''
                    for key, value in info.items():
                        if key == 'sex':
                            if value == 1:
                                value = 'женский'
                            if value == 2:
                                value = 'мужской'
                            else:
                                value = 'не указан'
                            info_1 += '{0}:{1}\n'.format(key, value)
                        else:
                            info_1 += '{0}:{1}\n'.format(key, value)
                    write_msg(event.object.peer_id, 'информация\n' + info_1)

                if event.object.text.lower() == '.нас':
                    members = vk.method('messages.getConversationMembers', {'peer_id': event.obj.peer_id, 'fields': 'count'})
                    write_msg(event.object.peer_id, 'количество участников ' + str(members['count']))

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

                if event.obj.text.lower() == '.будущее':
                    write_msg(event.obj.peer_id, 'Введите имя')
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:
                            if len(event.obj.text) > 50:
                                write_msg(event.obj.peer_id, 'уменьши сообщение)')
                                break
                            if event.obj.text == 'тимур' or event.obj.text == 'Тимур':
                                write_msg(event.obj.peer_id, 'информация вам недоступна')
                                break
                            else:
                                write_msg(event.obj.peer_id,
                                          '{0} вы станете {1} и {2}. А вообще, кто знает...'.format(event.obj.text, random.choice(who), random.choice(act)))
                                break

                if event.obj.text.lower() == '.вики':
                    write_msg(event.obj.peer_id, 'введите запрос')
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:
                            if len(event.obj.text) > 50:
                                write_msg(event.obj.peer_id, 'уменьши сообщение)')
                                break
                            try:
                                write_msg(event.obj.peer_id, 'Вот что я нашел: \n' + str(wikipedia.summary(event.obj.text)[:500]))
                                break
                            except wikipedia.exceptions.DisambiguationError:
                                write_msg(event.obj.peer_id, 'запрос не выполнен')
                                break
                                
                if event.obj.text == '.инфа':
                    write_msg(event.obj.peer_id, 'id:')
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW and event.object.peer_id != event.object.from_id:
                            if event.obj.from_id == 379076419:
                                info = vk.method('users.get', {'user_ids': int(event.obj.text), 'fields': 'sex'})[0]
                                info_1 = ''
                                for key, value in info.items():
                                    if key == 'sex':
                                        if value == 1:
                                            value = 'женский'
                                        if value == 2:
                                            value = 'мужской'
                                        else:
                                            value = 'не указан'
                                        info_1 += '{0}:{1}\n'.format(key, value)
                                    else:
                                        info_1 += '{0}:{1}\n'.format(key, value)
                                write_msg(event.object.peer_id, 'информация\n' + info_1)
                            else:
                                break 

    except Exception as E:
        print(Exception)
