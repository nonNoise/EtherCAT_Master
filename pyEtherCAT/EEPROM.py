from . import MasterEtherCAT_v2
import time


cat = MasterEtherCAT_v2("enp0s25")

ADP = 0x00000-2


def EEPROM_SetUp():
    cat.APWR(IDX=0x00, ADP=ADP, ADO=0x0500, DATA=[0x02])
    cat.socket_read()
    # time.sleep(0.1)
    cat.APWR(IDX=0x00, ADP=ADP, ADO=0x0500, DATA=[0x00])
    cat.socket_read()
    # time.sleep(0.1)


def EEPROM_Stasus(enable=0x00, command=0x00):
    d = command << 8 | enable
    cat.APWR(IDX=0x00, ADP=ADP, ADO=0x0502, DATA=[d & 0xFF, (d >> 8) & 0xFF])
    # time.sleep(0.05)
    (DATA, WKC) = cat.socket_read()
    # time.sleep(0.05)
    while True:
        cat.APRD(IDX=0x00, ADP=ADP, ADO=0x0502, DATA=[0x00, 0x00])
        # time.sleep(0.05)
        (DATA, WKC) = cat.socket_read()
        # time.sleep(0.05)
        #print("S= 0x{:04x}".format(DATA[0]|DATA[1]<<8))
        d = DATA[0] & 0xFF | DATA[1] << 8
        if d & 0x8000 == 0:
            break
    # time.sleep(0.1)
    return (DATA, WKC)


def EEPROM_AddrSet(addr=0x0000):
    cat.APWR(IDX=0x00, ADP=ADP, ADO=0x0504, DATA=[
             addr & 0xFF, (addr >> 8) & 0xFF])
    # time.sleep(0.05)
    (DATA, WKC) = cat.socket_read()
    # time.sleep(0.05)
    return (DATA, WKC)


def EEPROM_Read():
    cat.APRD(IDX=0x00, ADP=ADP, ADO=0x0508, DATA=[0x00, 0x00])
    # time.sleep(0.05)
    (DATA, WKC) = cat.socket_read()
    # time.sleep(0.05)
    return (DATA, WKC)


def EEPROM_Write(data):
    cat.APWR(IDX=0x00, ADP=ADP, ADO=0x0508, DATA=[
             data & 0xFF, (data >> 8) & 0xFF])
    # time.sleep(0.05)
    (DATA, WKC) = cat.socket_read()
    # time.sleep(0.05)
    return (DATA, WKC)


def CatREAD(addr):
    ADDR = addr
    cat.APRD(IDX=0x00, ADP=ADP, ADO=ADDR, DATA=[0x00, 0x00])
    (DATA, WKC) = cat.socket_read()
    return (DATA, WKC)


cat.APRD(IDX=0x00, ADP=ADP, ADO=0x0E08, DATA=[0x00, 0x00])
cat.socket_read()

# --- EEPROM SetUp ---------
EEPROM_SetUp()
for i in range(0x0080):
    EEPROM_AddrSet(i)
    EEPROM_Write(0)
    EEPROM_Stasus(enable=0x01, command=0x02)
    time.sleep(0.1)

time.sleep(0.1)
EEPROM_SetUp()
d = [0x0180, 0xFF00, 0x0000, 0x00FF, 0x0000, 0x0000, 0x0000, 0x0065]
# 04 0F 00 44 10 27 F0 FF
#d = [0x0F04,0x4400,0x2710,0xFFFF,0x0000,0x0000,0x0000,0x0065]
for i in range(8):
    EEPROM_AddrSet(i)
    EEPROM_Write(d[i])
    EEPROM_Stasus(enable=0x01, command=0x02)
    time.sleep(0.1)

EEPROM_AddrSet(0x0008)
EEPROM_Write(0x0A68)
EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.1)

for i in range(0x0080):
    EEPROM_AddrSet(i)
    EEPROM_Stasus(enable=0x00, command=0x01)
    (DATA, WKC) = EEPROM_Read()
    print("READ[0x{:04x}]= 0x{:04x}".format(i, DATA[0] | DATA[1] << 8))


cat.EEPROM_SetUp(0x0000)
cat.EEPROM_Stasus(enable=0x00, command=0x04)
