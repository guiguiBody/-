import sys
from func_client import *
from socket import *

sockfd=socket()
addr=("localhost",8888)
try:
    sockfd.connect(addr)
    Main1(sockfd)
except KeyboardInterrupt:
    sockfd.close()
    sys.exit("退出")
except:
    sockfd.close()
