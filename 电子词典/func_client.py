from pymongo import MongoClient
import sys
import re
from socket import *
from time import sleep
import getpass
def show_menu():
    print("\n       =======m e n u======")
    print("              1.登录")
    print("              2.注册")
    print("              3.退出")
    print("       ====================\n")

def show_service():
    print("\n       =======service======")
    print("           1.查单词")
    print("           2.查看历史记录")
    print("           3.退出")
    print("       =======service======\n")

def login(sockfd):
    name=input("请输入用户名:")
    sockfd.send(name.encode())
    password=getpass.getpass("请输入密码:")
    sockfd.send(password.encode())
    data=sockfd.recv(1024).decode()
    if data=="success":
        return data,name
    else:
        return data,None


def Main1(sockfd): 
    name=""
    while True:
        show_menu()
        select=input("请输入选项:")
        if select=="1":
            sockfd.send(b"m1-1")
            data,name=login(sockfd)
            sleep(0.1)
            if data=="success":
                Main2(sockfd,name)
            else:
                print(data)
        elif select=="2":
            sockfd.send(b"m1-2")
            register(sockfd)
        elif select=="3":
            sockfd.send(b"m1-3")
            sockfd.close()
            sys.exit()
        else:
            print("select error")
    

def find_word(sockfd):
    while True:
        word=input("请输入要查找的单词:")
        if not word:
            sockfd.send(b"#")
            break
        sockfd.send(word.encode())
        note=sockfd.recv(1024).decode()
        if note=="not found":
            print(note)
        else:
            print("note:",note)
def find_history(sockfd,name):
    print("\n******************hist******************")
    print("User:"+name)
    print("******************list******************")
    while True:
        data=sockfd.recv(1024).decode()
        if data=="#":
            print("******************over******************\n")
            break
        data=eval(data)
        print(data['word']+(14-len(data['word']))*" "+data['time'])


def Main2(sockfd,name):
    while True:
        show_service()
        select=input("请输入服务：")
        if select=="1":
            sockfd.send(b"m2-1")
            find_word(sockfd)
            #查单词
        elif select=="2":
            print(name)
            sockfd.send(b"m2-2")
            find_history(sockfd,name)
            #查看历史记录
        elif select=="3":
            #退出
            Main1(sockfd)
        else:
            print("请输入正确命令")

def register(sockfd):
    name=input("register your name:")
    sockfd.send(name.encode())
    password=input("register your password:")
    sockfd.send(password.encode())
    data=sockfd.recv(1024).decode()
    if data=="success":
        print("register success!")
    elif data=="fail":
        print("register failed!")
    else:
        print("register error")

#import getpass
#pass=getpass.getpass()