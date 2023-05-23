from machine import Pin ,I2C
from neopixel import NeoPixel
from VL53L0X import *
from tcs34725 import *
from time import sleep_ms

i2c_bus = I2C(0, sda=Pin(16), scl=Pin(17))
tcs = TCS34725(i2c_bus)
tcs.gain(4)#gain must be 1, 4, 16 or 60
tcs.integration_time(80)
i2c_bus1 = I2C(1, sda=Pin(21), scl=Pin(22))
tof = VL53L0X(i2c_bus1)
NUM_OF_LED = 3
np = NeoPixel(Pin(13), NUM_OF_LED)
np[0]=(0,0,0)
bk=1
Lt=100
while True:
    r,g,b=tcs.read(1)[0],tcs.read(1)[1],tcs.read(1)[2]
    h,s,v=rgb_to_hsv(r,g,b)
    if 0<h<60:
        #print('Red')
        np[0]=(Lt,0,0)
    elif 61<h<120:
        #print('Yellow')
        np[0]=(Lt,Lt,0)
    elif 121<h<180:
        if v>100:
            #print('White')
            np[0]=(Lt,Lt,Lt)
        elif 25<v<100:
            #print('Green')
            np[0]=(0,Lt,0)
        elif v<25:
            #print('Black')
            if bk==0:
                np[0]=(0,0,0)
                bk=1
            else:
                np[0]=(Lt,0,0)
                bk=0
    elif 181<h<240:
        if v>40:
            #print('Cyan')
            np[0]=(0,Lt,Lt)
        else:
            #print('Blue')
            np[0]=(0,0,Lt) 
    elif 241<h<360:
        #print('Magenta')
        np[0]=(Lt,0,Lt)      
    #print('R:',r,'G:',g,'B:',b,'H:',int(h),'S:',int(s),'V:',int(v))
    tof.start()
    d=tof.read()
    tof.stop()
    if 150<d<250:
        np[1]=(Lt,Lt,0)
    elif d<150:
        np[1]=(Lt,0,0)
    else:
        np[1]=(0,Lt,0)
    np.write()
    #sleep_ms(100)    
