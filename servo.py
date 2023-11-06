#servo.py

from machine import PWM,Pin

class PositionServo:
    def __init__(self, pin_number, freq=50, duty_us=1500):
        pin = Pin(pin_number)
        pwm = PWM(pin)
        pwm.freq(freq)
        self.pwm = pwm
        self.duty_us = duty_us

    def set_position(self, degrees):
        if degrees < 0:
            degrees = 0
        elif degrees > 180:
            degrees = 180

        pulse_width = 500 + degrees * 10  # Scale degrees to microseconds
        self.pwm.duty_ns(pulse_width * 1000)

    def stop(self):
        self.pwm.duty_ns(self.duty_us * 1000)

    def deinit(self):
        self.pwm.deinit()

class ContinuousServo:
    def __init__(self, pin_number, freq=50, duty_us=1500):
        pin = Pin(pin_number)
        pwm = PWM(pin)
        pwm.freq(freq)
        self.pwm = pwm
        self.duty_us = duty_us

    def set_speed(self, speed):
        if speed < -100:
            speed = -100
        elif speed > 100:
            speed = 100

        duty_us = self.duty_us + speed * 5
        self.pwm.duty_ns(duty_us * 1000)

    def stop(self):
        self.pwm.duty_ns(self.duty_us * 1000)

    def deinit(self):
        self.pwm.deinit()
