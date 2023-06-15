# Exercise: Get Username and Password
# ex = 3.7, 3.8
import re
import getpass
from datetime import datetime
# Version 2
"""
name = input("Enter your name: ")
while True:
    while not re.match("^[a-zA-Z]+$", name):
        name = input("Enter your name: ")
    else:
        print(name)
        exit()
"""
"""
# Version 3
def get_name():
    name = input("Enter your name: ")
    while True:
        while not re.match("^[a-zA-Z]+$", name):
            name = input("Enter your name: ")
        else:
            print(name)
            exit()


get_name()
"""
"""
# Excersie: Practice for ~ in range
for n in range(2, 4):
    print(("Creating VLAN" + str(n)))

txt1 = "Seeya later alligator"
for line in txt1:
    print(line, end=" ")
"""
"""
# Excercise: Use getpass() Module and User Input


def get_pwd():
    username = input("Enter username: ")
    password = getpass.getpass()
    print(username, password)


get_pwd()
"""
# Excercise: convert dd-mmm-yy and Calculate the Difference in Days and Then in Years

IOS_rel_date = '12-Jul-17'
x = IOS_rel_date.replace('-', ' ')
y_day = (datetime.strptime(x, '%d %b %y')).date()
t_day = datetime.today().date()
delta = t_day - y_day
years = round(((delta.days)/365), 2)
print(delta.days)
print(years)
