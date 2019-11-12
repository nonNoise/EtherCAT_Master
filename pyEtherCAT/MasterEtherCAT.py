import socket
import struct
import time


class MasterEtherCAT:
    def __init__(self, NickName):
        """
        :param str NickName:
        """
        ether_type = 0x88A4
        self.lowlevel = socket.socket(socket.PF_PACKET, socket.SOCK_RAW) # CAUTION: does not work on OSX
        timeval = struct.pack('ll', 0, 1)
        self.lowlevel.setsockopt(
            socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeval)
        self.lowlevel.setsockopt(
            socket.SOL_SOCKET, socket.SO_SNDTIMEO, timeval)
        self.lowlevel.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)
        self.lowlevel.settimeout(100)
        self.lowlevel.bind((NickName, ether_type))
        #----------------------------------------------------#
        self.send_mac = [0] * 6
        self.send_mac[0:6] = 0xff, 0xff, 0xff, 0xff, 0xff, 0xff
        self.receive_mac = [0] * 6
        self.receive_mac[0:6] = 0x01, 0x01, 0x01, 0x01, 0x01, 0x01
        #----------------------------------------------------#
        self.self_head = [0] * 2
        self.self_head[0] = 0x88
        self.self_head[1] = 0xA4
        #----------------------------------------------------#

    def socket_write(self, CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC):
        """
        :param int CMD: Command
        :param int IDX: Index
        :param int ADP: ADdress Position 16 bits (MSB half of 32bit)
        :param int ADO: ADdress Offset 16 bits (LSB half of 32 bit)
        :param int C:
        :param int NEXT:
        :param int IRQ:
        :param list DATA:
        :param int WKC: working counter
        """
        PDUframe = [0] * (len(DATA) + 13)
        PDUframe[0] = CMD               # CMD (1 byte)
        PDUframe[1] = IDX               # IDX (1 byte)
        PDUframe[2] = (ADP & 0xFF)        # ADP (2 byte)
        PDUframe[3] = (ADP & 0xFF00) >> 8
        PDUframe[4] = (ADO & 0xFF)        # ADO (2 byte)
        PDUframe[5] = (ADO & 0xFF00) >> 8
        PDUframe[6] = (len(DATA) & 0xFF)    # LEN (2 byte)
        PDUframe[7] = (len(DATA) & 0xFF00) >> 8
        PDUframe[8] = (IRQ & 0xFF)            # IRQ (2 byte)
        PDUframe[9] = (IRQ & 0x00FF)         # IRQ (2 byte)
        for i in range(len(DATA)):
            # print ('[{:d}]: 0x{:02x}'.format(i,self_PDUfream[i+10]))
            PDUframe[10 + i] = DATA[i]
        PDUframe[10 + len(DATA)] = (WKC & 0xFF)    # WKC (2 byte)
        PDUframe[11 + len(DATA)] = (WKC & 0xFF00) >> 8    # WKC (2 byte)
        #----------------------------------------------------#
        _frame = [0] * 2
        _frame[0] = len(PDUframe)
        _frame[1] = 0x10 | ((0x700 & len(PDUframe)) >> 8)
        _socket = []
        _socket.extend(self.send_mac)
        _socket.extend(self.receive_mac)
        _socket.extend(self.self_head)
        _socket.extend(_frame)
        _socket.extend(PDUframe)
        #----------------------------------------------------#
        # for i in range(len(self_scoket)):
        # print ('[%d]: 0x{:02x}'.format(self_scoket[i]) % (i))
        self.lowlevel.send(bytes(_socket))

    def socket_read(self):
        recv = self.lowlevel.recv(1023)
        PDUframe = [0]*len(recv)
        for i in range(len(recv)):
            if(i >= 16):
                #print ('[{:d}]: 0x{:02x}'.format(i-16,recv[i]))
                PDUframe[i-16] = recv[i]

        CMD = PDUframe[0]              # CMD (1 byte)
        IDX = PDUframe[1]              # IDX (1 byte)
        ADP = PDUframe[2] | (PDUframe[3] << 8)      # ADP (2 byte)
        ADO = PDUframe[4] | (PDUframe[5] << 8)    # ADO (2 byte)
        LEN = PDUframe[6] | (PDUframe[7] << 8)    # LEN (2 byte)
        IRQ = PDUframe[8] | (PDUframe[9] << 8)    # IRQ (2 byte)
        DATA = [0] * LEN
        for i in range(LEN):
            #print ('[{:d}]: 0x{:02x}'.format(i,self_PDUfream[10+i]))
            DATA[i] = PDUframe[10 + i]
        # WKC (2 byte)
        WKC = PDUframe[9 + LEN + 1] | (PDUframe[9 + LEN + 2] << 8)
        #frame = [0] * 2
        #frame[0] = len(PDUframe)
        #frame[1] = 0x10 | ((0x700 & len(PDUframe)) >> 8)
        # print("-"*30)
        # print("CMD= 0x{:02x}".format(CMD))
        # print("IDX= 0x{:02x}".format(IDX))
        # print("ADP= 0x{:04x}".format(ADP))
        # print("ADO= 0x{:04x}".format(ADO))
        # print("LEN= 0x{:04x}".format(LEN))
        # print("IRQ= 0x{:04x}".format(IRQ))
        # for i in range(LEN):
        #    print ('DATA[%d]: 0x{:02X}'.format(DATA[i]) % (i))
        # print("WKC= 0x{:04x}".format(WKC))
        return (DATA, WKC)

    def APRD(self, IDX, ADP, ADO, DATA):
        """ Auto increment physical read """
        CMD = 0x01  # APRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FPRD(self, IDX, ADP, ADO, DATA):
        """ Configured address physical read """
        CMD = 0x04  # FPRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def BRD(self, IDX, ADP, ADO, DATA):
        """ Broadcast read """
        CMD = 0x07  # BRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def LRD(self, IDX, ADP, ADO, DATA):
        """  Logical memory read """
        CMD = 0x0A  # LRD
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def APWR(self, IDX, ADP, ADO, DATA):
        """ Auto increment physical write """
        CMD = 0x02  # APWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FPWR(self, IDX, ADP, ADO, DATA):
        """ Configured address physical write """
        CMD = 0x05  # FPWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def BWR(self, IDX, ADP, ADO, DATA):
        """ Broadcast write """
        CMD = 0x08  # BWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def LWR(self, IDX, ADP, ADO, DATA):
        """ Logical memory write """
        CMD = 0x0B  # LWR
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def APRW(self, IDX, ADP, ADO, DATA):
        """ Auto increment physical read write """
        CMD = 0x03  # APRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FPRW(self, IDX, ADP, ADO, DATA):
        """ Configured address physical read write """
        CMD = 0x06  # FPRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def BRW(self, IDX, ADP, ADO, DATA):
        """ Broadcast read write """
        CMD = 0x09  # BRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def LRW(self, IDX, ADP, ADO, DATA):
        """ Logical memory read write """
        CMD = 0x0C  # LRW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def ARMW(self, IDX, ADP, ADO, DATA):
        """ Auto increment physical read multiple write """
        CMD = 0x0D  # ARMW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

    def FRMW(self, IDX, ADP, ADO, DATA):
        """ Configured address physical read multiple write """
        CMD = 0x0E  # FRMW
        C = 0
        NEXT = 0
        IRQ = 0x0000
        WKC = 0x0000
        self.socket_write(CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)

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
            # print("S= 0x{:04x}".format(DATA[0]|DATA[1]<<8))
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
