from machine import Pin, PWM, Timer
from time import sleep

SHOULDER_NEUTRAL = 1_400_000
CLAW_MAX = 2_050_000
CLAW_MIN = 1_550_000
CLAW_MID = (CLAW_MAX + CLAW_MIN) // 2
CLAW_RANGE = (CLAW_MAX - CLAW_MIN) // 2


class ArmController:
    def __init__(self, claw_id, left_shoulder_id, right_shoulder_id):
        # Config servo pins
        self.claw = PWM(Pin(claw_id))
        self.claw.freq(50)
        self.left_shoulder = PWM(Pin(left_shoulder_id))
        self.left_shoulder.freq(50)
        self.right_shoulder = PWM(Pin(right_shoulder_id))
        self.right_shoulder.freq(50)
        # Config controller timer
        self.jp_reg_timer = Timer(
            freq=25,
            mode=Timer.PERIODIC,
            callback=self.regulate_joints,
        )
        # Variables
        self.claw_pulse_width = CLAW_MID
        self.targ_pos_claw = 0
        self.pos_inc = 0.2
        # Constants
        self.claw.duty_ns(CLAW_MID)
        self.pw_inc = 50_000

    def regulate_joints(self, timer):
        err_claw = self.targ_pos_claw - self.claw_pos
        if err_claw > 0:
            self.claw_pos += self.pos_inc
            if self.claw_pos > 1:
                self.claw_pos = 1
        elif err_claw < 0:
            self.claw_pos -= self.pos_inc
            if self.claw_pos < -1:
                self.claw_pos = -1
        else:
            self.claw_pos = self.targ_pos_claw
        self.claw.duty_ns(CLAW_MID + int(self.claw_pos * CLAW_RANGE))

    def set_joint_positions(self, targ_pos_claw):
        assert -1 <= targ_pos_claw <= 1
        self.targ_pos_claw = targ_pos_claw

    # def close_claw(self, dir):  # Close claw
    #     """
    #     Open/Close claw
    #     Args:
    #         dir: -1/0/1, open/maintain/close
    #     """
    #     self.claw_pulse_width += self.pw_inc * dir
    #     if self.claw_pulse_width >= CLAW_MAX:
    #         self.claw_pulse_width = CLAW_MAX
    #     elif self.claw_pulse_width <= CLAW_MIN:
    #         self.claw_pulse_width = CLAW_MIN
    #     self.claw.duty_ns(self.claw_pulse_width)
    #


# Example usage
if __name__ == "__main__":
    from utime import sleep

    sleep(1)
    ac = ArmController(2, 3, 4)
    ac.set_joint_positions(0)
