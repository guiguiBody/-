# import re

# f=open("dict.txt")
# s=f.readline()
# pattern="\w+"
# word=re.search(pattern,s).group()
# note=s[s.find(word)+len(word):].strip()
# f.close()


# import getpass

# while True:
#     name=input("User:")
#     passwd=getpass.getpass("shi")
#     print(passwd)
# from pymongo import MongoClient
# Mconn=MongoClient('localhost',27017)
# db=Mconn.stu
# myset=db.his
# cursor=myset.find({"name":"edu"},{"_id":0})
# for i in cursor:
#     print(i)
#     print(i['name'])

# a={'name': 'edu', 'word': 'find', 'time': datetime.datetime(2018, 9, 28, 15, 35, 58, 913000)}
# print(a['name'])

import re
f=open("11.txt")
a=re.findall(r"\d+",f.read(),re.M)
print(a)
a=re.sub(r"\d+","a","123 456")
print(a)
f.close