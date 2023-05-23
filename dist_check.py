from machine import Pin,I2C # возможность работать с I2C ротоколом  
from VL53L0X import * # работа с лазерным дальномером
from time import sleep_ms,sleep # задержки в мс и с
import uasyncio as asio # возможность асинхронн программирования

i2c_bus1 = I2C(1, sda=Pin(17), scl=Pin(16)) # вторая шина для дальномера
tof = VL53L0X(i2c_bus1) # объект, работающий с лазерным дальномером
alfa=0.8 # параметр для фильтра сглаживания дистанции
debug=1 # выводится ли отладочная информация
dist, dist_l = 0,0

def dist_det(): # определение расстояния
    while 1:
        global dist, dist_l
        tof.start()
        dist_l=dist # запомнили прошлую дистанцию
        dist=tof.read()-54 # получили новую + корректировка
        tof.stop()
        dist=int(alfa*dist+(1-alfa)*dist_l) # сглаживание и получение итоговой дистанции
        sleep(0.5)
        if debug:
            print('Dist: {}'.format(dist))
    
dist_det()