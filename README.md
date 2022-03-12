# NTP
Ntp server and client implementation
description of how to compile and run your program.

## How to compile :
  After installing necessary packages, python3 ntp_server.py will start the server and python3 ntp_client.py will start the client.


## NTP CLIENT : 
  Schedule is used to send burst messages in every 4 minutes. We are counting the number of times this schedule is done. For this assignment we are scheduling 15 burst message with each burst containing 8 message. 
  For timeout we are setting the default timeout of socket and number of retries after timeout can be configured. 
  For checking duplicate packets we are checking the origin timestamp in the recieved message if the origin timestamp is already present then its a duplicate message which is discared. 
  
## NTP SERVER : 
  In case of NTP sever we are open UDP socket with two threads, the first thread recieves packets and places it in a queue, the second thread pops the packet from the queue and does the processing. The NTP packet class has the fields for unpacking and packing a packet.

## PACKAGES USED
python socket - UDP socket <br/>
matplotlib - ploting data metric <br/>
schedule - Creating a scheduler to run a code in regular interval <br/>
datetime -  for converting epoch into datatime <br/>
struct -  for packing and unpacking of byte data into object <br/>
traceback -  for exception handling and trace <br/>
## RESULTS:

All the plots are in the file Graphs.pdf <br/>
All the offset and delay metrics are populated in three different .xlsx files: <br/>

GCP.xlsx [server at GCP, Local client] <br/>
LAN.xlsx [server and client in the same LAN] <br/>
ntp.xlsx [NTP server ("pool.ntp.org")  and local client ] <br/>


##  The shorter and more symmetric the round-trip time is, the more accurate the estimate of the current time will be. 

Synchronizing a client to a network server consists of several packet exchanges where each exchange is a pair of request and reply. When sending out a request, the client stores its own time (originate timestamp) into the packet being sent. When a server receives such a packet, it will in turn store its own time (receive timestamp) into the packet, and the packet will be returned after putting a transmit timestamp into the packet. When receiving the reply, the receiver will once more log its own receipt time to estimate the travelling time of the packet. The travelling time (delay) is estimated to be half of "the total delay minus remote processing time", assuming symmetrical delays. [Definition from NTP]

We can conclude from our plot when the delay is less i.e shorter round trips than the offset decreases which leads to lesser delta on the local time and the server time. Since in our dispersion (maximum offset error) calculation we assume a symmetric round trip will decrease the offset error and we can conclude that the local time calculated will be more closer to the actual server time. 


From the above figure we can see in case of LAN since the round trip is shorter we can see more consistent data.
The delay and offset is less as compared to server running in GCP and NTP server. Also in NTP we can experience regular timeouts since we are hitting lower stratum servers.



