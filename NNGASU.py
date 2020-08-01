import requests
from Enrollee import *

def GetEnroleeNNGASU(link):
    try:
        from bs4 import BeautifulSoup
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table', attrs={'class': 'container-table'})
        pers = []
        for i,row in enumerate(table.find_all('tr')):
            columns = row.find_all('td')
            pers.append([])
            for column in columns:
                pers[i].append(column.text.strip())
            try:
                if len(pers[i]) != 0:
                    enrollee = Enrollee()
                    enrollee.name = pers[i][1]
                    if pers[i][2] != '—':
                        enrollee.total = int(pers[i][2])
                    else:
                        enrollee.total = 0
                    balls = pers[i][5].replace('1.','.').replace('2.','.').replace('3.','.').replace('4.','.').replace('5.','.').split('.')
                    del balls[0]
                    j = 0
                    for k in range(len(balls)):
                        if balls[k].split(':')[1] != ' —':
                            balls[j] = int(balls[k].split(':')[1].replace('(ЕГЭ)',''))
                            j+=1
                    try:
                        enrollee.first = int(balls[0])
                    except:
                        enrollee.first = 0
                    try:
                        enrollee.second = int(balls[1])
                    except:
                        enrollee.second = 0
                    enrollee.second = balls[1]
                    try:
                        enrollee.third = int(balls[2])
                    except:
                        enrollee.third = 0
                    enrollee.extraPoints = int(pers[i][4])
                    #enrollee.lgots = True if abitur[i][8] != 'Нет' else False
                    enrollee.lgots = False
                    enrollee.original = True if pers[i][8] != 'Нет' else False
                    pers[i] = enrollee
                    del enrollee
            except: pass
        del pers[0]
        return pers
    except:
        return False

GetEnroleeNNGASU("https://lka.nngasu.ru/app?back=356997172473&bc=baf09d3bfeb83a7127a147a809339537&bp=H4gl7cgruBTA8naCzQeCIUdncZ2qU-fpxkcojPoHmbowjg76LbMZ6VasqBPrrseMaA_BXCqM-cCk&service=bcs&site=356997172993")