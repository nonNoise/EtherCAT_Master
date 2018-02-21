


send_mac=[0]*6
send_mac[0:6] = 0xff,0xff,0xff,0xff,0xff,0xff
receive_mac=[0]*6
receive_mac[0:6] = 0x01,0x01,0x01,0x01,0x01,0x01


cat_head =[0]*2
cat_head[0] = 0x88
cat_head[1] = 0xA4

cat_PDUfream = [0]*13
cat_PDUfream[0] = 0x08          # CMD (1 byte)
cat_PDUfream[1] = 0x01          # IDX (1 byte)
cat_PDUfream[2:4] = 0x00,0x00   # ADP (2 byte)
cat_PDUfream[4:6] = 0x01,0x03   # ADO (2 byte)
cat_PDUfream[6:8] = 0x01,0x00   # LEN (2 byte)
cat_PDUfream[8:10] = 0x00,0x00   # IRQ (2 byte)
cat_PDUfream[10] = 0x00         # DATA (1 byte)
cat_PDUfream[11:13] = 0x00,0x01 # WKC (2 byte)
print(len(cat_PDUfream))
cat_frame = [0]*2
cat_frame[0] = len(cat_PDUfream)
cat_frame[1] =  0x10 | ((0x700&len(cat_PDUfream))>>8)

cat_scoket=[]
cat_scoket.extend(send_mac)
cat_scoket.extend(receive_mac)
cat_scoket.extend(cat_head)
cat_scoket.extend(cat_frame)
cat_scoket.extend(cat_PDUfream)

#for i in range(len(cat_scoket)):
#    print ('[%d]: 0x{:02x}'.format(cat_scoket[i]) % (i))

import socket
import struct
IPaddr = "255.255.255.255"
Poat = 0x88A4
cat = socket.socket(socket.PF_PACKET,socket.SOCK_RAW)
#cat.setsockopt(socket.SOL_SOCKET, 25, "enp0s25"+'\0')
timeval = struct.pack('ll', 0, 1)
cat.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,timeval)
cat.setsockopt(socket.SOL_SOCKET,socket.SO_SNDTIMEO,timeval)
cat.setsockopt(socket.SOL_SOCKET, socket.SO_DONTROUTE, 1)
print(cat_scoket)
#cat.bind( ("0,0,0,0", Poat))
cat.bind(("enp0s25", 0x88A4))
cat.send(bytes(cat_scoket))
#print(bytes(cat_scoket))
#print(cat.recv(4096))