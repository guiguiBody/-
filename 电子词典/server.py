from socket import *
import os
from func_server import *
import signal
import sys
from pymongo import MongoClient
sockfd=socket()
sockfd.bind(("0.0.0.0",8888))
sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sockfd.listen(5)
signal.signal(signal.SIGCHLD,signal.SIG_IGN)
#import_word()
while True:
    try:
        conn,addr=sockfd.accept()
    except KeyboardInterrupt:
        sockfd.close()
        sys.exit()
    except:
        conn.close()
        continue
    print("connect from ",addr)
    pid=os.fork()
    if pid<0:
        print("error")
    elif pid==0:
        sockfd.close()
        handle_msg(conn,addr)
    else:
        conn.close()
        continue