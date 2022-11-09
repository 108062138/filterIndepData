from curses.ascii import isspace
from lib2to3.pgen2 import token
import pathlib
import os
import sys
import getopt
import re
import numpy as np
import matplotlib.pyplot as plt

drawer = {}
differ = {}
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
            if flick and tokens[0] == 'Sum':
                res = tokens
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

def handleData(dataPath, processedRes, ssdType):
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
            print(str(file))
            ctp = str(file).split('_')[3]
            lineName = op + '_' + ctp + '_' + ssdType
            costTime = 0
            for i in range(0, len(container)):
                filtRes = handle(container, i, op)
                if i==0:
                    costTime = filtRes[10]
                    nop = filtRes[2]
                    costTime = filtRes[10]
                    if lineName in drawer:
                        drawer[lineName][1].append(int(nop)/1000000)
                    else:
                        drawer[lineName] = [[], [int(nop)/1000000]]    
                elif i==1:
                    drawer[lineName][0].append(int(filtRes[16]) * float(filtRes[17])/float(costTime))
                print(str(filtRes), file=f) 
                

if __name__ == '__main__':
    n = len(sys.argv)
    dirName = str(sys.argv[1])
    argssd = str(sys.argv[1]).split('_')[-1]
    anotherssd = 'nan'
    if argssd=='blackssd':
        anotherssd = 'znsssd'
    else:
        anotherssd = 'blackssd'
    
    newDirName = ''
    for i in range(0,len(sys.argv[1].split('_'))-1):
        if newDirName=='':
            newDirName = str(sys.argv[1]).split('_')[i]
        else:
            newDirName = newDirName + '_' + str(sys.argv[1]).split('_')[i]
    newDirName = newDirName + '_' + anotherssd
    
    for dirName in [dirName, newDirName]:
    
        dataPath = str(os.getcwd()) + '/'+ dirName + '/'
        processedRes = str(os.getcwd()) + '/processed_' + dirName + '/'
        print(dataPath, dirName, processedRes, newDirName)
        ssdType = argssd

        if not (os.path.exists(processedRes)):
            os.makedirs(processedRes)

        drawer = {}  
        handleData(dataPath, processedRes, ssdType)

        for key in drawer:
            y = [float(ele) for ele in drawer[key][0]]
            x = [float(ele) for ele in drawer[key][1]]

            ybar = [ele for _,ele in sorted(zip(x,y))]
            xbar = sorted(x)
            if dirName.split('_')[-1] == 'blackssd':
                plt.plot(xbar, ybar, linestyle='dashed', linewidth=3, marker='o', markerfacecolor='blue', markersize=12, label=str(key))
                differ[str(key)] = [ybar, xbar]
            else:
                ks = [str(ele) for ele in key.split('_')[:-1]]
                difKey = ''
                for ele in ks:
                    if difKey == '':
                        difKey = ele
                    else: difKey= difKey + '_' + ele
                difKey = difKey + '_' + 'znsssd'
                plt.plot(xbar, ybar, linestyle='dashed', linewidth=3, marker='H', markerfacecolor='red', markersize=12, label=str(difKey))
                differ[difKey] = [ybar, xbar]
            
    genFigName = 'compactionRatio' + str(dirName)
    plt.title('compaction ratio')
    plt.axis([0,14,0,1])
    plt.legend()
    plt.xlabel('num of operation(1M op/unit)')
    plt.ylabel('compaction percentage(sum of comp. time/total time)')
    processedRes = str(os.getcwd()) + '/everyssdFig/'
    if not (os.path.exists(processedRes)):
        os.makedirs(processedRes)
    plt.savefig(processedRes+genFigName)
    plt.show()
        
    print('enter div same ssd')
    for key in differ:
        print(key)
        if key.split('_')[0] == 'fillrandom':
            print('zz')
            ks = [str(ele) for ele in key.split('_')[1:]]
            difKey = ''
            for ele in ks:
                if difKey == '':
                    difKey = ele
                else: difKey= difKey + '_' + ele
            difKey = 'fillseq' + '_' + difKey
            
            
            y = differ[key][0]
            x = differ[key][1]
            z = []
            for i in range(0, len(x)):
                z.append(differ[difKey][0][i] / y[i])
            print(x,y)
            if ks[-1] == 'znsssd':
                plt.plot(x, z, linestyle='dashed', linewidth=3, marker='*', markerfacecolor='red', markersize=12, label=key)
            else:
                plt.plot(x, z, linestyle='dashed', linewidth=3, marker='.', markerfacecolor='blue', markersize=12, label=key)
    plt.title('compaction ratio among same ssd on different benchmark')
    plt.legend()
    plt.axis([0,14,0,2])
    plt.xlabel('num of operation(1M op/unit)')
    plt.ylabel('ratio(#time on seq/#time on random)')
    genFigName = 'divTime_cmpdivall_random_by_seqwrite_' + str(dirName)
    processedRes = str(os.getcwd()) + '/everyssdFig/'
    plt.savefig(processedRes+genFigName)
    plt.show()