import struct


ERROR_CODE = -1
class NTPPacket():
    
    _PACKET_FORMAT = "!B B B b 11I"
    
    def __init__(self):
        self.leap = 0
        self.version = 0
        self.mode = 0
        self.stratum = 0
        self.poll = 0
        self.precision = 0
        self.root_delay = 0
        self.root_dispersion = 0
        self.ref_id = 0
        self.ref_timestamp_low = 0
        self.ref_timestamp_high = 0
        self.orig_timestamp_high = 0
        self.orig_timestamp_low = 0
        self.recv_timestamp_high = 0
        self.recv_timestamp_low = 0
        self.tx_timestamp_high = 0
        self.tx_timestamp_low = 0
        
    def getTxTimeStamp(self):
        return (self.tx_timestamp_high,self.tx_timestamp_low)

    def unpackData(self,packet):
        try:
            unpacked_packet = struct.unpack(NTPPacket._PACKET_FORMAT,
                        packet[0:struct.calcsize(NTPPacket._PACKET_FORMAT)])
        except Exception as e:
            return (ERROR_CODE,str(e))   
        
        self.leap = unpacked_packet[0] >> 6 & 0x3
        self.version = unpacked_packet[0] >> 3 & 0x7
        self.mode = unpacked_packet[0] & 0x7
        self.stratum = unpacked_packet[1]
        self.ref_timestamp_low = unpacked_packet[7]
        self.ref_timestamp_high = unpacked_packet[8]
        self.orig_timestamp_high = unpacked_packet[9]
        self.orig_timestamp_low = unpacked_packet[10]
        self.tx_timestamp_high = unpacked_packet[13]
        self.tx_timestamp_low = unpacked_packet[14]
        
    def packData(self):
        try:
            packet = struct.pack(NTPPacket._PACKET_FORMAT,
                (self.leap << 6 | self.version << 3 | self.mode),
                    self.stratum,
                    self.poll,
                    self.precision,
                    self.root_delay,
                    self.root_dispersion,
                    self.ref_id,
                    self.ref_timestamp_low,
                    self.orig_timestamp_high,
                    self.orig_timestamp_low,
                    self.recv_timestamp_high,
                    self.recv_timestamp_low,
                    self.tx_timestamp_high,
                    self.tx_timestamp_low)
        except Exception as e:
            return (ERROR_CODE,str(e))
    