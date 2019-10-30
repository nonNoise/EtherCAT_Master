import socket
import struct
import time


class MasterEtherCAT_v2:

    def __init__(self, NickName):
        poat = 0x88A4
        self.self = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
        timeval = struct.pack('ll', 0, 1)
        self.self.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        self.self.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
        self.self.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)
        self.self.settimeout(100)
        self.self.bind((NickName, poat))

    def build_socket(self, CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC):
        pduflame = [0] * (len(DATA) + 13)
        pduflame[0] = CMD               # CMD (1 byte)
        pduflame[1] = IDX               # IDX (1 byte)
        pduflame[2] = (ADP & 0xFF)        # ADP (2 byte)
        pduflame[3] = (ADP & 0xFF00) >> 8
        pduflame[4] = (ADO & 0xFF)        # ADO (2 byte)
        pduflame[5] = (ADO & 0xFF00) >> 8
        pduflame[6] = (len(DATA) & 0xFF)    # LEN (2 byte)
        pduflame[7] = (len(DATA) & 0xFF00) >> 8
        pduflame[8] = (IRQ & 0xFF)            # IRQ (2 byte)
        pduflame[9] = (0x01 & NEXT) << 16 | (0x01 & C) << 15 | (
            IRQ & 0x7F00) >> 8            # IRQ (2 byte)
        for i in range(len(DATA)):
            #print ('[{:d}]: 0x{:02x}'.format(i,pduflame[i+10]))
            pduflame[10 + i] = DATA[i]
        pduflame[10 + len(DATA)] = (WKC & 0xFF)    # WKC (2 byte)
        pduflame[11 + len(DATA)] = (WKC & 0xFF00) >> 8    # WKC (2 byte)
        # for i in range(len(scoket)):
        #print ('[%d]: 0x{:02x}'.format(scoket[i]) % (i))
        return pduflame

    def socket_write(self, pduflame):
        #----------------------------------------------------#
        send_mac = [0] * 6
        send_mac[0:6] = 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        receive_mac = [0] * 6
        receive_mac[0:6] = 0x01, 0x01, 0x01, 0x01, 0x01, 0x01
        self_head = [0] * 2
        self_head[0] = 0x88
        self_head[1] = 0xA4
        #----------------------------------------------------#
        frame = [0] * 2
        frame[0] = len(pduflame)
        frame[1] = 0x10 | ((0x700 & len(pduflame)) >> 8)
        #----------------------------------------------------#
        scoket = []
        scoket.extend(send_mac)
        scoket.extend(receive_mac)
        scoket.extend(self_head)
        scoket.extend(frame)
        scoket.extend(pduflame)
        #----------------------------------------------------#
        self.self.send(bytes(self_scoket))

    def socket_read(self):
        # time.sleep(0.1)
        recv = self.self.recv(1023)
        pduflame = [0] * len(recv)
        for i in range(len(recv)):
            if(i >= 16):
                #print ('[{:d}]: 0x{:02x}'.format(i-16,recv[i]))
                pduflame[i - 16] = recv[i]
        offset = 0
        cnt = 0
        buff = []
        while 1:
            if(i > offset):
                CMD = pduflame[0 + offset]              # CMD (1 byte)
                IDX = pduflame[1 + offset]              # IDX (1 byte)
                # ADP (2 byte)
                ADP = pduflame[2 + offset] | (pduflame[3 + offset] << 8)
                # ADO (2 byte)
                ADO = pduflame[4 + offset] | (pduflame[5 + offset] << 8)
                # LEN (2 byte)
                LEN = pduflame[6 + offset] | (pduflame[7 + offset] << 8)
                # IRQ (2 byte)
                IRQ = pduflame[8 + offset] | (pduflame[9 + offset] << 8)
                DATA = [0] * LEN
                for i in range(LEN):
                    #print ('[{:d}]: 0x{:02x}'.format(i,pduflame[10+i]))
                    DATA[i] = pduflame[10 + offset + i]
                # WKC (2 byte)
                WKC = pduflame[9 + offset + LEN +
                               1] | (pduflame[9 + offset + LEN + 2] << 8)
                buff.append({CMD, IDX, ADP, ADO, LEN, IRQ, DATA, WKC})
                cnt = cnt + 1
                offset = 9 + LEN + 2
            else:
                break
        # print("-"*30)
        #print("CMD= 0x{:02x}".format(CMD))
        #print("IDX= 0x{:02x}".format(IDX))
        #print("ADP= 0x{:04x}".format(ADP))
        #print("ADO= 0x{:04x}".format(ADO))
        #print("LEN= 0x{:04x}".format(LEN))
        #print("IRQ= 0x{:04x}".format(IRQ))
        # for i in range(LEN):
        #    print ('DATA[%d]: 0x{:02X}'.format(DATA[i]) % (i))
        #print("WKC= 0x{:04x}".format(WKC))
        return buff

    def APRD(self, IDX, ADP, ADO, DATA):
        CMD = 0x01  # APRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FPRD(self, IDX, ADP, ADO, DATA):
        CMD = 0x04  # FPRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def BRD(self, IDX, ADP, ADO, DATA):
        CMD = 0x07  # BRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def LRD(self, IDX, ADP, ADO, DATA):
        CMD = 0x0A  # LRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def APWR(self, IDX, ADP, ADO, DATA):
        CMD = 0x02  # APWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FPWR(self, IDX, ADP, ADO, DATA):
        CMD = 0x05  # FPWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def BWR(self, IDX, ADP, ADO, DATA):
        CMD = 0x08  # BWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def LWR(self, IDX, ADP, ADO, DATA):
        CMD = 0x0B  # LWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def APRW(self, IDX, ADP, ADO, DATA):
        CMD = 0x03  # APRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FPRW(self, IDX, ADP, ADO, DATA):
        CMD = 0x06  # FPRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def BRW(self, IDX, ADP, ADO, DATA):
        CMD = 0x09  # BRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def LRW(self, IDX, ADP, ADO, DATA):
        CMD = 0x0C  # LRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def ARMW(self, IDX, ADP, ADO, DATA):
        CMD = 0x0D  # ARMW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FRMW(self, IDX, ADP, ADO, DATA):
        CMD = 0x0E  # FRMW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        return self.build_socket(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def EEPROM_SetUp(self, ADP):
        self.ADP = ADP
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=0x0500, DATA=[0x02])
        self.socket_read()
        # time.sleep(0.1)
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=0x0500, DATA=[0x00])
        self.socket_read()
        # time.sleep(0.1)

    def EEPROM_Stasus(self, enable=0x00, command=0x00):
        d = command << 8 | enable
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=0x0502,
                  DATA=[d & 0xFF, (d >> 8) & 0xFF])
        # time.sleep(0.05)
        (DATA, WKC) = self.socket_read()
        # time.sleep(0.05)
        while True:
            self.APRD(IDX=0x00, ADP=self.ADP, ADO=0x0502, DATA=[0x00, 0x00])
            # time.sleep(0.05)
            (DATA, WKC) = self.socket_read()
            # time.sleep(0.05)
            #print("S= 0x{:04x}".format(DATA[0]|DATA[1]<<8))
            d = DATA[0] & 0xFF | DATA[1] << 8
            if d & 0x8000 == 0:
                break
        # time.sleep(0.1)
        return (DATA, WKC)

    def EEPROM_AddrSet(self, addr=0x0000):
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=0x0504,
                  DATA=[addr & 0xFF, (addr >> 8) & 0xFF])
        # time.sleep(0.05)
        (DATA, WKC) = self.socket_read()
        # time.sleep(0.05)
        return (DATA, WKC)

    def EEPROM_Read(self):
        self.APRD(IDX=0x00, ADP=self.ADP, ADO=0x0508, DATA=[0x00, 0x00])
        # time.sleep(0.05)
        (DATA, WKC) = self.socket_read()
        # time.sleep(0.05)
        return (DATA, WKC)

    def EEPROM_Write(self, data):
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=0x0508,
                  DATA=[data & 0xFF, (data >> 8) & 0xFF])
        # time.sleep(0.05)
        (DATA, WKC) = self.socket_read()
        # time.sleep(0.05)
        return (DATA, WKC)

    def EthereCAT_Reset(self):
        ADDR = 0x0041  # Reset レジスタ
        data = 0x0052  # 'R'
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=ADDR,
                  DATA=[data & 0xFF, (data >> 8) & 0xFF])
        (DATA, WKC) = self.socket_read()
        ADDR = 0x0041  # Reset レジスタ
        data = 0x0045  # 'E'
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=ADDR,
                  DATA=[data & 0xFF, (data >> 8) & 0xFF])
        (DATA, WKC) = self.socket_read()
        ADDR = 0x0041  # Reset レジスタ
        data = 0x0053  # 'S'
        self.APWR(IDX=0x00, ADP=self.ADP, ADO=ADDR,
                  DATA=[data & 0xFF, (data >> 8) & 0xFF])
        (DATA, WKC) = self.socket_read()
        return (DATA, WKC)
