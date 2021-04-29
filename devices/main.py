import json
import time

from imu import IMU
import wifiCfg
from m5mqtt import M5mqtt
from m5stack import lcd, btnA, timerSch
from m5ui import setScreenColor, M5TextBox
from uiflow import wait_ms, wait

from config import (
    DEVICE_NAME,
    DEVICE_COLOR,
    WIFI_SSID,
    WIFI_PASSPHRASE,
    MQTT_HOST,
    MQTT_PASSWORD,
    MQTT_USER,
    MQTT_TOPIC_PUBLISH,
    MQTT_TOPIC_SUBSCRIBE,
)


def glapzometro():
    global GLAPZ
    accelerometer = IMU()
    if (accelerometer.acceleration[1]) > 0.7:
        GLAPZ = GLAPZ + (accelerometer.acceleration[1])


def connect_wifi():
    print("Starting Wi-Fi")
    while wifiCfg.is_connected() is False:
        print("Attempting connection")
        wifiCfg.doConnect(WIFI_SSID, WIFI_PASSPHRASE)
        wait_ms(5000)
    print("Wifi is connected")


def init_mqtt():
    global MQTT
    MQTT = M5mqtt(
        DEVICE_NAME,
        MQTT_HOST,
        1883,
        MQTT_USER,
        MQTT_PASSWORD,
        300,
    )

    MQTT.subscribe(MQTT_TOPIC_SUBSCRIBE, on_message)
    MQTT.start()


def on_message(topic_data):
    """
    callback when a message is received on specific topic
    """
    reset_glapz_and_time()


def countdown():
    """
    It's the final countdown
    """
    setScreenColor(0x000000)
    countdown = M5TextBox(18, 54, "3", lcd.FONT_DejaVu72, 0xFFFFFF, rotate=0)
    wait(1)
    countdown.setText("2")
    wait(1)
    countdown.setText("1")
    wait(1)
    countdown.setText("0")
    wait(1)
    setScreenColor(DEVICE_COLOR)


def reset_glapz_and_time():
    """
    reset glapz and time
    """
    print("reseting glapz and time")
    countdown()
    global GLAPZ
    global START_TIME
    GLAPZ = 0
    START_TIME = time.ticks_ms()


@timerSch.event("send_data")
def tsend_data():
    global GLAPZ
    global MQTT
    global START_TIME

    current_time = round((time.ticks_ms() - START_TIME) / 1000)
    MQTT.publish(
        MQTT_TOPIC_PUBLISH,
        json.dumps(
            {"device": DEVICE_NAME, "value": GLAPZ, "time": current_time}
        ),
    )


if __name__ == "__main__":
    GLAPZ = 0
    START_TIME = time.ticks_ms()
    connect_wifi()
    init_mqtt()

    # register callback on btn A
    btnA.wasPressed(reset_glapz_and_time)

    # create a timer to send_data to mqtt
    timerSch.setTimer("send_data", 1000, 0x00)
    timerSch.run("send_data", 1000, 0x00)

    # init display
    setScreenColor(DEVICE_COLOR)
    DISP_GLAPZ = M5TextBox(
        43, 19, "0 glapz", lcd.FONT_DejaVu24, 0x0F0F0F, rotate=90
    )
    DISP_TITLE = M5TextBox(
        78, 10, "Glapzometre", lcd.FONT_DejaVu18, 0x0A0A0A, rotate=90
    )

    while True:
        DISP_TITLE.show()
        DISP_GLAPZ.show()
        glapzometro()
        DISP_GLAPZ.setText(str(round(GLAPZ)) + " glapz")
        wait_ms(2)
