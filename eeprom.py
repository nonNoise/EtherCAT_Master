from pyEtherCAT import MasterEtherCAT
import time

cat = MasterEtherCAT.MasterEtherCAT("enp0s25")

# EEPROM Setup
cat.EEPROM_SetUp(0x0000)

# EEPROM ゼロクリア
for i in range(0x0080):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Write(0)
    cat.EEPROM_Stasus(enable=0x01,command=0x02)
    time.sleep(0.01)

# EEPROM データ書き込み
d = [0x0180,0xFF00,0x0000,0x00FF,0x0000,0x0000,0x0000,0x0065]
for i in range(8):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Write(d[i])
    cat.EEPROM_Stasus(enable=0x01,command=0x02)
    time.sleep(0.01)
time.sleep(0.01)

# EEPROM ベンダーID
cat.EEPROM_AddrSet(0x0008)
cat.EEPROM_Write(0x0A68)
#cat.EEPROM_Write(0x0000)

# EEPROM モード切替
cat.EEPROM_Stasus(enable=0x01,command=0x02)
time.sleep(0.01)

# EEPROM 読み出し
for i in range(0x0080):
    cat.EEPROM_AddrSet(i)
    cat.EEPROM_Stasus(enable=0x00,command=0x01)
    (DATA,WKC) = cat.EEPROM_Read()
    print("READ[0x{:04x}]= 0x{:04x}".format(i,DATA[0]|DATA[1]<<8))
