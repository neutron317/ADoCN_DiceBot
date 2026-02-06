#!/usr/bin/env python3
import random
import re
import csv

def roll(n):
    res = []
    for i in range(n):
        res.append(random.randint(1, 6))
    return res

def sumnumbers(matched):
    txt = ''
    sum = 0

    if matched != None:
        addnums = re.findall(r'[+-]\d+', matched.group())
        for i in addnums:
            txt += i
            sum += int(i)
    return [txt, sum]

def d66():
    fst = roll(1)
    sec = roll(1)
    return fst[0] * 10 + sec[0]

def d66table(file):
    diceresult = d66()
    dicetuple = [diceresult]
    with open(file) as table_file:
        reader = csv.reader(table_file)
        above_row = []
        for row in reader:
            if int(row[0]) == diceresult:
                return dicetuple + row
            elif int(row[0]) > diceresult:
                return dicetuple + above_row
            above_row = row

def d6table(file):
    diceresult = roll(1)[0]
    dicetuple = [diceresult]
    with open(file) as table_file:
        reader = csv.reader(table_file)
        above_row = []
        for row in reader:
            if int(row[0]) == diceresult:
                return dicetuple + row
            elif int(row[0]) > diceresult:
                return dicetuple + above_row
            above_row = row