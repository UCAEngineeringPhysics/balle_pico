from machine import Pin, PWM


class MotorDriver:
    def __init__(self, ina_id, inb_id, pwm_id):
        self.ina_pin = Pin(ina_id, Pin.OUT)
        self.inb_pin = Pin(inb_id, Pin.OUT)
        self.pwm_pin = PWM(Pin(pwm_id))
        self.pwm_pin.freq(1000)
        self.disable()

    def stop(self):
        self.pwm_pin.duty_u16(0)

    def forward(self, duty):
        assert 0 <= duty <= 1  # make sure dutycycle in [0, 1]
        self.ina_pin.on()
        self.inb_pin.off()
        self.pwm_pin.duty_u16(int(65535 * duty))

    def backward(self, duty):
        assert 0 <= duty <= 1  # make sure dutycycle in [0, 1]
        self.ina_pin.off()
        self.inb_pin.on()
        self.pwm_pin.duty_u16(int(65535 * duty))

    def disable(self):
        self.ina_pin.off()
        self.inb_pin.off()


if __name__ == "__main__":
    from time import sleep

    # SETUP
    # md = MotorDriver(ina_id=6, inb_id=7, pwm_id=8)  # left
    md = MotorDriver(ina_id=2, inb_id=3, pwm_id=4)  # right

    # LOOP
    for i in range(100):
        md.forward((i + 1) / 100)
        print(f"f, dc: {i}%")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        md.forward((i + 1) / 100)
        print(f"f, dc: {i}%")
        sleep(4 / 100)  # 4 seconds to ramp down
    # Backwardly ramp up and down
    for i in range(100):
        md.backward((i + 1) / 100)
        print(f"b, dc: {i}%")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        md.backward((i + 1) / 100)
        print(f"b, dc: {i}%")
        sleep(4 / 100)  # 4 seconds to ramp down

    # TERMINATE
    md.disable()
    print("Motor driver disabled")
