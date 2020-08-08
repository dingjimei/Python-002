import sys
import multiprocessing as mp
from multiprocessing import Process
from multiprocessing.pool import Pool
import socket
from time import time
import json
import os

MY_LIST = set(('-n', '-f', '-ip', '-w', '-v')) 
cpu = 4
iplist = list()

def myPing(ip,filename,mylock):
    backinfo = os.system('ping -c 1 -w 1 %s'%ip) # 实现pingIP地址的功能，-c1指发送报文一次，-w1指等待1秒 
    if backinfo: 
        print ('%s not online'%ip)
    else: 
        try:
            mylock.acquire()
            with open(filename, "a+", encoding="utf-8") as myfile:
                myfile.write(ip)
                myfile.write('\n')
        except IOError:
            print("文件操作失败")
        finally:
            mylock.release()

def myPortCheck(ip,port):
    try:
        connSkt = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        connSkt.connect((ip,port))
        print("tcp open port:" + str(port))
    except:
        print('tcp closed:'+str(port))

if __name__ == "__main__":
    argv_list = sys.argv 
    mylock = mp.Manager().RLock()
    #解析命令行参数
    argv1 = None
    argv2 = None
    argv3 = False
    ipscope = list()
    for i in argv_list:
        if i.startswith('-') and i not in MY_LIST:
            print("无效的参数：" + i)
        elif i == '-n':
            argv1 = int(argv_list[argv_list.index('-n') + 1])
        elif i == '-f':
            argv2 = argv_list[argv_list.index('-f') + 1]
        elif i == '-ip':
            ip_argv = argv_list[argv_list.index('-ip') + 1]
            ipscope = ip_argv.split('-')
        elif i == '-w':
            argv3 = argv_list[argv_list.index('-w') + 1]

    mypool = Pool(argv1)
    if argv2 == "ping":
        split_1 = ipscope[0].split('.')
        split_2 = ipscope[1].split('.')
        if split_1[0] != split_2[0] or split_1[1] != split_2[1] or split_1[2] != split_2[2] or split_1[-1] == split_2[-1]:
            print ("错误的ip地址范围，请重新输入")
        else:
            ip_part = ipscope[0][:ipscope[0].rfind('.')+1]
            if split_1[-1] > split_2[-1]:
                split_1[-1], split_2[-1] = split_2[-1], split_1[-1]
            for i in range(int(split_1[-1]), int(split_2[-1])+1):
                ip = ip_part + str(i)
                mypool.apply_async(func=myPing, args=(ip, argv2, mylock))
    elif argv2 == "tcp":
        for i in range(1,65535):
            mypool.apply_async(func=myPortCheck, args=(ipscope[0], i))

    mypool.close()
    mypool.join()