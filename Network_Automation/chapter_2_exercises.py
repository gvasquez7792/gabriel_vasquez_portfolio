from time import asctime, sleep
import os
import glob
import sys

print("\nWelcome User\n")

# Exercise 2-69/70/71: Read, Display, Close Hosts File from your PC
"""try:
    hosts = open('/private/etc/hosts', 'r', encoding='utf-8')
    hosts_read = hosts.read()
    print(hosts_read)
finally:
    print('File Closed: {}'.format(hosts.closed))
    if not hosts.closed:
        hosts.close()
    print('File Closed: {}'.format(hosts.closed))
"""
# Exercise 2-72: Create a text file to read, write, and print
"""
file = open(
    "file1.txt", 'w')
for i in range(3):
    file.write('This is line %d.\r' % (i + 1))
file.close()  # Always close file. Data gets written as file closes
file = open(
    "file1.txt")
file_read = file.read()
print(file_read.strip())  # .strip() removes undesired whitespaces
file.close()
"""
"""
try:
    if os.path.isfile('file2.txt') is False:
        with open('file2.txt', 'w+') as file:
            for i in range(3):
                file.write("This is line %d.\r\n" % (i+1))
        with open('file2.txt', 'r') as file:
            for line in file:
                print(line)
    elif os.path.isfile('file2.txt') is True:
        os.remove('file2.txt')
        print('file deleted')
except os.path.isfile('file2.txt', 'x') as e:
    print(str(e))
"""
# Excersie 2-84
for path in sys.path:
    print(path)
