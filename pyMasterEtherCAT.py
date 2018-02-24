import socket
import struct

class MasterEtherCAT:
    def __init__(self,NickName):
        poat = 0x88A4
        self.cat = socket.socket(socket.PF_PACKET,socket.SOCK_RAW)
        timeval = struct.pack('ll', 0, 1)
        self.cat.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,timeval)
        self.cat.setsockopt(socket.SOL_SOCKET,socket.SO_SNDTIMEO,timeval)
        self.cat.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)
        self.cat.bind((NickName,poat))
        #----------------------------------------------------#
        self.send_mac=[0]*6
        self.send_mac[0:6] = 0xff,0xff,0xff,0xff,0xff,0xff
        self.receive_mac=[0]*6
        self.receive_mac[0:6] = 0x01,0x01,0x01,0x01,0x01,0x01
        #----------------------------------------------------#
        self.cat_head =[0]*2
        self.cat_head[0] = 0x88
        self.cat_head[1] = 0xA4
        #----------------------------------------------------#

    def socket_write(self,CMD,IDX,ADP,ADO,C,NEXT,IRQ,DATA,WKC):
        cat_PDUfream =[0]*(len(DATA)+13)
        cat_PDUfream[0] = CMD               # CMD (1 byte)
        cat_PDUfream[1] = IDX               # IDX (1 byte)
        cat_PDUfream[2] = (ADP&0xFF)        # ADP (2 byte)
        cat_PDUfream[3] = (ADP&0xFF00)>>8    
        cat_PDUfream[4] = (ADO&0xFF)        # ADO (2 byte)
        cat_PDUfream[5] = (ADO&0xFF00)>>8
        cat_PDUfream[6] = (len(DATA)&0xFF)    # LEN (2 byte)
        cat_PDUfream[7] = (len(DATA)&0xFF00)>>8      
        cat_PDUfream[8] = (IRQ&0xFF)            # IRQ (2 byte)
        cat_PDUfream[9] = (0x01&NEXT)<<16 | (0x01&C)<<15 | (IRQ&0x7F00)>>8            # IRQ (2 byte)
        for i in range(len(DATA)):
            #print ('[{:d}]: 0x{:02x}'.format(i,cat_PDUfream[i+10]))
            cat_PDUfream[10+i] = DATA[i]
        cat_PDUfream[10+len(DATA)] = (WKC&0xFF)    # WKC (2 byte)
        cat_PDUfream[11+len(DATA)] = (WKC&0xFF00)>>8    # WKC (2 byte)
        cat_frame = [0]*2
        cat_frame[0] = len(cat_PDUfream)
        cat_frame[1] =  0x10 | ((0x700&len(cat_PDUfream))>>8)
        #----------------------------------------------------#
        cat_scoket=[]
        cat_scoket.extend(self.send_mac)
        cat_scoket.extend(self.receive_mac)
        cat_scoket.extend(self.cat_head)
        cat_scoket.extend(cat_frame)
        cat_scoket.extend(cat_PDUfream)
        #----------------------------------------------------#
        #for i in range(len(cat_scoket)):
            #print ('[%d]: 0x{:02x}'.format(cat_scoket[i]) % (i))
        self.cat.send(bytes(cat_scoket))
    def socket_read(self):
        recv = self.cat.recv(1024)
        cat_PDUfream=[0]*len(recv)
        for i in range(len(recv)):
            if(i>=16):
                #print ('[{:d}]: 0x{:02x}'.format(i-16,recv[i]))
                cat_PDUfream[i-16] = recv[i]
                
        CMD = cat_PDUfream[0]              # CMD (1 byte)
        IDX = cat_PDUfream[1]              # IDX (1 byte)
        ADP = cat_PDUfream[2] | (cat_PDUfream[3]<<8)      # ADP (2 byte)
        ADO = cat_PDUfream[4] | (cat_PDUfream[5]<<8)    # ADO (2 byte)
        LEN = cat_PDUfream[6] | (cat_PDUfream[7]<<8)    # LEN (2 byte)
        IRQ = cat_PDUfream[8] | (cat_PDUfream[9]<<8)    # IRQ (2 byte)
        DATA = [0] * LEN
        for i in range(LEN):
            #print ('[{:d}]: 0x{:02x}'.format(i,cat_PDUfream[10+i]))
            DATA[i] = cat_PDUfream[10+i]
        WKC = cat_PDUfream[9+LEN+1] | (cat_PDUfream[9+LEN+2]<<8)    # WKC (2 byte)
        cat_frame = [0]*2
        cat_frame[0] = len(cat_PDUfream)
        cat_frame[1] =  0x10 | ((0x700&len(cat_PDUfream))>>8)
        print("CMD= 0x{:02x}".format(CMD))
        print("IDX= 0x{:02x}".format(IDX))
        print("ADP= 0x{:04x}".format(ADP))
        print("ADO= 0x{:04x}".format(ADO))
        print("LEN= 0x{:04x}".format(LEN))
        print("IRQ= 0x{:04x}".format(IRQ))
        for i in range(LEN):
            print ('DATA[%d]: 0x{:02X}'.format(DATA[i]) % (i))
        print("WKC= 0x{:04x}".format(WKC))
        
    def APRD(self,IDX,ADP,ADO,DATA):
        CMD = 0x01  # APRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD,IDX,ADP,ADO,C,NEXT,IRQ,DATA,WKC)
    def BWR(self,IDX,ADP,ADO,DATA):
        CMD = 0x08  # APRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD,IDX,ADP,ADO,C,NEXT,IRQ,DATA,WKC)

    