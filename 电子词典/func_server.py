from pymongo import MongoClient
from socket import *
import sys
import re
from time import sleep
from signal import *
import datetime
def handle_msg(conn,addr):
    name=""
    while True:
        data=conn.recv(1024).decode()
        print(data)
        if not data:
            conn.close()
            sys.exit(str(addr)+"已退出")
        elif data=="m1-1":
            s,name=login(conn)
            conn.send(s.encode())
        elif data=="m1-2":
            s=register(conn)
            conn.send(s.encode())
        elif data=="m1-3":
            conn.close()
            print(addr,"exit")
            sys.exit()
        elif data=="m2-1":
            find_word(conn,name)
        elif data=="m2-2":
            find_history(conn,name)
        else:
            print("error")

def find_history(conn,name):
    Mconn=MongoClient('localhost',27017)
    db=Mconn.stu
    myset=db.his
    cursor=myset.find({"name":name},{"_id":0})
    for i in cursor:
        conn.send(str(i).encode())
        print(i)
        sleep(0.1)
    else:
        conn.send(b"#")
        Mconn.close()

def find_word(conn,name):
    Mconn=MongoClient('localhost',27017)
    db=Mconn.stu
    myset=db.dict
    myset1=db.his
    while True:
        word=conn.recv(1024).decode()
        if word=="#":
            Mconn.close()
            break    
        cursor=myset.find_one({"word":word},{"_id":0})
        myset1.insert({"name":name,"word":word,"time":str(datetime.datetime.now())})
        if not cursor:
            conn.send(b"not found")
        else:
            conn.send(cursor['note'].encode())


def login(conn):
    Mconn=MongoClient('localhost',27017)
    db=Mconn.stu
    myset=db.user 
    name=conn.recv(1024).decode()
    password=conn.recv(1024).decode()
    cursor=myset.find_one({"name":name},{'_id':0})
    print(cursor)
    if not cursor:
        Mconn.close()
        return "没有此用户",None
    else:
        if password==cursor['password']:
            Mconn.close()
            return "success",name
        else:
            Mconn.close()
            return "密码错误",None

def import_word():
    conn=MongoClient('localhost',27017)
    db=conn.stu
    myset=db.dict
    myset.remove({})

    f=open("dict.txt")
    while True:
        s=f.readline()
        if not s:
            break
        pattern="\w+"
        word=re.search(pattern,s).group()
        note=s[s.find(word)+len(word):].strip()
        myset.insert({"word":word,"note":note})
    f.close()
    conn.close()

def register(conn):
    Mconn=MongoClient('localhost',27017)
    db=Mconn.stu
    myset=db.user
    name=conn.recv(1024).decode()
    password=conn.recv(1024).decode()
    cursor=myset.find_one({"name":name},{'_id':0})
    print(cursor)
    if not cursor:
        myset.insert({"name":name,"password":password})
        Mconn.close()
        return "success"
    else:
        Mconn.close()
        return "fail"      