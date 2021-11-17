#!/usr/bin/python3

import random

santas = []

try:
    with open('list.txt', 'r') as s:
        for name in s:
            santas.append(name.strip())
except FileNotFoundError:
    print('list.txt does not exist.\n exiting...')
    exit()


def retry(func):
    def inner(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except RuntimeError as e:
                print(e)
    return inner


@retry
def generate_list():
    gifted = santas[:]
    lst = []
    for x in santas:
        gift = random.choice(gifted)
        if gift is x and len(gifted) == 1:
            raise RuntimeError('Single person left in list, regenerating.')
        while gift is x:
            gift = random.choice(gifted)
        message = f'{len(lst) + 1}: {x} will draw for {gift}'
        lst.append(message)
        gifted.remove(gift)
    return lst


result = generate_list()
list(map(lambda x: print(x), result))

try:
    with open('output.txt', 'w') as o:
        for c in result:
            o.write(c + '\n')
except:
    print('something went wrong')
