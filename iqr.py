from machine import Pin,I2C # возможность работать с I2C ротоколом
from neopixel import NeoPixel # работа с адресными светодиодами
from MX1508 import * # драйверы двигателя
from VL53L0X import * # работа с лазерным дальномером
from tcs34725 import * # работа с датчиком цвета
from time import sleep_ms,sleep # задержки в мс и с
import uasyncio as asio # возможность асинхронн программирования
import aioespnow # асинхронный ESP-now
import network # функции работы по wi-fi
R_W_count,W_count,col_id,col_id_l,direct,di,dist,busy,busy_col,col_sel=0,0,0,0,0,0,500,0,0,5 # инициализация глобальных переменных
L_W_count = 0
L_last_count,R_last_count = [0,0],[0,0] # разница между предыдущем количество оборотов и нынешним
R_m_pin = Pin(32, Pin.IN) # пины энкодеров для использования в прерываниях
L_m_pin = Pin(25, Pin.IN)

def R_W_int(pin): # функции счета срабатываний энкодера
    global W_count,R_W_count,R_last_count
    W_count+=1
    R_W_count+=1
    R_last_count[0] = R_last_count[1]
    R_last_count[1] = R_W_count
    
    
    
def L_W_int(pin):
    global W_count,L_W_count,L_last_count
    W_count+=1
    L_W_count+=1
    L_last_count[0] = L_last_count[1]
    L_last_count[1] = L_W_count
    
    
R_m_pin.irq(trigger=Pin.IRQ_FALLING |Pin.IRQ_RISING , handler=R_W_int) #t rigger=Pin.IRQ_FALLING | - при поступлении высокого/низкого потенциала на пин энкодера вызываем функции счета
L_m_pin.irq(trigger=Pin.IRQ_FALLING |Pin.IRQ_RISING , handler=L_W_int)

while 1:
    print('W_count = {}\nR_W_count = {}\nL_W_count = {}'. format(W_count, R_last_count[1]-R_last_count[0], L_last_count[1]-L_last_count[0]))
    sleep(2)