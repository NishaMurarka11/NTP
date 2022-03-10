import struct
import traceback


ERROR_CODE = -1
class NTPPacket():
    
    packet = "!B B B b 11I"
    
    def __init__(self):
        #### first 4 bytes ####
        self.leap = 0
        self.version = 0
        self.mode = 0
        self.stratum = 0
        self.poll = 0
        self.precision = 0
        #### 
        self.root_delay = 0
        ####
        self.root_dispersion = 0
        ####
        self.ref_id = 0
        #####
        self.ref_timestamp = 0
        #####
        self.origin_timestamp_int_byte = 0
        self.origin_timestamp_frac_byte = 0
        self.orig_timestamp = 0
        ####
        self.recv_timestamp = 0
        ####
        self.tx_timestamp_int_byte = 0
        self.tx_timestamp_frac_byte = 0
        self.tx_timestamp = 0
        
    def getTxTimeStamp(self):
        return (self.tx_timestamp_int_byte,self.tx_timestamp_frac_byte)

    def unpackData(self,packet):
        try:
            unpacked_packet = struct.unpack(NTPPacket.packet,
                        packet[0:struct.calcsize(NTPPacket.packet)])
        except Exception as e:
            return (ERROR_CODE,str(e))   
        
        self.leap = unpacked_packet[0] >> 6 & 0x3
        self.version = unpacked_packet[0] >> 3 & 0x7
        self.mode = unpacked_packet[0] & 0x7
        self.stratum = unpacked_packet[1]

        self.ref_timestamp = unpacked_packet[7] + float(unpacked_packet[8])/2**32	

        self.origin_timestamp_int_byte = unpacked_packet[9]
        self.origin_timestamp_frac_byte = unpacked_packet[10]
        self.orig_timestamp = unpacked_packet[9] + float(unpacked_packet[10])/2**32

        self.recv_timestamp = unpacked_packet[11] + float(unpacked_packet[12])/2**32

        self.tx_timestamp_int_byte = unpacked_packet[13]
        self.tx_timestamp_frac_byte = unpacked_packet[14]
        self.tx_timestamp = unpacked_packet[13] + float(unpacked_packet[14])/2**32
        
    def packData(self):
        try:
            packet = struct.pack(NTPPacket.packet,
                (self.leap << 6 | self.version << 3 | self.mode),
                    self.stratum,
                    self.poll,
                    self.precision,
                    self.root_delay,
                    self.root_dispersion,
                    self.ref_id,
                    int(self.ref_timestamp),
                    int(abs(self.ref_timestamp - int(self.ref_timestamp)) * 2**32),
                    self.origin_timestamp_int_byte,
                    self.origin_timestamp_frac_byte,
                    int(self.recv_timestamp),
                    int(abs(self.recv_timestamp - int(self.recv_timestamp))* 2**32),
                    int(self.tx_timestamp),
                    int(abs(self.tx_timestamp - int(self.tx_timestamp))* 2**32))
            print(str(packet))
        except Exception as e:
            traceback.print_exc()
            return (ERROR_CODE,str(e))
        return packet