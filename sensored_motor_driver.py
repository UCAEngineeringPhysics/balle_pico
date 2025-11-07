from motor_driver import MotorDriver
from machine import Pin


class SensoredMotorDriver(MotorDriver):
    def __init__(self, driver_pins, encoder_pins):
        # Pin configuration
        super().__init__(*driver_pins)
        self.enca = Pin(encoder_pins[0], Pin.IN)
        self.encb = Pin(encoder_pins[1], Pin.IN)
        self.enca.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._update_counts_a
        )
        self.enca.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._update_counts_b
        )
        # Variables
        self._enca_val = self.enca.value()
        self._encb_val = self.encb.value()
        self.encoder_counts = 0
        # Properties
        self.cpr = 64  # pulses per revolution, PPR * 4 = CPR
        self.gear_ratio = (
            102.083  # speed reduction rate, v_wheel = v_motor / GEAR_RATIO
        )

    def _update_counts_a(self, pin):
        self._enca_val = pin.value()
        if self._enca_val == 1:
            if self._encb_val == 0:  # a=1, b=0
                self.encoder_counts += 1
            else:  # a=1, b=1
                self.encoder_counts -= 1
        else:
            if self._encb_val == 0:  # a=0, b=0
                self.encoder_counts -= 1
            else:  # a=0, b=1
                self.encoder_counts += 1

    def _update_counts_b(self, pin):
        self._encb_val = pin.value()
        if self._encb_val == 1:
            if self._enca_val == 0:  # b=1, a=0
                self.encoder_counts -= 1
            else:  # b=1, a=1
                self.encoder_counts += 1
        else:
            if self._enca_val == 0:  # b=0, a=0
                self.encoder_counts += 1
            else:  # b=0, a=1
                self.encoder_counts -= 1

    def reset_encoder_counts(self):
        self.encoder_counts = 0

    # def measure_velocity(self, timer):
    #     delta_counts = self.encoder_counts - self.prev_counts
    #     self.prev_counts = self.encoder_counts  # UPDATE prev_counts
    #     counts_per_sec = delta_counts * self.vel_meas_freq  # delta_c / delta_t
    #     orig_rev_per_sec = counts_per_sec / self.cpr
    #     orig_rad_per_sec = orig_rev_per_sec * 2 * pi  # original motor shaft velocity
    #     self.meas_ang_vel = orig_rad_per_sec / self.gear_ratio
    #     self.meas_lin_vel = self.meas_ang_vel * self.meas_radius


if __name__ == "__main__":
    from time import sleep

    # SETUP
    smd = SensoredMotorDriver((2, 3, 4), (21, 20))

    # LOOP
    for i in range(100):
        smd.forward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {smd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        smd.forward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {smd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down
    # Backwardly ramp up and down
    for i in range(100):
        smd.backward((i + 1) / 100)
        print(f"b, dc: {i}%, enc_cnt: {smd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        smd.backward((i + 1) / 100)
        print(f"b, dc: {i}%, enc_cnt: {smd.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down

    # TERMINATE
    smd.disable()
