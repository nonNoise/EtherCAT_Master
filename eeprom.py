from pyEtherCAT import MasterEtherCAT
import time
import os
import psutil


def CRC(data):
    crc = 0xFF
    for i in range(len(data)):
        crc ^= data[i]
        for j in range(8):
            if(crc & 0x80):
                crc = (crc << 1) ^ 0x07
            else:
                crc = (crc << 1)
    return (0xFF & crc)


cat = MasterEtherCAT.MasterEtherCAT("enp0s25")
cat.ADP = 0x000000

"""
cat.APRD(IDX=0x00,ADP=cat.ADP,ADO=0x0502,DATA=[0x00,0x00])
time.sleep(0.05)
(DATA,WKC) = cat.socket_read()
print(DATA)
print('DATA:{:04x}'.format(DATA[0] | DATA[1]<<8))
"""

# EEPROM Setup
print("EEPROM Setup")
cat.EEPROM_SetUp(0x0000)

# EEPROM ゼロクリア
print("EEPROM Zero Clear")
for i in range(0x010):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Write(0)
    cat.EEPROM_Stasus(enable=0x01, command=0x02)
    time.sleep(0.01)

"""
# EEPROM データ書き込み
#800E00CC8813f000000000800000
print("EEPROM Deta Write")
d = [0x0180,0xFF00,0x0000,0x00FF,0x0000,0x0000,0x0000,0x0065]
for i in range(8):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Write(d[i])
    cat.EEPROM_Stasus(enable=0x01,command=0x02)
    time.sleep(0.01)
time.sleep(0.01)
"""
# EEPROM データ書き込み
# 800100FF0000FF

print("EEPROM Deta Write")
d = [0x80, 0x01, 0x00, 0xFF, 0x00, 0x00, 0xFF,
     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
# d = [0x80, 0x00, 0x00, 0xCC, 0x88, 0x13, 0xf0,
#      0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00]
buf = [d[0] | d[1] << 8, d[2] | d[3] << 8, d[4] | d[5] << 8, d[6] |
       d[7] << 8, d[8] | d[9] << 8, d[10] | d[11] << 8, d[12] | d[13] << 8]
for i in range(7):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Write(buf[i])
    cat.EEPROM_Stasus(enable=0x01, command=0x02)
    time.sleep(0.01)
crc = CRC(d)
cat.EEPROM_AddrSet(7)
cat.EEPROM_Write(crc)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
print('CRC:{:04x}'.format(crc))


# ベンダーID [0x00000A68]
cat.EEPROM_AddrSet(0x0008)
cat.EEPROM_Write(0x0A68)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
cat.EEPROM_AddrSet(0x0009)
cat.EEPROM_Write(0x0000)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
# プロダクト コード [0x00000001]
cat.EEPROM_AddrSet(0x000A)
cat.EEPROM_Write(0x0001)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
cat.EEPROM_AddrSet(0x000B)
cat.EEPROM_Write(0x0000)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
# リビジョン ナンバー [0x00000001]
cat.EEPROM_AddrSet(0x000C)
cat.EEPROM_Write(0x0001)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
cat.EEPROM_AddrSet(0x000D)
cat.EEPROM_Write(0x0000)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
# シリアル ナンバー [0x00000001]
cat.EEPROM_AddrSet(0x000E)
cat.EEPROM_Write(0x0001)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)
cat.EEPROM_AddrSet(0x000F)
cat.EEPROM_Write(0x0000)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)


# シリアル ナンバー [0x00000001]
cat.EEPROM_AddrSet(0x003E)
cat.EEPROM_Write(0x0001)
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)


"""
Category_Header = 30
Category_Data = 0x0001
Category_Size


cat.EEPROM_AddrSet(0x0040)
cat.EEPROM_Write(0x0000)
cat.EEPROM_AddrSet(0x0041)
cat.EEPROM_Write(0x0000)
cat.EEPROM_AddrSet(0x0042)
cat.EEPROM_Write(0x0000)

"""


# EEPROM モード切替
cat.EEPROM_Stasus(enable=0x01, command=0x02)
time.sleep(0.01)


# EEPROM 読み出し
for i in range(0x0010):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Stasus(enable=0x00, command=0x01)
    (DATA, WKC) = cat.EEPROM_Read()
    print("READ[0x{:04x}]= 0x{:04x}".format(i, DATA[0] | DATA[1] << 8))


cat.EthereCAT_Reset()
time.sleep(1)

cat.ADP = 0x0000
cat.APRD(IDX=0x00, ADP=cat.ADP, ADO=0x0502, DATA=[0x00, 0x00])
time.sleep(0.05)
(DATA, WKC) = cat.socket_read()
print(DATA)
print('DATA:{:04x}'.format(DATA[0] | DATA[1] << 8))
