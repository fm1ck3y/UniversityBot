import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

def main_keyboard(user):
    keyboard = VkKeyboard()
    keyboard.add_button("&#127963;  Политех им.Алексеева",VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("&#127971; Университет Лобачевского ", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("&#128285; Место с оригиналом", VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    if user.notification:
        keyboard.add_button("🔈 Оповещение", VkKeyboardColor.PRIMARY)
    else:
        keyboard.add_button("🔇 Оповещение", VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

def ngtu_link_keyboard():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button("🔗 Добавить ссылку",payload="add_link_ngtu")
    keyboard.add_button("✂ Удалить ссылку",payload="delete_link_ngtu")
    keyboard.add_line()
    keyboard.add_button("Скрыть",payload='hiden')
    return keyboard.get_keyboard()

def ngtu_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button("&#128203; Мои данные",VkKeyboardColor.POSITIVE,payload='{\"button\": \"1\"}')
    keyboard.add_line()
    keyboard.add_button("&#128102; Полное имя (ФИО)", VkKeyboardColor.POSITIVE,payload='{\"button\": \"2\"}')
    keyboard.add_line()
    keyboard.add_button("&#128279; Управление ссылками", VkKeyboardColor.PRIMARY,payload='{\"button\": \"3\"}')
    keyboard.add_line()
    keyboard.add_button("Назад ", VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def nngu_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button("&#128203; Мои данные", VkKeyboardColor.POSITIVE, payload='{\"button\": \"4\"}')
    keyboard.add_line()
    keyboard.add_button("&#128279; Ссылка на профиль", VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button("Назад ", VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def links_ngtu(message_id):
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button("✅ Добавить",VkKeyboardColor.POSITIVE,payload='{\"button\": \"add_link_ngtu:%s\"}'%(message_id+1))
    keyboard.add_button("⛔ Удалить",VkKeyboardColor.POSITIVE,payload='{\"button\": \"delete_link_ngtu:%s\"}'%(message_id+1))
    keyboard.add_line()
    keyboard.add_button("❗ Скрыть",VkKeyboardColor.NEGATIVE,payload='{\"button\": \"hiden:%s\"}'%(message_id+1))
    return keyboard.get_keyboard()

def delete_links_ngtu(user,message_id):
    from database import Link
    keyboard = VkKeyboard(inline=True)
    for link in user.get_user_links_ngtu():
        this_link = Link.select().where(Link.link == link).get()
        keyboard.add_button("📍" + this_link.name_direction.split(' ',1)[1][0:40], VkKeyboardColor.PRIMARY,payload='{\"button\": \"delete_link_ngtu_opr:%s:%s\"}'%(this_link.id,message_id+1))
        keyboard.add_line()
    keyboard.add_button("❗ Скрыть",VkKeyboardColor.NEGATIVE,payload='{\"button\": \"hiden:%s\"}'%(message_id+1))
    return keyboard.get_keyboard()

