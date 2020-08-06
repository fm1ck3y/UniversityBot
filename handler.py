from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType,VkBotMessageEvent
from config import *
from database import *
from keyboard import *
from threading import Thread
import logging
from vk_api.utils import get_random_id
from NNGU import *
import schedule
import time
import json

logging.basicConfig(format='%(asctime)s %(message)s',filename='logger.log')
vk_session = vk_api.VkApi(token=VK_API_ACCESS_TOKEN)
vk = vk_session.get_api()

def handler_command(message : VkBotMessageEvent):
    user = get_user(message.obj['message']['from_id'])
    text = message.obj['message']['text']
    payload = ''
    try:
        payload = json.loads(message.obj['message']['payload'])['button']
    except: pass
    if text == '':
        if len(message.message['attachments']) > 0:
            link = message.message['attachments'][0]['link']['url']
    else:
        link = text
    if text == '🏛  Политех им.Алексеева':
        send_message("Меню политехнического института имени Алексеева",user,ngtu_keyboard())
    elif text == '🏣 Университет Лобачевского':
        send_message('Меню Университета Лобачевского',user,nngu_keyboard())
    elif text == '👦 Полное имя (ФИО)':
        send_message("🧓 Введите ваше ФИО.\nНапример: Иванов Иван Иванович. (❗ как в списках)",user)
        user.last_command = '/set_name'
    elif text == '📋 Мои данные':
        send_message(str(user),user)
    elif text == 'Назад':
        send_message("🏢 Главное меню",user,main_keyboard(user))
    elif text == '🔈 Оповещение' or text == "🔇 Оповещение":
        if user.notification:
            user.notification = False
            send_message("✅ Оповещения успешно выключены!",user,main_keyboard(user))
        else:
            user.notification = True
            send_message("✅ Оповещения успешно включены!",user,main_keyboard(user))
    elif text == '🔗 Ссылка на профиль':
        send_message("❗ Введите ссылку на ваш профиль на сайте Университета Лобачевского.\n"
                     "Например: https://enter.unn.ru/preport/stat/abit.php?id=281474976795355",user)
        user.last_command = '/link_nngu'
    elif text == '🔝 Место с оригиналом':
        from NGTU import GetInfoForEnrolle
        response = "Политехнический институт им. Алексеева: \n\n"
        for i,link_ngtu in enumerate(user.get_user_links_ngtu()):
            info = GetInfoForEnrolle(link_ngtu,user.full_name)
            if info != None:
                response += str(i+1) + '. ' + GetInfoForEnrolle(link_ngtu,user.full_name)
        response += 'Университет Лобачевского:\n\n' + PlacesPersToString(user.link_nngu)
        send_message(response,user)
    elif text == '🔗 Управление ссылками':
        send_message(text,user,links_ngtu(message.obj['message']['id']))
    elif user.last_command == '/set_name':
        user.full_name = text
        user.last_command = ''
        send_message("✅ ФИО успешно изменено!",user)
    elif user.last_command == '/link_nngu':
        if LinkAvailable(link):
            add_link_nngu(link, user.link_nngu)
            user.link_nngu = link
            send_message("✅ Вы успешно изменили ссылку на ваш профиль в Университете Лобачевского!",user)
        else:
            send_message("⛔ Ссылка введена неверно.\n Пример ссылки: https://enter.unn.ru/preport/stat/abit.php?id=281474976795355", user)
        user.last_command = ''
    elif user.last_command == '/add_link_ngtu':
        from NGTU import LinkAvailableNGTU
        if LinkAvailableNGTU(link):
            user.add_link_ngtu(link)
            add_link_ngtu(link)
            send_message("✅ Вы успешно добавили ссылку на направление в Политехническом институте им. Алексеева!",user)
        else:
            send_message("⛔ Ссылка введена неверно.\n Пример ссылки: https://abit.nntu.ru/info/bak/rating/?learn_form_id=0&fac_id=281474976714124&specialization=&spec_id=281474976710709&commerce=1",user)
        user.last_command = ''
    elif 'add_link_ngtu' in payload:
        send_message("Введите ссылку на список с вашим факультетом.\nНапример: https://abit.nntu.ru/info/bak/rating/?learn_form_id=0&fac_id=281474976714124&specialization=&spec_id=281474976710709&commerce=1",user)
        user.last_command = '/add_link_ngtu'
        vk.messages.delete(message_ids=payload.split(':')[1], group_id=GROUP_ID, delete_for_all=1)
    elif 'delete_link_ngtu_opr' in payload:
        try:
            this_link = Link.select().where(Link.id == payload.split(':')[1]).get()
            delete_link_ngtu(this_link.link)
            user.delete_link_ngtu(this_link.link)
        except: pass
        send_message("✅ Вы успешно удалили ссылку!",user)
        vk.messages.delete(message_ids = payload.split(':')[2],group_id = GROUP_ID,delete_for_all = 1)
    elif 'delete_link_ngtu' in payload:
        send_message("❗ Выберите направление, которое вы хотите удалить.",user,delete_links_ngtu(user,message.obj['message']['id']))
        vk.messages.delete(message_ids=payload.split(':')[1], group_id=GROUP_ID, delete_for_all=1)
    elif 'hiden' in payload:
        vk.messages.delete(message_ids=payload.split(':')[1], group_id=GROUP_ID, delete_for_all=1)
    else:
        send_message("❗ Неизвестная команда", user, main_keyboard(user))
    user.save()

def handler_message():
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    _server, _key, _ts = longpoll.server, longpoll.key, longpoll.ts
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            Thread(target=handler_command, args=[event]).start()

def send_message(message, user, keyboard = None) :
    """Отправка сообщения пользователю Вконтакте по user_id """
    try:
        if keyboard == None:
            msg = vk.messages.send(peer_id=user.id,
                             message=message,
                             random_id=get_random_id())
        else:
            msg = vk.messages.send(peer_id=user.id,
                             message=message,
                             keyboard=keyboard,
                             random_id=get_random_id())
        return
    except Exception as e: logging.error(e)

def ThreadSchedule():
    from Enrollee import update_links
    update_links()
    find_change_position()
    schedule.every().minute.do(update_links)
    #schedule.every().minute.do(find_change_position)
    while True:
        schedule.run_pending()
        time.sleep(1)

def find_change_position():
    from NGTU import GetInfoForEnrolle
    from NNGU import GetEnroolee
    for user in User.select():
        old_positions = user.old_position_link_ngtu()
        for link_ngtu in user.get_user_links_ngtu():
            try:
                string_format,position_with_original = GetInfoForEnrolle(link_ngtu,user.full_name,True)
                if old_positions[link_ngtu] != str(position_with_original):
                    send_message("❗❗ Позиция изменилась!\n" + string_format[0:-2] + "\nСтарая позиция: " + str(old_positions[link_ngtu]) + "\n❗❗",user)
                    user.change_position_ngtu(link_ngtu,position_with_original)
            except: pass

            
            
Thread(target= ThreadSchedule).start()
handler_message()
