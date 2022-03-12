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
python socket - UDP socket 
matplotlib - ploting data metric
schedule - Creating a scheduler to run a code in regular interval
datetime -  for converting epoch into datatime
struct -  for packing and unpacking of byte data into object
traceback -  for exception handling and trace
## RESULTS:

All the plots are in the file Graphs.pdf
All the offset and delay metrics are populated in three different .xlsx files:

GCP.xlsx [server at GCP, Local client]
LAN.xlsx [server and client in the same LAN]
ntp.xlsx [NTP server ("pool.ntp.org")  and local client ]
