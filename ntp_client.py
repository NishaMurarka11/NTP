from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time 
from NTPPacket import NTPPacket
import time
import datetime
import queue
import schedule
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker



class ntpClient():
	system_epooch =  datetime.date(*time.gmtime(0)[0:3])
	ntp_epooch = datetime.date(1900,1,1)
	ntp_delta = (system_epooch - ntp_epooch).days * 24 * 3600
	#ntp_delta = 0
	last_server_response_time = 0
	local_time_of_pkt_recv = 0
	host = "0.0.0.0" # The server.
	#host = "pool.ntp.org"
	#host = "192.168.0.6"
	port = 22222 # Port.
	#port = 123
	read_buffer = 1024 # The size of the buffer to read in the received UDP packet.
	address = ( host, port ) # Tuple needed by sendto.
	stats_dict = {}
	burst_no = 0
	min_delay_map = {}
	calls = 0;
	global job
	counter = 15
	MAX_RETRY = 3
	retry = 0


	def __init__(self) -> None:
    		socket.setdefaulttimeout(10)


	def createPacket(self):
		pkt = NTPPacket()
		pkt.version = 2
		pkt.mode = 3
		pkt.orig_timestamp= self.last_server_response_time
		pkt.recv_timestamp= self.local_time_of_pkt_recv  
		pkt.tx_timestamp = time.time() + self.ntp_delta
		print("sent time " +str(pkt.tx_timestamp))
		print("Packet Tuple "+str(pkt))
		return pkt

	def sendPacket(self,messageNumber, burst_no):
		try:
			print("TIME: {} {} {} ".format(str(time.time),str(messageNumber),str(burst_no)))
			pkt = self.createPacket()
			pkt = pkt.packData()
			print("Packet Byte"+str(pkt))
			client = socket.socket( AF_INET, SOCK_DGRAM )
			#client.setblocking(False)
			client.sendto( pkt, self.address ) 
			data, address = client.recvfrom( self.read_buffer )
			self.local_time_of_pkt_recv = time.time() + self.ntp_delta
			responsePkt = NTPPacket()
			print("Data "+ str(data))
			responsePkt.unpackData(data)
			meta_lis = self.calculateDispersion(responsePkt,messageNumber,burst_no)
			print("Response "+ str(responsePkt))
			last_server_response_time = responsePkt.tx_timestamp
			self.displayResponse(responsePkt)
			return meta_lis
		except socket.timeout as e:
			print("timeout for message"+str(messageNumber)+" "+str(burst_no))
			self.retry = self.retry + 1
			if self.retry >= self.MAX_RETRY:
				print("returning timeout")
				return (-1,"Timeout")
			return self.sendPacket(messageNumber,burst_no)


		# scheduler = sched.scheduler(time.time, 
  #                           time.sleep)

				# change 2 to 4 and seconds to minutes
		
		# 1 hour period (8 packet burst every 4mins) - calcularte min(delta) and min(offset)
		
		# schedule.every(4).seconds.do(self.sendPacket())

		# schedule.run_pending()

	def updateData(self,messageNumber,burst_no,meta_lis):
		key  = str(messageNumber)+","+str(burst_no)
		self.stats_dict[key] = meta_lis




	def calculateDispersion(self, responsePkt,messageNumber,burst_no):
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
		meta_lis = []
		meta_lis.append(delta)
		meta_lis.append(offset)
		self.updateData(messageNumber,burst_no,meta_lis)
		return meta_lis
		

	def displayResponse(self,responsePkt):
		print("Origin TimeStamp "+ time.ctime(responsePkt.orig_timestamp-self.ntp_delta))
		print("Transit TimeStamp "+time.ctime(responsePkt.tx_timestamp-self.ntp_delta))
		print("Receive TimeStamp "+ time.ctime(responsePkt.recv_timestamp-self.ntp_delta))


	def plotAll(self,stats_dict,min_delay_map):
		lists = sorted(stats_dict.items()) # sorted by key, return a list of tuples
		print("Lists"+ str(lists))
		x, y = zip(*lists) # unpack a list of pairs into two tuples
		print("X "+ str(x))
		print("Y "+ str(y))
		objects = plt.plot(x, y)
		plt.xlabel('Burst_no #, message_pair')
		plt.ylabel('Delay , Offset')
		plt.legend(iter(objects), ('Delay', 'Offset') , loc="upper left")
		plt.show()

		lists2 = sorted(min_delay_map.items())
		x, y = zip(*lists) # unpack a list of pairs into two tuples
		object2 = plt.plot(x, y)
		plt.xlabel('Burst_no')
		plt.ylabel('Delta , theta')
		plt.legend(iter(object2), ('Delta', 'theta'))
		plt.show()

	
	def plotFunction(self,stats_dict,min_delay_map):

		lists = sorted(stats_dict.items()) # sorted by key, return a list of tuples
		print("Lists"+ str(lists))
		x, y = zip(*lists) # unpack a list of pairs into two tuples
		delay, offset = map(list, zip(*y))
		print("X "+ str(x))
		print("Y "+ str(y))
		# objects = plt.plot(x, y)


		lists2 = sorted(min_delay_map.items())
		x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
		delta, theta = map(list, zip(*y2))
		# plt.xlabel('Burst_no')
		# plt.ylabel('Delta , theta')
		# plt.legend(iter(object2), ('Delta', 'theta'))
		# plt.show()


		figure, axis = plt.subplots(2, 2)
		# ax = plt.axes()
		# ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
  
		# For Sine Function
		axis[0, 0].plot(x, delay, '-r')
		axis[0, 0].set_title("Burst_no #, message_pair vs Delay (di)")
		  
		# For Cosine Function
		axis[0, 1].plot(x, offset, '-g')
		axis[0, 1].set_title("Burst_no #, message_pair vs offset (oi)")
		  
		# For Tangent Function
		axis[1, 0].plot(x2, delta, '-b')
		axis[1, 0].set_title("Burst_no # vs delta")
		  
		# For Tanh Function
		axis[1, 1].plot(x2, theta, 'm')
		axis[1, 1].set_title("Burst_no # vs theta")
		  
		# Combine all the operations and display
		plt.show()


	def sendBurstPackets(self):
		self.calls = self.calls+1
		if(self.calls>self.counter):
			schedule.cancel_job(self.job)
			return

		
		self.burst_no = self.burst_no+1
		delay_offest_pair_lis = []
		for i in range (8):
			meta_lis = self.sendPacket(i,self.burst_no)
			# Storing delay and offset as a pair, to calculate minimum delay at the end of the burst
			if meta_lis[0] == -1:
				print("Check ")
				schedule.cancel_job(self.job)
				self.calls = self.counter + 1
				break
			delay_offest_pair_lis.append((meta_lis[0], meta_lis[1]))

		#  sort by delay
		
		
		# take the smallest delay and corresponding offeset 
		if delay_offest_pair_lis:
			delay_offest_pair_lis.sort(key=lambda x:x[0])
			min_delay = delay_offest_pair_lis[0][0]
			min_offest = delay_offest_pair_lis[0][1]
			self.min_delay_map[self.burst_no] = ((min_delay,min_offest))	
		else:
			print("No Message delivered")
			return
		
		
		# Setting the min delay offset pair to a map with burst number as the key

		


	def schedule(self):
		self.job = schedule.every(4).seconds.do(self.sendBurstPackets)
		# scheduler.enter(2, 1,  
		#                    self.sendPacket)
		# schedule.cancel_job(job)
		count = 0;	
		while(True):
			schedule.run_pending()
			time.sleep(1)
			if self.calls>self.counter:
				break

		print("CALLS "+ str(self.calls))
		print("Stats Dict :", str(self.stats_dict))
		print("Min Delay per burst "+ str(self.min_delay_map))
		self.plotFunction(self.stats_dict,self.min_delay_map)


client = ntpClient()
client.schedule()








