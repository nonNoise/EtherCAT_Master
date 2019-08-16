

import aseqdump
import threading

data = 0
Ch =0
def Note():
    midi = aseqdump.aseqdump("24:0")
    while 1:
        onoff,key,velocity = midi.Note_get()
        if(onoff == ""):
            continue
        print("Note: %s , %s , %s" % (onoff,key,velocity))

def Control():
    global Ch
    midi = aseqdump.aseqdump("24:2")
    while 1:
        Ch,value = midi.Control_get()
        if(Ch == ""):
            continue
        print("Control: %s , %s" % (Ch,value))

def Pitch():
    midi = aseqdump.aseqdump("24:1")
    while 1:
        Ch,value = midi.Pitch_get()
        if(Ch == ""):
            continue
        print("Pitch: %s , %s" % (Ch,value))


thread_1 = threading.Thread(target=Note)
thread_1.start()
"""
thread_2 = threading.Thread(target=Control)
thread_2.start()

thread_3 = threading.Thread(target=Pitch)
thread_3.start()
"""
while 1:
    pass
    #print("0x%04X" % data)

#midi2 = aseqdump.aseqdump("24:2")

    #Ch,value = midi2.Control_get()
    #print("Control2: %s , %s " % (Ch,value))
    

