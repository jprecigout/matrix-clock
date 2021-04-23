# main.py
from machine import Pin, SPI, Timer
import network
import utime
import ntptime
import ujson
import max7219

# ESP32 / Matrix
# MOSI = DIN
# CS = CS
# SCK = CLK
din = 12
cs = 14
clk = 27
DISPLAY_BRIGHTNESS = 2
CLOCK_TIMER_DELAY = 1000 # (ms)

def connect_network(network_ssid: str, network_password: str) -> None:
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(network_ssid, network_password)

    while station.isconnected() == False:
        pass

    print('Connection Network successful')

#mask = "{3:02d}:{4:02d} - {2:02d}/{1:02d}/{0:02d}"
#output = mask.format(*local_time)
# for p in range(8 * 8, len(output) * -8 - 1, -1):
#     display.fill(0)
#     display.text(output, p, 0, not 0)
#     display.show()
#     utime.sleep_ms(60)
def data_display(timer):
    local_time_sec = utime.time() + timezone_hour * 3600
    local_time = utime.localtime(local_time_sec)
    mask = "{3:02d}{4:02d}"
    output = mask.format(*local_time)
    display.fill(0)
    display.text(output, 0, 0, 1)
    # display.pixel(15,3,1)
    # display.pixel(16,3,1)
    display.show()


spi = SPI(1, baudrate=10000000, polarity=1, phase=0, sck=Pin(clk), mosi=Pin(din))
display = max7219.Matrix8x8(spi, Pin(cs), 4)
display.brightness(DISPLAY_BRIGHTNESS)

# Read secret
try:
    with open('secrets.json') as fp:
        secrets = ujson.loads(fp.read())
except OSError as e:
    print("secrets.json file is missing")

# Connect network
try:
    connect_network(secrets["wifi"]["ssid"], secrets["wifi"]["password"])
except OSError as e:
    print("Network connection is not possible")

ntptime.settime()
timezone_hour = 2  # timezone offset (hours)

timer_clock  = Timer(-1)
timer_clock.init(period=CLOCK_TIMER_DELAY,
                 mode=Timer.PERIODIC,
                 callback=data_display)
data_display(None)

