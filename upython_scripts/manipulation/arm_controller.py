from machine import Pin, PWM, Timer
from time import sleep


SHOULDER_NEUTRAL = 1_400_000  # nano sec
SHOULDER_MAX = 2_400_000  # nano sec
SHOULDER_MIN = 700_000  # nano sec
CLAW_NEUTRAL = 1_800_000
CLAW_MAX = 2_500_000
CLAW_MIN = 1_550_000


class ArmController:
    # TODO: timer for setting target positions
    def __init__(self, claw_pin, shoulder_a_pin, shoulder_b_pin):
        self.claw = PWM(Pin(claw_pin))
        self.shoulder_a = PWM(Pin(shoulder_a_pin))
        self.shoulder_b = PWM(Pin(shoulder_b_pin))
        self.claw.freq(50)
        self.shoulder_a.freq(50)
        self.shoulder_b.freq(50)
        # Set initial positions
        # self.set_neutral()
        self.joints_set_timer = Timer(
            freq=100,
            mode=Timer.PERIODIC,
            callback=self.set_joint_positions,
        )
        # Variables
        self.claw_target = CLAW_MAX
        self.shoulder_a_target = SHOULDER_NEUTRAL
        self.shoulder_b_target = SHOULDER_NEUTRAL

    def set_joint_positions(self, timer):
        self.claw.duty_ns(self.claw_target)
        self.shoulder_a.duty_ns(self.shoulder_a_target)
        self.shoulder_b.duty_ns(self.shoulder_b_target)

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

    sleep(1)
    ac = ArmController(15, 13, 14)
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
