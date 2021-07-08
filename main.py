#! /usr/bin/python3

import random

santas = []
gifted = []
count = 1

with open('list.txt', 'r') as s:
    for name in s:
        santas.append(name.strip())

gifted = santas[:]

for x in santas:
    gift = random.choice(gifted)
    while gift is x:
        gift = random.choice(gifted)
    print(str(count) + ': ' + x + ' will draw for ' + gift)
    count += 1
    gifted.remove(gift)
