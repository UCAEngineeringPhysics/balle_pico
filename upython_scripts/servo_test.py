from machine import Pin, PWM, reset
from time import sleep

# SAFETY CHECK

# SETUP

# SERVO 0 KEY INFO (CLAW)                                                                                               #
# Max Duty: (2600000) Fully closed claw
# Min Duty: (1800000) Open position before grabbing the ball
# Mid Duty: (1800000) 45 degrees higher duty closes and lower duty opens
# Grab Duty: (2600000) Duty to be set after claw is in position to grab. This will ensure good hold on the ball
# servo_0 = PWM(Pin(15))
# servo_0.freq(50)
# servo_0.duty_ns(1800000)

# Servo 1 & 2 key info (ARM) - servo 1 is the left, servo 2 is the right

#Servo 1 (left)
#(1300000) is the starting/ neutral position
#(2500000) is the max/ grabbing duty value for left
#(800000) is the min/ compact config position for left. this value can change
servo_1 = PWM(Pin(13))
servo_1.freq(50)
servo_1.duty_ns(1300000)

# Total range of arm servos - (300000) to (2600000)

#Servo 2 (right)
#(1600000) is the starting/ neutral position
#(400000) is below the grabbing duty to give enough range of motion
#(~500000) is the max/ grabbing duty value for left
#(2100000) is the min/ compact config position for left. this value can change
servo_2 = PWM(Pin(14))
servo_2.freq(50)
servo_2.duty_ns(1600000)


# LOOP


# while True:
#     #Servo 1
#     print("<<<--- <<-- <- W -> -->> --->>>\n")
#     for i in range(1650000, 2600000, 50000):
#         #servo_0.duty_ns(i)
#         servo_1.duty_ns(i)
#         print(i)
#         sleep(0.2)
#     print("--->>> -->> -> W <- <<-- <<<---- \n")
#     for i in reversed(range(2600000, 700000, 50000)):
#         #servo_0.duty_ns(i)
#         servo_1.duty_ns(i)
#         print(i)
#         sleep(0.2)
#     # servo 1
#     for i in range(1800000, 2300000, 50000):
#         servo_0.duty_ns(i)
#         #servo_1.duty_ns(i)
#         print(i)
#         sleep(0.2)
#     print("--->>> -->> -> W <- <<-- <<<---- \n")
#     for i in reversed(range(2300000, 1550000, 10000)):
#         servo_0.duty_ns(i)
#         #servo_1.duty_ns(i)
#         print(i)
#         sleep(0.2)
#     servo_0.duty_ns(1800000)
#     servo_1.duty_ns(1800000)
#     sleep(1)
#     servo_0.duty_ns(2200000)
#     servo_1.duty_ns(2200000)
#     sleep(1)
#     servo_0.duty_ns(1800000)
#     servo_1.duty_ns(1800000)
#     sleep(1)
#     servo_0.duty_ns(1300000)
#     servo_1.duty_ns(1300000)
#     sleep(1)
#     servo_0.duty_ns(1800000)
#     servo_1.duty_ns(1800000)
#     sleep()
