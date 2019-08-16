
import subprocess
class aseqdump:
    def __init__ (self,chanel):
        command = "aseqdump -p %s" % chanel
        self.p = subprocess.Popen(command.split(),stdout=subprocess.PIPE)
    def Note_get(self):
        data = self.p.stdout.readline().strip().split()
        print(data)
        if(data[1]==b"Note"):
            onoff = (data[2].decode("UTF-8").strip(','))
            key =(data[5].decode("UTF-8").strip(','))
            velocity =(data[7].decode("UTF-8").strip(','))
            return(onoff,key,velocity)
        else:
            return("","","")

    def Control_get(self):
        data = self.p.stdout.readline().strip().split()
        #print(data)
        if(data[1]==b"Control"):
            Ch = (data[3].decode("UTF-8").strip(',')) + "-" + (data[5].decode("UTF-8").strip(','))
            value =int(data[7].decode("UTF-8").strip(','))
            return(Ch,value)
        else:
            return("","")

    def Pitch_get(self):
        data = self.p.stdout.readline().strip().split()
        #print(data)
        if(data[1]==b"Pitch"):
            Ch = (data[3].decode("UTF-8").strip(','))
            value =int(data[5].decode("UTF-8").strip(','))
            return(Ch,value)
        else:
            return("","")
