from machine import Pin, PWM, Timer
from time import sleep


SHOULDER_NEUTRAL = 1_500_000  # nano sec
SHOULDER_MAX = 2_200_000
SHOULDER_MIN = 1_000_000
CLAW_NEUTRAL = 1_800_000
CLAW_MAX = 2_550_000
CLAW_MIN = 1_550_000
PULSE_WIDTH_INC_STEP = 5_000


class ArmController:
    # TODO: timer for setting target positions
    def __init__(self, claw_pin, shoulder_a_pin, shoulder_b_pin):
        self.claw = PWM(Pin(claw_pin))
        self.shoulder_a = PWM(Pin(shoulder_a_pin))
        self.shoulder_b = PWM(Pin(shoulder_b_pin))
        self.claw.freq(50)
        self.shoulder_a.freq(50)
        self.shoulder_b.freq(50)
        # Set to neutral
        self.claw.duty_ns(CLAW_NEUTRAL)
        self.shoulder_a.duty_ns(SHOULDER_NEUTRAL)
        self.shoulder_b.duty_ns(SHOULDER_NEUTRAL)
        # Variables
        self.pulse_width_claw = CLAW_NEUTRAL
        self.pulse_width_shoa = SHOULDER_NEUTRAL
        self.pulse_width_shob = SHOULDER_NEUTRAL
        self.target_claw = CLAW_NEUTRAL
        self.target_shoa = SHOULDER_NEUTRAL
        self.target_shob = SHOULDER_NEUTRAL
        # Set joint pos timer
        self.joints_set_timer = Timer(
            freq=50,
            mode=Timer.PERIODIC,
            callback=self.manipulate_joints,
        )

    def set_joint_positions(
        self,
        target_claw=CLAW_NEUTRAL,
        target_shoa=SHOULDER_NEUTRAL,
    ):
        self.target_claw = target_claw
        self.target_shoa = target_shoa
        self.target_shob = SHOULDER_NEUTRAL - (target_shoa - SHOULDER_NEUTRAL)

    def manipulate_joints(self, timer):
        diff_claw = self.target_claw - self.pulse_width_claw
        diff_shoa = self.target_shoa - self.pulse_width_shoa
        self.pulse_width_claw += max(
            min(diff_claw, PULSE_WIDTH_INC_STEP), -PULSE_WIDTH_INC_STEP
        )
        self.pulse_width_shoa += max(
            min(diff_shoa, PULSE_WIDTH_INC_STEP), -PULSE_WIDTH_INC_STEP
        )
        self.pulse_width_shob -= max(
            min(diff_shoa, PULSE_WIDTH_INC_STEP), -PULSE_WIDTH_INC_STEP
        )
        self.claw.duty_ns(self.pulse_width_claw)
        self.shoulder_a.duty_ns(self.pulse_width_shoa)
        self.shoulder_b.duty_ns(self.pulse_width_shob)

    # def set_neutral(self):
    #     self.shoulder_servo_a.duty_ns(SHOULDER_NEUTRAL)
    #     self.shoulder_servo_b.duty_ns(SHOULDER_NEUTRAL)
    #     self.claw_servo.duty_ns(CLAW_NEUTRAL)
    #     # Save neutral value as current value
    #     self.shoulder_duty_a = SHOULDER_NEUTRAL
    #     self.shoulder_duty_b = SHOULDER_NEUTRAL
    #     self.claw_duty = CLAW_NEUTRAL
    #
    # def lower_claw(self, dc_inc=0):  # negtive dc_inc to raise arm
    #     assert -50_000 <= dc_inc <= 50_000  # recommend dc increment: <20_000 ns
    #     self.shoulder_duty_a += dc_inc
    #     self.shoulder_duty_b -= dc_inc
    #     # Lowest
    #     if self.shoulder_duty_a >= 2_400_000:
    #         self.shoulder_duty_a = 2_400_000
    #         self.shoulder_duty_b = 700_000
    #     # Highest
    #     elif self.shoulder_duty_a <= 700_000:
    #         self.shoulder_duty_a = 700_000
    #         self.shoulder_duty_b = 2_700_000
    #     self.shoulder_servo_a.duty_ns(self.shoulder_duty_a)
    #     self.shoulder_servo_b.duty_ns(self.shoulder_duty_b)
    #
    # def close_claw(self, dc_inc=0):
    #     assert -50_000 <= dc_inc <= 50_000
    #     self.claw_duty += dc_inc
    #     if self.claw_duty >= 2_500_000:  # 2_500_000
    #         self.claw_duty = 2_500_000
    #     elif self.claw_duty <= 1_550_000:
    #         self.claw_duty = 1_550_000
    #     self.claw_servo.duty_ns(self.claw_duty)
    #


# Example usage
if __name__ == "__main__":
    from utime import sleep

    ac = ArmController(15, 13, 14)
    sleep(1)
    ac.set_joint_positions(CLAW_MAX, SHOULDER_MIN)
    sleep(5)

#     for _ in range(80):
#         ac.close_claw(10_000)
#         sleep(0.1)
#         print(f"Closing claw duty cycle: {ac.claw_duty}")
#     for _ in range(20):
#         ac.close_claw(-20_000)
#         sleep(0.1)
#         print(f"Opening claw duty cycle: {ac.claw_duty}")
#
#     ac.set_neutral()
#     sleep(1)
#     print("arm set to neutral")
#
#     for _ in range(20):
#         ac.lower_claw(20_000)
#         sleep(0.1)
#         #print(f"Lowering claw duty cycle: {ac.shoulder_duty}")
#     for _ in range(20):
#         ac.lower_claw(-20_000)
#         sleep(0.1)
# print(f"Lifting claw duty cycle: {ac.shoulder_duty}")
