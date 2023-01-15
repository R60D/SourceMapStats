import matplotlib.pyplot as plt
import numpy as np
import csv
import re
from datetime import datetime, timedelta
import copy
#def f(x): return x**2
#x = np.linspace(-3,3,1000)
#plt.plot(x,f(x))
#plt.show()
#the fortmat of the csv is the following [ip,port,mapname,playercount,time,Region] [0,5]
format = '%Y-%m-%d-%H:%M:%S' # date format
file = "output.csv"

#Shows the actual data as a plot
def plotter(data):
    allmaps = {}
    for day in data:
        x = []
        y = []
        ytotal = 0
        for map in data[day]:
            if map not in allmaps.keys():
                allmaps.update({map:[[],[],1]})
            allmaps[map][0].append(data[day][map])#y axis
            ytotal += data[day][map]
            allmaps[map][1].append(day)#x axis
        for map in data[day]:
            allmaps[map][2] = ytotal #max for this timespan

            #sort with sum of players
    allmaps2 = copy.deepcopy(allmaps)
    allmaps3 = copy.deepcopy(allmaps)
    for map in allmaps2:
        allmaps2[map][0] = sum(allmaps2[map][0])
    allmaps2 = sorted(allmaps2.items(), key=lambda x:x[1],reverse=True)

    mapindex = 0
    previousmap = None
    for map in allmaps2:
        if(mapindex > 1):
            break
        mapindex += 1
        
        
        _YMAX = allmaps3[map[0]][2]
        _X = allmaps3[map[0]][1]
        _Y = allmaps3[map[0]][0]
        _YNORMALIZED = [x / _YMAX for x in _Y]
        plotdraw(_X,_Y,map[0])
    plt.grid(True)
    plt.legend()
    plt.show()
#Groups rows into arrays that share the specified time interval

def plotdraw(_X,_Y,_label):

    col = (np.random.random(), np.random.random(), np.random.random())

    if(previousmap == None):
        plt.bar(np.arange(len(_Y)),_Y, color=col, label=_label)
    else:
        plt.bar(np.arange(len(_Y)),_Y, color=col, label=_label,bottom=previousmap)
    previousmap = _Y
    print(previousmap)
    print(plt.xlim())
    a = _X[0]
    b = _X[int(len(_X) / 2)]
    c = _X[-1]
    a = datetime.strptime(a,format)
    b = datetime.strptime(b,format)
    c = datetime.strptime(c,format)
    plt.xticks(np.linspace(plt.xlim()[0],plt.xlim()[1],3),[a.strftime("%Y/%m/%d"),b.strftime("%Y/%m/%d"),c.strftime("%Y/%m/%d")])

def timechunker(_file,_format,interval=1):

    chunkedarray = []
    chunkedarray_index = 0
    chunktime = timedelta(interval,0,0,0,0,0,0)
    initialtime = None

    with open(_file,"r") as serverdata:
        rawstat = csv.reader(serverdata)
        for row in rawstat:
            if(initialtime == None):
                initialtime = datetime.strptime(row[4], _format) #get the first row time
            datetime_object = datetime.strptime(row[4], _format)
            try:
                chunkedarray[chunkedarray_index].append(row)
            except:
                chunkedarray.append([])
                chunkedarray[chunkedarray_index].append(row)
                #print(chunkedarray[chunkedarray_index][-1])
            else:
                if(datetime_object > initialtime+chunktime):
                    #print(chunkedarray_index)
                    chunkedarray_index += 1
                    chunktime += timedelta(interval,0,0,0,0,0,0)
            
        return chunkedarray

#Makes sure that different versions of the same map are not considered unique.
def namecutter(x,filter=["fix","final","redux","1","2","3","4","5","6","7","8","9","0","finished","remake"]):
    y = re.search("dr_",x).start()
    z = x[y:]
    e = z.split("_")
    try:
        rex = f"{e[0]}_{e[1]}_{e[2]}"
    except IndexError:
        rex = f"{e[0]}_{e[1]}"
        return rex
    for n in filter:
        if n in e[2]:
            rex = f"{e[0]}_{e[1]}"
    return rex

#remove prefixes
def prefixremover(data):
    for timelist in data:
        for row in timelist:
            row[2] = namecutter(row[2])
    return data

##remove duplicates and make a dict
def remdup(data):
    datatemp2 = {}
    for timelist in data:
        firsttime = timelist[0][4]
        datatemp2[firsttime] = {}
        for row in timelist:
            if(row[2] in datatemp2[firsttime].keys()):
                datatemp2[firsttime].update({row[2]:datatemp2[firsttime].get(row[2])+int(row[3])})#adds player count to dict
            else:
                datatemp2[firsttime].update({row[2]:int(row[3])})#adds a new dict with the player count
    return datatemp2

#a = timechunker(file,format,2)
#b = prefixremover(a)
#plotter(remdup(b))

#Read the .cvs file and show a ratio between map/all players
def Reader(file):
    mapsum = {}
    countrysum = {}
    countrysum2 = {}
    countrysum3 = {}
    uniqueips = []
    data_amount = []
    countrysum_prefixed = {}
    format = '%Y-%m-%d-%H:%M:%S'
    with open(file,"r") as serverdata:
        for ip in csv.reader(serverdata):
            if ip[0] not in data_amount:
                data_amount.append(ip[0])
            try: # first entry? => exists
                mapsum[ip[2]]
                mapsum[ip[2]][ip[5]] = int(ip[3])+int(ip[3]) # add duplicate region map player count together
            except: #first entry does not exist
                mapsum[ip[2]] = {ip[5]:int(ip[3])}
        #print(mapsum) # data type {'mapname':{'country':playercount}}

        for map in mapsum:
            countrynum = 0 # this value 
            for country in mapsum[map]:
                countrynum += mapsum[map][country]
            countrysum[map] = countrynum # countrysum is mapname and all countries players

        for map in countrysum:
            if namecutter(map) in countrysum2:
                countrysum2[namecutter(map)] += countrysum[map]
            else:
                countrysum2[namecutter(map)] = countrysum[map]

        totalplayers = 0
        for map in countrysum:
            totalplayers += countrysum[map]


        for map in mapsum:
            for cntr in mapsum[map]:
                try:
                    countrysum3[cntr] += mapsum[map][cntr]
                except KeyError:
                    countrysum3[cntr] = mapsum[map][cntr]
        #sort
        countrysum2 =  {k: v for k, v in sorted(countrysum2.items(), key=lambda item: item[1],reverse=True)}
        countrysum3 =  {k: v for k, v in sorted(countrysum3.items(), key=lambda item: item[1],reverse=True)}


    nexa = False
    sanitycheck = 0

    print("##############################################")
    print("Map player ratio")
    print("##############################################")
    for map in countrysum2:
        sanitycheck += countrysum2[map]
        if nexa == False:

            print(f"{countrysum2[map]}/{totalplayers} players ||| {round(100*countrysum2[map]/totalplayers,2)} % ||| {map} !!!Most popular deathrun map!!!")
            nexa = True
        else:
            print(f"{countrysum2[map]}/{totalplayers} players ||| {round(100*countrysum2[map]/totalplayers,2)} % ||| {map}")
    print(f"{sanitycheck} : summed ")
    print("##############################################")
    print(f"Server country ratio ||| {len(data_amount)} unique servers")
    print("##############################################")
    nexa = False
    for map in countrysum3:
        if nexa == False:
            print(f"{countrysum3[map]}/{totalplayers} players ||| {round(100*countrysum3[map]/totalplayers,2)} % ||| {map} !!!Most popular region!!!")
            nexa = True
        else: print(f"{countrysum3[map]}/{totalplayers} players ||| {round(100*countrysum3[map]/totalplayers,2)} % ||| {map}")



