import requests
import bs4
from database import get_name_file_link

def LinkAvailable(link):
    try:
        from bs4 import BeautifulSoup
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'id': 'jtable'})
        if table == None:
            return False
        return True
    except: return False

def GetEnroolee(link):
    try:
        from bs4 import BeautifulSoup
        html = open(get_name_file_link(link)).read()
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'id': 'jtable'})
        pers = []
        i = 0
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            pers.append([])
            for column in columns:
                pers[i].append(column.text)
            i += 1
        del html, soup, table, pers[0]
        enrollees = []
        for x in pers:
            enrollee = {
                'id' : x[0],
                'fac' : x[2] + ' - ' + x[1],
                'total' : x[6],
                'with_original' : x[9],
                'places' : x[7],
            }
            enrollees.append(enrollee)
        return enrollees
    except:
        return False

def PlacesPersToString(link,position = False):
    if link == '': return ''
    enrollees = GetEnroolee(link)
    response = ""
    for enrollee in enrollees:
        response += "{id}. {fac}\n" \
               "Всего баллов: {total}\n" \
               "Положение в списке: {places}\n" \
               "Место с согласием: {with_original}\n".format(
            id = enrollee['id'],
            fac = enrollee['fac'],
            total = enrollee['total'],
            places = enrollee['places'],
            with_original = enrollee['with_original']
        ) + '\n'
    return response