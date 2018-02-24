import pyMasterEtherCAT

cat = pyMasterEtherCAT.MasterEtherCAT("enp0s25")

DATA =[0]*1
DATA[0] = 0x01

#cat.APRD(IDX=0x01,ADP=0x0000,ADO=0xffff,DATA=DATA)
cat.FPRD(IDX=0x02,ADP=0x0000,ADO=0x0008,DATA=DATA)
#cat.socket_write(0x08,0x01,0x0000,0x0103,0,0,0x0000,DATA,0xFFFF)
cat.socket_read()
