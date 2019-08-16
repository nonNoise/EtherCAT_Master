from pyEtherCAT import MasterEtherCAT
import time


#============================================================================#
# C95用の簡易EtherCATパッケージです。
# 本来は細かいパケットに付いて理解を深めた上で仕組みを構築していきますが、
# 説明も実験も追いつかず、ひとまずGPIOで高速にON/OFF出来る部分だけを纏めました。
# 動作は Linux(RaspberryPi含む) にて Python3　で動作します。
# sudo python3 test03.py
#============================================================================#
# ここから簡易ライブラリ
#============================================================================#
def EtherCAT_Init(ADP):
    cat = MasterEtherCAT.MasterEtherCAT("eth0")  #ネットワークカードのアドレスを記載
    #cat.EEPROM_SetUp(ADP) # EEPROMの設定、特に変更不要
    #cat.EEPROM_Stasus(enable=0x00,command=0x04) # EEPROMの設定、特に変更不要
    cat.ADP = ADP
    return cat
def EtherCAT_SetUp(cat):
    ADDR = 0x0120 # AL 制御レジスタ
    data = 0x0002 # 2h: 動作前ステートを要求する
    cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
    (DATA,WKC) = cat.socket_read()
    print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
    ADDR = 0x0120 # AL 制御レジスタ
    data = 0x0002 # 2h: 動作前ステートを要求する
    cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
    (DATA,WKC) = cat.socket_read()
    print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
    ADDR = 0x0120 # AL 制御レジスタ
    data = 0x0004 # 4h: 安全動作ステートを要求する
    cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
    (DATA,WKC) = cat.socket_read()
    print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
    ADDR = 0x0120 # AL 制御レジスタ
    data = 0x0008 # 8h: 動作ステートを要求する
    cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
    (DATA,WKC) = cat.socket_read()
    print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
def EtherCAT_GPIOMode(cat,data):
    ADDR = 0x0F00 # デジタル I/O 出力データレジスタ
    #data = 0x00FF # 出力データ
    cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
    (DATA,WKC) = cat.socket_read()
    print("[0x{:04x}]= 0x{:04x}".format(ADDR,DATA[0]|DATA[1]<<8))
def EtherCAT_GPIO_Out(cat,data):
    ADDR = 0x0F10
    cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
    (DATA,WKC) = cat.socket_read()
#============================================================================#
# ここまで　簡易ライブラリ
#============================================================================#



ADP = 0x0000 -1 # PCから1台目は０、２台目以降は-1していく
cat = EtherCAT_Init(ADP)    # EtherCATのネットワーク初期設定
ADDR = 0x0120 # AL 制御レジスタ
data = 0x0002 # 2h: 動作前ステートを要求する
cat.APWR(IDX=0x00,ADP=cat.ADP,ADO=ADDR,DATA=[data&0xFF,(data>>8)&0xFF])
exit()
EtherCAT_SetUp(cat)         # EtherCATスレーブの初期設定
EtherCAT_GPIOMode(cat,0xFFFF)         # EtherCATスレーブのGPIO方向設定　0:入力 1:出力

while 1:
    EtherCAT_GPIO_Out(cat,0xFFFF);
    EtherCAT_GPIO_Out(cat,0x0000);


    #for i in range(0xFFFF):
    #    EtherCAT_GPIO_Out(cat1,i);
