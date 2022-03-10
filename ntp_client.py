from socket import AF_INET, SOCK_DGRAM # For setting up the UDP packet.
import sys
import socket
import struct, time # To unpack the packet sent back and to convert the seconds to a string.
from NTPPacket import NTPPacket
import time
import datetime



# data = '\x1b' + 47 * '\0' # Hex message to send to the server.

# epoch = 2208988800L # Time in seconds since Jan, 1970 for UNIX epoch.


# t = struct.unpack( "!12I", data )[ 10 ] # Unpack the binary data and get the seconds out.

# t -= epoch; # Calculate seconds since the epoch.

# print("Time = %s" % time.ctime( t )) # Print the seconds as a formatted string.


class ntpClient():
	system_epooch =  datetime.date(*time.gmtime(0)[0:3])
	ntp_epooch = datetime.date(1900,1,1)
	ntp_delta = (system_epooch - ntp_epooch).days * 24 * 3600
	#ntp_delta = 0
	last_server_response_time = 0
	local_time_of_pkt_recv = 0
	host = "0.0.0.0" # The server.
	#host = "pool.ntp.org"
	port = 22222 # Port.
	#port = 123
	read_buffer = 1024 # The size of the buffer to read in the received UDP packet.
	address = ( host, port ) # Tuple needed by sendto.



	def createPacket(self):
		pkt = NTPPacket()
		pkt.version = 2
		pkt.mode = 3
		pkt.orig_timestamp= self.last_server_response_time
		pkt.recv_timestamp= self.local_time_of_pkt_recv  
		pkt.tx_timestamp = time.time() + self.ntp_delta
		print("sent time" +str(pkt.tx_timestamp))
		print("Packet Tuple"+str(pkt))
		return pkt

	def sendPacket(self):
		pkt = self.createPacket()
		pkt = pkt.packData()
		print("Packet Byte"+str(pkt))
		client = socket.socket( AF_INET, SOCK_DGRAM )
		client.sendto( pkt, self.address ) 
		data, address = client.recvfrom( self.read_buffer )
		self.local_time_of_pkt_recv = time.time() + self.ntp_delta
		responsePkt = NTPPacket()
		print("Data "+ str(data))
		responsePkt.unpackData(data)

		self.calculateDispersion(responsePkt)

		print("Response "+ str(responsePkt))
		last_server_response_time = responsePkt.tx_timestamp
		self.displayResponse(responsePkt)

	def calculateDispersion(self, responsePkt):
		t1 = responsePkt.orig_timestamp 
		t2 = responsePkt.recv_timestamp 
		t3 = responsePkt.tx_timestamp 
		t4 = self.local_time_of_pkt_recv
		print("t1 "+ str(t1))
		print("t2 "+ str(t2))
		print("t3 "+ str(t3))
		print("t4 "+ str(t4))
		delta = ((t4-t1) - (t3-t2))
		offset = 0.5*((t2-t1) + (t3-t4))

		print("Delta "+ str(delta))
		print("Offset "+str(offset))



	def displayResponse(self,responsePkt):
		print("Origin TimeStamp "+ time.ctime(responsePkt.orig_timestamp+self.ntp_delta))

		print("Transit TimeStamp "+time.ctime(responsePkt.tx_timestamp+self.ntp_delta))

		print("Receive TimeStamp "+ time.ctime(responsePkt.recv_timestamp+self.ntp_delta))



client = ntpClient()
client.sendPacket()








