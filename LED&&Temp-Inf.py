# get temperature:
import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()

while True:
    temperature = sensor.get_temperature()
    print("The temperature is %s celsius" % temperature)
    time.sleep(1)

#turn light on:
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) 
GPIO.setup(18, GPIO.OUT)

GPIO.output(18, GPIO.HIGH) #digitalWrite(18, HIGH)

# off:
GPIO.output(18, GPIO.LOW) #digitalWrite(18, LOW)

            try:
                pass
            except:
                pass
            except:
                pass
            finally:
                GPIO.cleanup()