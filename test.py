import datetime


format = '%Y-%m-%d-%H:%M:%S'
yearX = int(input("choose a year EX. 2021"))
monthX = int(input("choose a month EX. 12"))
lengthX = int(input("choose a length in months EX. 1"))
a = "2021-09-20-04:10:36"

if datetime.datetime.strptime(a,format) > datetime.datetime(yearX,monthX,1): #min
    print("Yes")
else:
    print("no")