import gevent.monkey
gevent.monkey.patch_socket()
from pyEtherCAT import MasterEtherCAT
import time
import os
import psutil



#============================================================================#
# C95用の簡易EtherCATパッケージです。
# 本来は細かいパケットに付いて理解を深めた上で仕組みを構築していきますが、
# 説明も実験も追いつかず、ひとまずGPIOで高速にON/OFF出来る部分だけを纏めました。
# 動作は Linux(RaspberryPi含む) にて Python3　で動作します。
# sudo python3 test03.py
#============================================================================#
# ここから簡易ライブラリ
#============================================================================#
def EtherCAT_Init():
    cat = MasterEtherCAT.MasterEtherCAT("enp0s25")  #ネットワークカードのアドレスを記載
    
    return cat
def EtherCAT_SetUp(cat):
    cat.EEPROM_SetUp(cat.ADP) # EEPROMの設定、特に変更不要
    cat.EEPROM_Stasus(enable=0x00,command=0x04) # EEPROMの設定、特に変更不要
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
    #(DATA,WKC) = cat.socket_read()
#============================================================================#
# ここまで　簡易ライブラリ
#============================================================================#



cat = EtherCAT_Init()    # EtherCATのネットワーク初期設定

#-- EtherCATのステートマシンを実行に移す処理
cat.ADP = 0x0000  # PCから1台目は０、２台目以降は-1していく
EtherCAT_SetUp(cat)         # EtherCATスレーブの初期設定
EtherCAT_GPIOMode(cat,0xFFFF)         # EtherCATスレーブのGPIO方向設定　0:入力 1:出力

#-- EtherCATのステートマシンを実行に移す処理
cat.ADP = 0x0000 -1  #例　これは2台目　繋がってなければ必要ない
EtherCAT_SetUp(cat)         # EtherCATスレーブの初期設定
EtherCAT_GPIOMode(cat,0xFFFF)         # EtherCATスレーブのGPIO方向設定　0:入力 1:出力

#-- EtherCATのステートマシンを実行に移す処理
cat.ADP = 0x0000 -2  #例　これは3台目 繋がってなければ必要ない
EtherCAT_SetUp(cat)         # EtherCATスレーブの初期設定
EtherCAT_GPIOMode(cat,0xFFFF)         # EtherCATスレーブのGPIO方向設定　0:入力 1:出力

#-- 1台目のLEDをシフトする
cat.ADP = 0x0000

#IME = 0.0005
#step = [0x01,0x09,0x04,0x05,0x02,0x06,0x08,0x0A]
#step = [0x09,0x05,0x06,0x0A]
TIME = 0.0015
step = [0x01<<0,0x04<<0,0x02<<0,0x08<<0]
try:
    while 1:
        #time.sleep(TIME)
        
        for n in range(360-1):
            for i in range(len(step)):
                EtherCAT_GPIO_Out(cat,step[i]);
                time.sleep(TIME)
        #EtherCAT_GPIO_Out(cat,0x0000);
        time.sleep(2)
        
        for n in range(360-1):
            for i in range(len(step)):
                EtherCAT_GPIO_Out(cat,step[len(step)-1-i]);
                time.sleep(TIME)
        #EtherCAT_GPIO_Out(cat,0x0000);
        time.sleep(2)
except KeyboardInterrupt:
    EtherCAT_GPIO_Out(cat,0x0000);
    print("")
    print("End.")