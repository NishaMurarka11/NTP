import datetime
import socket
import threading
from NTPPacket import NTPPacket
import select
import time
import queue
import traceback


packet_queue = queue.Queue()
flag = False
ERROR_CODE = -1


class NTP:
    system_epooch =  datetime.date(*time.gmtime(0)[0:3])
    ntp_epooch = datetime.date(1900,1,1)
    ntp_delta = (system_epooch - ntp_epooch).days * 24 * 3600

class recievePacket(threading.Thread):
    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
    
    def run(self):
        while True:
            if flag:
                break
            try:
                readable,writable,exceptional = select.select([self.socket],[],[],1);
                if len(readable) != 0:
                    for tempSocket in readable:
                        data,addr = tempSocket.recvfrom(1024)
                        server_recieve_timestamp = time.time() + NTP.ntp_delta
                        packet_queue.put((data,addr,server_recieve_timestamp))
            except Exception as e:
                traceback.print_exc()
                print(str(e))
        
class processPacket(threading.Thread):

    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket

    def run(self):
        while True:
            if flag:
                break
            try:
                if not packet_queue.empty():
                    data,addr,recvTimestamp = packet_queue.get(timeout=1)
                    recvPacket = NTPPacket()
                    recvPacket.unpackData(data)
                    timeStamp_high,timeStamp_low=recvPacket.getTxTimeStamp();
                    sendPacket = NTPPacket()
                    sendPacket.version = 3
                    sendPacket.mode = 4
                    sendPacket.ref_timestamp = recvTimestamp-5
                    sendPacket.orig_timestamp_high = timeStamp_high
                    sendPacket.orig_timestamp_low = timeStamp_low
                    sendPacket.recv_timestamp = recvTimestamp
                    sendPacket.tx_timestamp = time.time() + NTP.ntp_delta
                    self.socket.sendto(sendPacket.packData(),addr)
            except Exception as e:
                traceback.print_exc()
                print(str(e))  

class NTPServer():
    
    def start_udp_connection(self,host,port):
        server = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
        server.bind((host,port))
        recvTh = recievePacket(server)
        recvTh.start()
        workTh = processPacket(server)
        workTh.start()
        while True:
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                flag = True
            recvTh.join()
            workTh.join()
            break
        
server = NTPServer()
server.start_udp_connection("0.0.0.0",22222)
