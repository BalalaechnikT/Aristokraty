from machine import Pin,I2C # возможность работать с I2C ротоколом
from neopixel import NeoPixel # работа с адресными светодиодами
from MX1508 import * # драйверы двигателя
from VL53L0X import * # работа с лазерным дальномером
from tcs34725 import * # работа с датчиком цвета
from time import sleep_ms,sleep # задержки в мс и с
import uasyncio as asio # возможность асинхронн программирования
import aioespnow # асинхронный ESP-now
import network # функции работы по wi-fi

i2c_bus = I2C(0, sda=Pin(21), scl=Pin(22)) # создание шины под датчик цвета
tcs = TCS34725(i2c_bus)
NUM_OF_LED = 2
np = NeoPixel(Pin(27), NUM_OF_LED)
tcs.gain(4)#gain must be 1, 4, 16 or 60 (значение усиления)
tcs.integration_time(80) # время накопления данных и решения по цвету
Lt=60 # интенсивность цветов
color=['Red','Yellow','White','Green','Black','Cyan','Blue','Magenta'] # набор обрабатываемых цветов
color_id=[(Lt,0,0),(Lt,Lt,0),(Lt,Lt,Lt),(0,Lt,0),(0,0,0),(0,Lt,Lt),(0,0,Lt),(Lt,0,Lt)] # раскраски цветов
debug=1 # выводится ли отладочная информация

col_id,col_id_l,di=0,0,0 

def color_det():
    while 1:
        sleep(1)
        global col_id,col_id_l,debug
        rgb=tcs.read(1)
        r,g,b=rgb[0],rgb[1],rgb[2]
        h,s,v=rgb_to_hsv(r,g,b)
        if 320<h<360:
            col_id_l=col_id
            col_id=0
        elif 61<h<120:
            col_id_l=col_id
            col_id=1
        elif 121<h<180:
            if v>100:
                col_id_l=col_id
                col_id=2
            elif 70<v<100:
                col_id_l=col_id
                col_id=3
            elif v<70:
                col_id_l=col_id
                col_id=4
        elif 181<h<300:
            if v>100:
                col_id_l=col_id
                col_id=5
            else:
                col_id_l=col_id
                col_id=6
        elif 300<h<320:
            col_id_l=col_id
            col_id=7 
        if debug:
            print('Color is {}. R:{} G:{} B:{} H:{:.0f} S:{:.0f} V:{:.0f}'.format(color[col_id],r,g,b,h,s,v))
        LED_cont(col_id)

    
def LED_cont(i):
    for npixel in range(NUM_OF_LED):
        np[npixel] = color_id[i]
        np.write()
        sleep(1)
color_det()
              
