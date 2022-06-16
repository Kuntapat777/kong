from machine import Pin,PWM,I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd,
import utime
from machine import UART, Pin
from NetworkHelper import NetworkHelper
import time, sys

MQ2 = machine.ADC(26)
buzzer = PWM(Pin(18))
led_Red = Pin(14,Pin.OUT)
led_Yellow = Pin(15,Pin.OUT)
pump = Pin(10, Pin.OUT)


I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

def wifi():
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print("RPi-Pico MicroPython Ver:", sys.version)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    esp8266_at_ver = None
    print("StartUP", con.startUP())
    # print("ReStart",con.reStart())
    print("StartUP", con.startUP())
    print("Echo-Off", con.echoING())
    print("\r\n\r\n")
    esp8266_at_ver = con.getVersion()
    if esp8266_at_ver != None:
        print(esp8266_at_ver)
    con.setCurrentWiFiMode()
    print("\r\n\r\n")
    """
    Connect with the WiFi
    """
    ssid = "KNOWD" #wifi name
    pwd = "12345678" # password
    print("Try to connect with the WiFi..")
    timeout = 0
    # default delay wifi delay 5 sec
    while timeout < 6:
        if "WIFI CONNECTED" in con.connectWiFi(ssid, pwd,delay=1):
            print("ESP8266 connect with the WiFi..")
            return True
            break
        else:
            print(".")
            timeout += 1
            time.sleep(0.5)
    if timeout >= 6:
        print("Timeout connect with the WiFi")
        return False
    
def getApi(host, path, param=""):
    print("\r\n\r\n")
    print("Now it's time to start HTTP Get/Post Operation.......\r\n")
    # host = "192.168.1.2"  # host
    # path = "/"  # path  ?? url
    #param = ""
    if param != "":
        path = path + "?" + param
    else:
        path = path
    timeout = 0
    # default delay get api delay 3 sec
    while timeout < 3:
        httpCode, httpRes = con.doHttpGet(host, path,delay=0)
        print(
            "-----------------------------------------------------------------------------"
        )
        print("HTTP Code:", httpCode)
        print("HTTP Response:", httpRes)
        print(
            "-----------------------------------------------------------------------------\r\n"
        )
        if httpCode == 200:
            print("Get data successful..\r\n")
            return httpRes
            break
        else:
            print("Error")
            print("Get data fail...")
            print("Please wait to try again....\r\n")
            timeout += 1
            time.sleep(0.5)
        if timeout >= 3:
            return False
    
def gas():
    smoke_value = MQ2.read_u16()
    utime.sleep(1)
    return smoke_value
        

def sound_on():
    buzzer.duty_u16(10000)
 
   
def sound_off():
    buzzer.duty_u16(0)


def pump_on():
    pump.value(0)
    
  
    
def pump_off():
    pump.value(1)
   

def lcd1_on():
        lcd.move_to(4,0)
        lcd.putstr("Have SOMKE")
        lcd.blink_cursor_off
        lcd.blink_cursor_on()
        lcd.clear
        
def lcd2_off():
        lcd.move_to(4,0)
        lcd.putstr("Not  SMOKE")
        lcd.blink_cursor_off()
        lcd.blink_cursor_on()
        lcd.clear
        

con = NetworkHelper()
wifiCon = wifi()

host = "192.168.148.88"
#path = "/update_value_hw"
#param = ""

conversion_factor =3.3/(65535)
while wifiCon:
    value = gas()/100
    print(f"gas :{value}")
    utime.sleep(4)
    if(value > 130):
        sound_on()
        pump_on()
        led_Yellow.high()
        led_Red.low()
        lcd1_on()
    else:
        sound_off()
        pump_off()
        led_Red.high()
        led_Yellow.low()
        lcd2_off()
    path = "/update_value_hw"
    param = "ID=24&value={}".format(value)
    data = getApi(host, path, param)
    print(data)
    
    #print("Voltage is",voltage)
