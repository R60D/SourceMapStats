import sys
sys.path.append("python-valve")
import valve.source
import datetime
import requests
import socket
import csv
from time import time,sleep
import re
#scan masterserver for ips, output address if it contains prefix=dr_
def SlowScan(prefix="dr_",timeout_master=1,timeout_query=1,regionserver="all"):
    format = '%Y-%m-%d-%H:%M:%S' # date format
    x = 0 # number of "broken" servers print me to see it
    y = 0 # number of timed out servers
    z = 0 #total servers
    ips = []
    with valve.source.master_server.MasterServerQuerier(timeout=timeout_master) as msq:
        try:
            for address in msq.find(gamedir=u"tf",empty=True,secure=True,region=regionserver):
                print(address)
                try:
                    server = valve.source.a2s.info(address,timeout=timeout_query)

                    datastack = [address[0],address[1],server.map_name,server.player_count]
                    if prefix in datastack[2]:
                        datastack.append(datetime.datetime.now().strftime(format))
                        print(f'!!!!{datastack} has been added')
                        response = requests.get(f"http://ip-api.com/json/{address[0]}").json()
                        region = response["countryCode"]
                        datastack.append(region)
                        ips.append(datastack)
                        x += 1
                except (AttributeError,valve.source.a2s.BrokenMessageError):
                    y += 1
                except socket.timeout:
                    z += 1
                print(f"{x}:deathrun servers {y}:server errors {z}:timeouts")

            print("__________")
            print(ips)
            return ips
        except valve.source.NoResponseError:
            print("Master server request timed out!")
# Writes input to csv use prefixcull for all servers
def ProtoWriter(list,file="output.csv"):
    try:
        with open(file,"r") as filedata:
            print("read successful")
    except:
        with open(file,"w",newline="") as filedata:
            print("NO FILE, MAKING NEW")

    with open(file,"a",newline="") as filedata:
            for ip in list:
                csv.writer(filedata).writerow(ip)
# Scans unique Ip's in .cvs file and appends new data to the list Much faster than scanning all the servers
def FastScan(file="output.csv"):
    iplist = []
    with open(file,"r") as filedata:
        csvreader = csv.reader(filedata)
        for ip in csvreader:
            if (ip[0],ip[1]) not in iplist:
                iplist.append((ip[0],ip[1]))
                print(iplist)
            else:
                print(f"{ip}:duplicate!!!!")
    return iplist
def Listscan(prefix="dr_",timeout_master=1,timeout_query=1,regionserver="all",list_ips=[]):
    format = '%Y-%m-%d-%H:%M:%S' # date format
    x = 0 # number of "broken" servers print me to see it
    y = 0 # number of timed out servers
    z = 0 #total servers
    ips = []
    try:
        for address in list_ips:
            fix_address = (address[0],int(address[1]))
            print(fix_address)
            try:
                server = valve.source.a2s.info(fix_address,timeout=timeout_query)

                datastack = [address[0],fix_address[1],server.map_name,server.player_count]
                if prefix in datastack[2]:
                    datastack.append(datetime.datetime.now().strftime(format))
                    print(f'!!!!{datastack} has been added')
                    response = requests.get(f"http://ip-api.com/json/{address[0]}").json()
                    region = response["countryCode"]
                    datastack.append(region)
                    ips.append(datastack)
                    x += 1
            except (AttributeError,valve.source.a2s.BrokenMessageError):
                
                
                y += 1
            except socket.timeout:
                z += 1
            print(f"{x}:deathrun servers {y}:server errors {z}:timeouts")

        print("__________")
        print(ips)
        return ips
    except valve.source.NoResponseError:
        print("Master server request timed out!")
# Runs in slow mode first to create initial server list, then in fast mode. Running in slowmode afterwards increase the sever pool that fast mode scans for.
def MainWriter(isfast,file):
    if isfast == True:
        a = Listscan(list_ips=FastScan(file))
        ProtoWriter(a,file)
    elif isfast == False:
        ProtoWriter(SlowScan(),file)
    else:
        print("Invalid mode!!! please use Ex. MainWriter(True,filex)")

#Run MainWriter in fast/slow mode for n minutes
def Iterator(file,delay=5,length=60,update=15):

    end = time() + length*60
    x = update
    while time() < end:
        if x >= update:
            print("Initiate SLOW SEARCH")
            MainWriter(False,file)
            x = 0
        else:
            print("Initiate FAST SEARCH")
            MainWriter(True,file)
            x += 1
            sleep(delay*60)

    print(f"{length} : minutes complete")

