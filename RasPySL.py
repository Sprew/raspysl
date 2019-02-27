from tkinter import *
from tkinter import ttk
from time import ctime
from datetime import datetime
import requests
import json


global textMidSL, textWestSL, textEastSL, textMidWeather, textWestWeather, textEastWeather
id       = "740069538"                                 ##Kvarnbäckskolans ID
apitoken = "4305d1db-03c5-4ea2-a70d-45b4093f7bcc"
payload  = (('key', apitoken),('id',id),('format','json'),('maxJourneys',8),('passlist',0))
wsymb    = {'1':'Klar Himmel','2':'Nästan Klar Himmel','3':'Varierad Molnighet','4':'Halvklar Himmel','5':'Molnigt',
            '6':'Mulet','7':'Dimmigt','8':'Regnskurar','9':'Åskväder','10':'Lätt Hagel',
            '11':'Snöskurar','12':'Regn','13':'Åska','14':'Hagel','15':'Snöfall'}

def strip(strang):
    head, mid, tail = strang.partition("(")
    return head

def onClickSL():
    textWestSL = ""
    textMidSL = ""
    textEastSL = ""
    r = requests.get('https://api.resrobot.se/v2/departureBoard', params=payload)
    data = json.loads(r.text)
    for entry in data['Departure']:
        linje = entry['transportNumber']
        mot = strip(entry['direction'])
        tid = entry['time']
        textWestSL += str(linje) + "\n"
        textMidSL += str(mot) + "\n" 
        textEastSL += str(tid) + "\n"
    
    labelMidSL.config(text=textMidSL, bg="light grey")
    labelWestSL.config(text=textWestSL, bg="light grey")
    labelEastSL.config(text=textEastSL, bg="light grey")
    currentTime.config(text="Klocka: "+ctime().split(" ")[3])
    

def onClickVadret():
    iterate = 0
    textMidWeather = ""
    textWestWeather = ""
    textEastWeather = ""
    rg = requests.get('https://opendata-download-metfcst.smhi.se/api/category/pmp2g/version/2/geotype/point/lon/18.063240/lat/59.334591/data.json')
    data = json.loads(rg.text)
    for entry in data['timeSeries']:
        if ((entry['validTime'][0:16]).split('T')[1]).split(':')[0] >= (ctime().split(" ")[3]).split(':')[0]:
            print((entry['validTime'][0:16]).split('T')[1])
            print((ctime().split(" ")[3]).split(':')[0])
            textWestWeather += str(((entry['validTime'][0:16])).split('T')[1]) + "\n"
            for parameters in entry['parameters']:
                if parameters['name'] == 't':
                    textMidWeather += str(parameters['values'][0]) + "\n"
                    print("Antal Grader: " , parameters['values'])
                if parameters['name'] == 'Wsymb':
                    textEastWeather += str(wsymb[str(parameters['values'][0])]) + "\n"
                    print(wsymb[str(parameters['values'][0])])
                    iterate +=1
            if iterate == 8:
                break
    labelWestWeather.config(text=textWestWeather, bg="light grey")
    labelMidWeather.config(text=textMidWeather, bg="light grey")
    labelEastWeather.config(text=textEastWeather, bg="light grey")

root = Tk()
nb = ttk.Notebook(root)

sl = ttk.Frame(nb)
nb.add(sl, text='SL-Avgångar')

vadret = ttk.Frame(nb)
nb.add(vadret, text='Dagens Väder')

#topFrame = Frame(root)
#topFrame.pack()
#bottomFrame = Frame(root)
#bottomFrame.pack()
root.title("RasPySL")
root.attributes("-fullscreen", True)

labelWestSL = Label(sl, text="", font=("Helvetica", 16))
labelMidSL = Label(sl, text="Inga avgångar för tillfället,\n klicka på uppdatera.", font=("Helvetica", 16))
labelEastSL = Label(sl, text="", font=("Helvetica", 16))
button = Button(sl, text="UPPDATERA", command=onClickSL, width="10", bg="green", font=("Helvetica", 16))
label = Label(sl, text="Avgångar", font=("Helvetica", 14))
currentTime = Label(sl, text="Klocka: " + ctime().split(" ")[3], font=("Helvetica", 14))


weather = Button(vadret, text="UPPDATERA", command=onClickVadret, width="10", bg="blue", font=("Helvetica", 16))
labelWestWeather = Label(vadret, text="", font=("Helvetica", 16))
labelMidWeather = Label(vadret, text="Klicka på uppdatera för prognos", font=("Helvetica, 16"))
labelEastWeather = Label(vadret, text="", font=("Helvetica, 16"))
currentTimeW = Label(vadret, text="Klocka: " + ctime().split(" ")[3], font=("Helvetica", 14))

nb.pack(fill=X)
button.pack(fill=X)
currentTime.pack(fill=X)
label.pack(fill=X)

labelWestSL.pack(side=LEFT, expand=TRUE)
labelMidSL.pack(side=LEFT, expand=TRUE)
labelEastSL.pack(side=LEFT, expand=TRUE)

weather.pack(fill=X)
currentTimeW.pack(fill=X)

labelWestWeather.pack(side=LEFT, expand=TRUE)
labelMidWeather.pack(side=LEFT, expand=TRUE)
labelEastWeather.pack(side=LEFT, expand=TRUE)

root.mainloop()
