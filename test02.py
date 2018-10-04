import pyMasterEtherCAT
import time
cat = pyMasterEtherCAT.MasterEtherCAT("enp0s25")

ADP = 0x0000-1

def EEPROM_SetUp():
    cat.APWR(IDX=0x00,ADP=ADP,ADO=0x0500,DATA=[0x02])
    cat.socket_read()
    #time.sleep(0.1)
    cat.APWR(IDX=0x00,ADP=ADP,ADO=0x0500,DATA=[0x00])
    cat.socket_read()
    #time.sleep(0.1)
    
def EEPROM_Stasus(enable=0x00,command=0x00):
    d = command<<8 | enable
    cat.APWR(IDX=0x00,ADP=ADP,ADO=0x0502,DATA=[d&0xFF,(d>>8)&0xFF])
    #time.sleep(0.05)
    (DATA,WKC) = cat.socket_read()
    #time.sleep(0.05)
    while True:
        cat.APRD(IDX=0x00,ADP=ADP,ADO=0x0502,DATA=[0x00,0x00])
        #time.sleep(0.05)
        (DATA,WKC) = cat.socket_read()
        #time.sleep(0.05)
        #print("S= 0x{:04x}".format(DATA[0]|DATA[1]<<8))
        d = DATA[0]&0xFF | DATA[1]<<8
        if d&0x8000 == 0:
            break
    #time.sleep(0.1)
    return (DATA,WKC)
    
def EEPROM_AddrSet(addr=0x0000):
    cat.APWR(IDX=0x00,ADP=ADP,ADO=0x0504,DATA=[addr&0xFF,(addr>>8)&0xFF])
    #time.sleep(0.05)
    (DATA,WKC) = cat.socket_read()
    #time.sleep(0.05)
    return (DATA,WKC)
    
def EEPROM_Read():
    cat.APRD(IDX=0x00,ADP=ADP,ADO=0x0508,DATA=[0x00,0x00])
    #time.sleep(0.05)
    (DATA,WKC) = cat.socket_read()
    #time.sleep(0.05)
    return (DATA,WKC)

def EEPROM_Write(data):
    cat.APWR(IDX=0x00,ADP=ADP,ADO=0x0508,DATA=[data&0xFF,(data>>8)&0xFF])
    #time.sleep(0.05)
    (DATA,WKC) = cat.socket_read()
    #time.sleep(0.05)
    return (DATA,WKC)

def CatREAD(addr):
    ADDR = addr
    cat.APRD(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[0x00,0x00])
    (DATA,WKC) = cat.socket_read()
    return (DATA,WKC) 

cat.APRD(IDX=0x00,ADP=ADP,ADO=0x0E08,DATA=[0x00,0x00])
cat.socket_read()

#--- RUN LED  ---------
"""
cat.APWR(IDX=0x00,ADP=0x0000,ADO=0x0138,DATA=[0x1D,0x00])
cat.socket_read()
cat.APWR(IDX=0x00,ADP=0xFFFF,ADO=0x0138,DATA=[0x1D,0x00])
cat.socket_read()
cat.APWR(IDX=0x00,ADP=0xFFFE,ADO=0x0138,DATA=[0x1D,0x00])
cat.socket_read()
print("="*30)
"""
#--- EEPROM SetUp ---------
"""
EEPROM_SetUp()
for i in range(0x0080):
    EEPROM_AddrSet(i)
    EEPROM_Write(0)
    EEPROM_Stasus(enable=0x01,command=0x02)
    time.sleep(0.01)
d = [0x0180,0xFF00,0x0000,0x00FF,0x0000,0x0000,0x0000,0x0065]
#04 0F 00 44 10 27 F0 FF
#d = [0x0F04,0x4400,0x2710,0xFFFF,0x0000,0x0000,0x0000,0x0065]
for i in range(8):
    EEPROM_AddrSet(i)
    EEPROM_Write(d[i])
    EEPROM_Stasus(enable=0x01,command=0x02)
    time.sleep(0.01)
time.sleep(0.01)
EEPROM_AddrSet(0x0008)
EEPROM_Write(0x0A68)
EEPROM_Stasus(enable=0x01,command=0x02)
time.sleep(0.01)

for i in range(0x0080):
    EEPROM_AddrSet(i)
    EEPROM_Stasus(enable=0x00,command=0x01)
    (DATA,WKC) = EEPROM_Read()
    print("READ[0x{:04x}]= 0x{:04x}".format(i,DATA[0]|DATA[1]<<8))
"""

EEPROM_SetUp()
EEPROM_Stasus(enable=0x00,command=0x04)

ADDR = 0x0120
data = 0x0002
cat.APWR(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
(DATA,WKC) = cat.socket_read()
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))

ADDR = 0x0140
(DATA,WKC) = CatREAD(ADDR)
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
ADDR = 0x0150
(DATA,WKC) = CatREAD(ADDR)
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
ADDR = 0x0982
(DATA,WKC) = CatREAD(ADDR)
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
ADDR = 0x0152
(DATA,WKC) = CatREAD(ADDR)
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))


ADDR = 0x0120
data = 0x0002
cat.APWR(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
(DATA,WKC) = cat.socket_read()
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
ADDR = 0x0120
data = 0x0004
cat.APWR(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
(DATA,WKC) = cat.socket_read()
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
ADDR = 0x0120
data = 0x0008
cat.APWR(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
(DATA,WKC) = cat.socket_read()
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))

ADDR = 0x0120
(DATA,WKC) = CatREAD(ADDR)
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))

ADDR = 0x0F00
data = 0x00FF
cat.APWR(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
(DATA,WKC) = cat.socket_read()
print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))

while 1:
    for i in range(0xFFFF):
        ADDR = 0x0F10
        data = i#0x00FF
        try:
            cat.APWR(IDX=0x00,ADP=ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
        except BlockingIOError:
            pass
        #(DATA,WKC) = cat.socket_read()
        #print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
        #time.sleep(0.01)



(DATA,WKC) = CatREAD(0x0F00)
print("[0x{:04x}]= 0x{:04x}".format(0x0F00,DATA[0]|DATA[1]<<8))

print("-"*20)





"""
PDI Control 0x0000                          PDI Control レジスタの初期値 (0x140~0x141)
PDI Configuration 0x0001                    PDI Configuration レジスタの初期値 (0x150~0x151)
SyncImpulseLen 0x0002                       同期インパルス(10ns の倍数)
PDI Configuration2 0x0003                   PDI Configuration レジスタ R8 の初期値最上位ワード (0x152~0x153)
Configured Station Alias 0x0004             エイリアスアドレス
reserved 0x0005                              0 固定
Checksum 0x0007                             下位バイトには、多項式 x ^8+x+1 と初期値 0xFF を使った(ワード 0 からワード 6 の)CRC の計算結果
Vendor ID 0x0008                            CAN オブジェクト 0x1018、サブインデックス 1
Product Code 0x000A                         CAN オブジェクト 0x1018、サブインデックス 2
Revision Number 0x000C                      CAN オブジェクト 0x1018、サブインデックス 3
Serial Number 0x000E                        CAN オブジェクト 0x1018、サブインデックス 4
reserved 0x0013                              0 固定
Bootstrap Receive Mailbox Offset 0x0014     Bootstrap 状態の受信メールボックスのオフセット(マスタ⇒スレーブ)
Bootstrap Receive Mailbox Size 0x0015       Bootstrap 状態の受信メールボックスのサイズ(マスタ⇒スレーブ)
Bootstrap Send Mailbox Offset 0x0016        Bootstrap 状態の送信メールボックスのオフセット(スレーブ⇒マスタ)
Bootstrap Send Mailbox Size 0x0017          Bootstrap 状態の送信メールボックスのサイズ(スレーブ⇒マスタ)
Standard Receive Mailbox Offset 0x0018      標準状態の受信メールボックスのオフセット(マスタ⇒スレーブ)
Standard Receive Mailbox Size 0x0019        標準状態の受信メールボックスのサイズ(マスタ⇒スレーブ)
Standard Send Mailbox Offset 0x001A         標準状態の送信メールボックスのオフセット(スレーブ⇒マスタ)
Standard Send Mailbox Size 0x001B           標準状態の送信メールボックスのサイズ(スレーブ⇒マスタ)
Mailbox Protocol 0x001C                     表 18 に定義されている、サポートされるメールボックスプロトコル
reserved 0x002B                             0 固定
Size 0x002E                                 E2PROM のサイズ(Kbit-1)単位
Version 0x002F                              このバージョンは 1
"""