==================================================================
Python EtherCAT Master lib
==================================================================

What is Thise. これはなに？
-------------------------------------------------------------------

これはEtherCATを試すためのサンプルソースです。

EtherCATのマスタープログラムをPython3(Socket)で記述しています。

pyMasterEtherCAT



API 
-------------------------------------------------------------------

     |  APRD(self, IDX, ADP, ADO, DATA)
     |  
     |  APRW(self, IDX, ADP, ADO, DATA)
     |  
     |  APWR(self, IDX, ADP, ADO, DATA)
     |  
     |  ARMW(self, IDX, ADP, ADO, DATA)
     |  
     |  BRD(self, IDX, ADP, ADO, DATA)
     |  
     |  BRW(self, IDX, ADP, ADO, DATA)
     |  
     |  BWR(self, IDX, ADP, ADO, DATA)
     |  
     |  FPRD(self, IDX, ADP, ADO, DATA)
     |  
     |  FPRW(self, IDX, ADP, ADO, DATA)
     |  
     |  FPWR(self, IDX, ADP, ADO, DATA)
     |  
     |  FRMW(self, IDX, ADP, ADO, DATA)
     |  
     |  LRD(self, IDX, ADP, ADO, DATA)
     |  
     |  LRW(self, IDX, ADP, ADO, DATA)
     |  
     |  LWR(self, IDX, ADP, ADO, DATA)
     |  
     |  __init__(self, NicName)
     |  
     |  socket_read(self)
     |  
     |  socket_write(self, CMD, IDX, ADP, ADO, C, NEXT, IRQ, DATA, WKC)


