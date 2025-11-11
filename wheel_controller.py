from wheel_driver import WheelDriver
from machine import Timer


class WheelController(WheelDriver):
    def __init__(self, driver_ids, encoder_ids):
        # Pin configuration
        super().__init__(driver_ids, encoder_ids)  # call super class's "__init__"
        # Constants
        self.k_p = 0.5
        self.k_i = 0.0
        self.k_d = 0.5
        self.freq_reg = 50  # Hz
        # Variables
        self.reg_vel_counter = 0
        self.duty = 0.0
        self.error = 0.0
        self.prev_error = 0.0
        self.error_inte = 0.0  # integral
        self.error_diff = 0.0  # differentiation
        self.ref_lin_vel = 0.0
        # PID controller config
        self.vel_reg_timer = Timer(
            freq=self.freq_reg,
            mode=Timer.PERIODIC,
            callback=self._regulate_velocity,
        )

    def _regulate_velocity(self, timer):
        if self.ref_lin_vel == 0.0 or self.reg_vel_counter > self.freq_reg:
            self.stop()
            self.prev_error = 0.0
        else:
            self.error = self.ref_lin_vel - self.meas_lin_vel  # ang_vel also works
            self.error_inte += self.error
            self.error_diff = self.error - self.prev_error
            self.prev_error = self.error  # UPDATE previous error
            inc_duty = (
                self.k_p * self.error
                + self.k_i * self.error_inte
                + self.k_d * self.error_diff
            )
            self.duty = self.duty + inc_duty
            if self.duty > 0:
                if self.duty > 1.0:
                    self.duty = 1.0
                self.forward(self.duty)
            else:
                if self.duty < -1.0:
                    self.duty = -1.0
                self.backward(-self.duty)
            self.reg_vel_counter += 1

    def set_velocity(self, ref_lin_vel):
        if ref_lin_vel is not self.ref_lin_vel:
            self.ref_lin_vel = ref_lin_vel
            self.prev_error = 0.0
            self.error_inte = 0.0
            self.reg_vel_counter = 0


# TEST
if __name__ == "__main__":
    from utime import sleep
    from machine import Pin

    # wc = WheelController(
    #     driver_ids=(6, 7, 8),
    #     encoder_ids=(11, 10),
    # )
    wc = WheelController(
        driver_ids=(2, 3, 4),
        encoder_ids=(21, 20),
    )
    for i in range(100):
        if i == 24:  # step up @ t=0.5 s
            wc.set_velocity(0.5)
        elif i == 74:  # step down @ t=1.5 s
            wc.set_velocity(0.0)
        print(
            f"Reference velocity={wc.ref_lin_vel} m/s, Measured velocity={wc.meas_lin_vel} m/s"
        )
        sleep(0.02)
    # Terminate
    wc.disable()
    print("Wheel disabled")
