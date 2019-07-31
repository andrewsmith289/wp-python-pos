from threading import Timer
from sys import exit
from os import name
if name is 'posix':
    import RPi.GPIO as GPIO
from SharedUtilities import printt


class Buzzer(object):
    dc = 75  # duty cycle (0-100) for PWM pin
    active = False
    pwm = {}
    supported_platform = False

    def __init__(self, pin):
        if name is 'posix':
            GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
            GPIO.setup(pin, GPIO.OUT)  # PWM pin set as output
            self.pwm = GPIO.PWM(pin, self.dc)  # Initialize PWM on pwmPin
            self.supported_platform = True
        else:
            printt("This platform does not support the (Linux Only) GPIO Library")

    def start(self, duty_cycle=10):
        if not self.supported_platform:
            printt('Warning: Unsupported GPIO environment. Buzzer would have started.')
            return
        if not self.active:
            self.pwm.start(duty_cycle)
            self.active = True

    def stop(self):
        self.active = False

        if not self.supported_platform:
            printt('Warning: Unsupported GPIO environment. Buzzer would have stopped.')
            return

        self.pwm.stop()

    def t_stop(self):
        self.stop()
        exit() # destroy thread to avoid leaks

    def buzz(self, millis=1000):
        self.start(self.dc)
        Timer(millis / 1000, self.t_stop).start()