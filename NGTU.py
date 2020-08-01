from Enrollee import *
from database import get_name_file_link

def LinkAvailableNGTU(link):
    from bs4 import BeautifulSoup
    try:
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.body.find('table', attrs={'class': 'table rating_fac table-hover table-sm table-bordered'})
        if table == None: return False
        return True
    except:
        return False

def GetEnrollees(link):
    from bs4 import BeautifulSoup
    try:
        html = open(get_name_file_link(link)).read()
        soup = BeautifulSoup(html,'html.parser')
        table = soup.body.find('table',attrs = {'class':'table rating_fac table-hover table-sm table-bordered'})
        fac = soup.body.find_all('div',attrs = {'class' : 'col-sm-9'})[1].find('option',selected = True).text
        direction = soup.body.find_all('div',attrs = {'class' : 'col-sm-9'})[2].find('option',selected = True).text
        abitur = []
        i = 0
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            abitur.append([])
            for column in columns:
               abitur[i].append(column.text)
            if len(columns) != 0:
                enrollee = Enrollee()
                enrollee.name = abitur[i][1]
                enrollee.total = int(abitur[i][2])
                balls = abitur[i][3].split(',')
                for j in range(len(balls)):
                    balls[j] = int(balls[j].split('-')[1])
                enrollee.first = balls[0]
                enrollee.second = balls[1]
                enrollee.third = balls[2]
                enrollee.extraPoints = int(abitur[i][4])
                enrollee.lgots = True if abitur[i][5] != '' else False
                enrollee.original = True if abitur[i][6] != '' else False
                abitur[i] = enrollee
                del enrollee
                i += 1
        del html,soup,table
        del abitur[len(abitur)-1]
        return abitur,fac,direction
    except:
        return False,False,False

def GetInfoForEnrolle(link,full_name,position = False):
    enrollees,fac,direction = GetEnrollees(link)
    def byOriginal_key(enrollee : Enrollee):
        return enrollee.original == False
    enrollees = sorted(enrollees,key = byOriginal_key)
    if enrollees != False:
        this_enrollee = None
        for enrollee in enrollees:
            if enrollee == []: continue
            if enrollee.name == full_name:
                this_enrollee = enrollee
                break
        if this_enrollee != None:
            position_with_original = get_position_with_original(enrollees,this_enrollee)
            if position == False:
                return "Институт/Факультет : {fac}\n" \
                       "Направление : {direction}\n" \
                       "Место с согласием : {position_with_original}\n\n".format(
                    fac = fac,
                    direction = direction,
                    position_with_original = position_with_original
                )
            else:
                return "Институт/Факультет : {fac}\n" \
                       "Направление : {direction}\n" \
                       "Место с согласием : {position_with_original}\n\n".format(
                    fac=fac,
                    direction=direction,
                    position_with_original=position_with_original
                ), position_with_original
        else:
            return None
    return None

def GetFacAndDirection(link):
    from bs4 import BeautifulSoup
    try:
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'html.parser')
        fac = soup.body.find_all('div', attrs={'class': 'col-sm-9'})[1].find('option', selected=True).text
        direction = soup.body.find_all('div', attrs={'class': 'col-sm-9'})[2].find('option', selected=True).text
        del html, soup
        return fac, direction
    except:
        return None,None