#! /usr/bin/python3

import random

santas = []
gifted = []
lst = []
count = 1

try:
    with open('list.txt', 'r') as s:
        for name in s:
            santas.append(name.strip())
except FileNotFoundError:
    print('list.txt does not exist.\n exiting...')
    exit()

gifted = santas[:]

for x in santas:
    gift = random.choice(gifted)
    while gift is x:
        gift = random.choice(gifted)
    message = str(count) + ': ' + x + ' will draw for ' + gift
    print(message)
    lst.append(message)
    count += 1
    gifted.remove(gift)

try:
    with open('output.txt', 'a') as o:
        for c in lst:
            o.write(c + '\n')
except:
    print('something went wrong')
