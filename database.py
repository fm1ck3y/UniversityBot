from peewee import *
import datetime
import uuid
from playhouse.migrate import *
db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = IntegerField(null= False)
    full_name = CharField(default= '')
    link_nngu = CharField(default= '')
    link_ngtu =CharField(default='')
    last_keyboard = CharField(default='')
    last_command = CharField(default='')
    notification = BooleanField(default=True)
    position_ngtu = CharField(default='')
    position_nngu = CharField(default='')
    class Meta:
        db_table = "users"
        order_by = ('created_at')

    def get_user_links_ngtu(self):
        links = [x for x in self.link_ngtu.split(";")]
        if links == ['']: return []
        return links

    def add_link_ngtu(self,link):
        links = self.get_user_links_ngtu()
        if link not in links:
            links.append(link)
        self.add_position_ngtu()
        self.link_ngtu = ';'.join(x for x in links)
        self.save()

    def delete_link_ngtu(self,link):
        links = self.get_user_links_ngtu()
        links.remove(link)
        self.delete_position_ngtu(link)
        self.link_ngtu = ';'.join(x for x in links)
        self.save()

    def old_position_link_ngtu(self):
        this_links = self.get_user_links_ngtu()
        this_positions = [x for x in self.position_ngtu.split(";")]
        if this_positions == ['']: this_positions = []
        this_dict = {}
        for i,link in enumerate(this_links):
            this_dict[link] = this_positions[i]
        return this_dict

    def delete_position_ngtu(self,link):
        this_dict = self.old_position_link_ngtu()
        this_dict.pop(link)
        self.position_ngtu = ';'.join(str(x) for x in this_dict.values())
        self.save()

    def add_position_ngtu(self):
        this_positions = self.position_ngtu.split(';')
        if this_positions == ['']: this_positions = []
        this_positions.append(0)
        self.position_ngtu = ';'.join(str(x) for x in this_positions)
        self.save()

    def change_position_ngtu(self,link,new_pos):
        this_positions = self.old_position_link_ngtu()
        this_positions[link] = new_pos
        self.position_ngtu = ';'.join(str(x) for x in this_positions.values())
        self.save()

    def __str__(self):
        links_ngtu_str = "\n"
        link_nngu_str = self.link_nngu
        for i,link in enumerate(self.get_user_links_ngtu()):
            links_ngtu_str += str(i+1) + ': ' + link + '\n'
        if links_ngtu_str == "\n": links_ngtu_str = "ссылок нет"
        if link_nngu_str== '': link_nngu_str = 'ссылки нет'
        return "🧓 Ваше ФИО: {full_name}\n" \
               "🔗 Ваши ссылки НГТУ: {link_ngtu}\n" \
               "🔗 Ваша ссылка ННГУ: {link_nngu}\n".format(
            full_name=self.full_name,
            link_ngtu=links_ngtu_str,
            link_nngu=link_nngu_str
        )

class Link(BaseModel):
    id = PrimaryKeyField()
    link = CharField(default='')
    name_fac = CharField(default='')
    name_direction = CharField(default='')
    class Meta:
        db_table = "links"
        order_by = ('created_at')

def get_user(id):
    try:
        return User.select().where(User.id == id).get()
    except DoesNotExist as de:
        User.create(id = id)
    return User.select().where(User.id == id).get()

def initialize():
    try:
        db.connect()
        User.create_table(safe=True)
        Link.create_table(safe=True)
    except InternalError as px:
        print(str(px))

def get_name_file_link(link):
    try:
        return 'links/' + str(Link.select().where(Link.link == link).get().id) + '.html'
    except: return None

def add_link_nngu(new_link,old_link):
    from Enrollee import add_new_link
    try:
        length = len(User.select().where(User.link_nngu == old_link))
        if length == 1:
            this = Link.select().where(Link.link == old_link).get()
            this.delete_instance()
    except: pass
    this_link = Link.create(link = new_link)
    add_new_link(this_link)

def delete_link_ngtu(link):
    try:
        if len(User.select().where(link in User.link_nngu)) == 1:
            Link.select().where(Link.link == link).get().delete_instance()
    except: pass

def add_link_ngtu(link):
    from NGTU import GetFacAndDirection
    from Enrollee import add_new_link
    if len(Link.select().where(Link.link == link)) == 0:
        fac,direction = GetFacAndDirection(link)
        this_link = Link.create(link = link,name_fac = fac,name_direction = direction)
        add_new_link(this_link)

initialize()