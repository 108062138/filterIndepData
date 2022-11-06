from curses.ascii import isdigit, isspace
from lib2to3.pgen2 import token
import pathlib
import os
import sys
import getopt
import re
import numpy as np
import matplotlib.pyplot as plt
from torch import true_divide

drawer = {}

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def handle( container, index, root):
    block = container[index]
    res = []
    if index == 0:
        for line in block:
            tokens = line.split()
            if tokens[0] == root:
                for token in tokens:
                    if is_number(token) or token.endswith('0K'):
                        res.append(token)
            if tokens[0].endswith(':'):
                res.append(tokens[1])
    elif index == 1:
        flick = False
        for line in block:
            tokens = line.split()
            if flick:
                res.append(tokens)
            if tokens[0] == '------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------':
                flick = True
    elif index == 2:
        flick = False
        for line in block:
            tokens = line.split()
            if flick:
                res.append(tokens)
            if tokens[0] == '------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------':
                flick = True
    elif index == 3:
        for line in block:
            tokens = line.split()
            for token in tokens:
                if is_number(token) or token.endswith('0K'):
                    res.append(token)
                elif is_number(token[:-1]):
                    res.append(token[:-1])
    elif index == 4:
        for line in block:
            tokens = line.split()
            for token in tokens:
                if is_number(token) or token.endswith('0K'):
                    res.append(token)
                elif is_number(token[:-1]):
                    res.append(token[:-1])
    elif index == 6:
        for line in block:
            tokens = line.split()
            for token in tokens:
                if is_number(token) or token.endswith('0K'):
                    res.append(token)
                                    
    return res
    
def getOp(root, dataPath):
    rempref = root.removeprefix(dataPath)
    remsuff = rempref.split(',')[0]
    return remsuff

def handleData(dataPath, processedRes, drawFile):
    files = os.listdir(dataPath)
    for file in files:
        filePath = dataPath+str(file)
        f = open(filePath, 'r')
        op = getOp( filePath, dataPath + 'bmk_')
        
        lines = f.readlines()
        cntEmpty = 0
        lineN = 0
        block = []
        container = []
        lib = []

        for line in lines:
            lineN += 1
            if line.isspace():
                cntEmpty += 1
                if len(block) != 0:
                    container.append(block)
                block = []
                continue
            block.append(line)

        with open(processedRes + str(file)+'.txt','w') as f:
            for i in range(0, len(container)):
                filtRes = handle(container, i, op)
                if i==0:
                    nop = filtRes[2]
                    costTime = filtRes[10]
                    ctp = str(file).split('_')[3]
                    print(op, ctp, nop, costTime)
                    s = str(op+'_'+ctp)
                    print(s)
                    if op + '_' + ctp in drawer:
                        print('hit')
                        drawer[op+'_'+ctp][0].append(costTime)
                        drawer[op+'_'+ctp][1].append(int(nop)/500000)
                        
                    else:
                        drawer[op+'_'+ctp] = [[costTime], [int(nop)/500000]]
                    
                print(str(filtRes), file=f) 

if __name__ == '__main__':
    n = len(sys.argv)
    dirName = str(sys.argv[1])
    
    dataPath = str(os.getcwd()) + '/'+ dirName + '/'
    processedRes = str(os.getcwd()) + '/processed_' + dirName + '/'
    drawFile = str(os.getcwd()) + '/'+ dirName + '/' + 'collectedList'
    print(dataPath, dirName, processedRes)
    
    if not (os.path.exists(processedRes)):
        os.makedirs(processedRes)
    drawer = {}
    handleData(dataPath, processedRes, drawFile)
    
    print(drawer)
    
    for key in drawer:
        print(key)
        y = drawer[key][0]
        x = drawer[key][1]
        
        ybar = [ele for _,ele in sorted(zip(x,y))]
        xbar = sorted(x)
        print('haha')
        print(x)
        print(y)
        print(ybar)
        print(xbar)
        
        plt.plot(xbar, ybar, linestyle='dashed', linewidth=3, marker='o', markerfacecolor='blue', markersize=12, label=str(key))
        plt.axis([0,15,0,9])
        plt.legend()
        plt.xlabel('num of operation')
        plt.ylabel('time')
    plt.show()