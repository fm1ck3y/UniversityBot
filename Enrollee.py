import requests

class Enrollee():
    name = ''
    id = 0
    total = 0
    first = 0
    second = 0
    third = 0
    extraPoints = 0
    original = False
    lgots = False

def get_position_with_original(Enrollees, pers):
    num = 1
    for j in range(0, len(Enrollees)):
        if Enrollees[j] == pers:
            break
        if Enrollees[j].original == False and Enrollees[j].lgots == False:
            break
        if Enrollees[j].original and Enrollees[j].lgots and pers.lgots == False:
            num -= 1
        if Enrollees[j].original == False and Enrollees[j].lgots:
            num -= 1
        if Enrollees[j].lgots == False and pers.lgots:
            break
        if Enrollees[j].total < pers.total and (
                (pers.lgots and Enrollees[j].lgots) or (pers.lgots == False and Enrollees[j].lgots == False)):
            break
        if Enrollees[j].total == pers.total:
            if Enrollees[j].first < pers.first:
                break
            if Enrollees[j].first == pers.first:
                if Enrollees[j].second < pers.second:
                    break
                if Enrollees[j].second == pers.second:
                    if Enrollees[j].third < pers.third:
                        break
                    if Enrollees[j].third == pers.third:
                        if Enrollees[j].extraPoints < pers.extraPoints:
                            break
        num += 1
    return num

def update_links():
    import os
    import shutil
    from database import Link
    for link in Link.select():
        r = requests.get(link.link)
        f = open('temp_links/'+str(link.id) + '.html','w+')
        f.write(r.text)
        f.close()
    shutil.rmtree('links', ignore_errors=True)
    os.rename('temp_links', 'links')
    os.makedirs('temp_links')

def add_new_link(link):
    r = requests.get(link.link)
    f = open('links/' + str(link.id) + '.html', 'w+')
    f.write(r.text)
    f.close()