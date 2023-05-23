from machine import Pin,I2C
import network
import aioespnow
import uasyncio as asio
import ssd1306

# A WLAN interface must be active to send()/recv()
network.WLAN(network.STA_IF).active(True)

e = aioespnow.AIOESPNow()  # Returns AIOESPNow enhanced with async support
e.active(True)

i2c = I2C(0, sda=Pin(21), scl=Pin(22))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Received messages
async def resive(e,int_ms):
    while 1:
        async for mac, msg in e:
            oled.fill(0)
            oled.text(msg.decode("utf-8").split(' ')[0] , 10, 10)
            oled.text(msg.decode("utf-8").split(' ')[1] , 10, 20)
            oled.text(msg.decode("utf-8").split(' ')[2] , 10, 30)
            oled.show()
            await asio.sleep_ms(int_ms)
            

# define loop
loop = asio.get_event_loop()

#create looped tasks
loop.create_task(resive(e,50))
# loop run forever
loop.run_forever()