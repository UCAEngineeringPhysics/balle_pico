from base_motor import BaseMotor
from machine import Pin


class EncodedMotor(BaseMotor):
    def __init__(self, driver_ids: list | tuple, encoder_ids: list | tuple) -> None:
        super().__init__(*driver_ids)
        # Pin configuration
        self.enca_pin = Pin(encoder_ids[0], Pin.IN)
        self.encb_pin = Pin(encoder_ids[1], Pin.IN)
        self.enca_pin.irq(trigger=Pin.IRQ_RISING, handler=self.update_counts)
        # zero out encoder counts
        self.reset_counts()

    def update_counts(self, pin):
        if self.encb_pin.value() == pin.value():  # A channel RISE later than B channel
            self.encoder_counts -= 1
        else:
            self.encoder_counts += 1

    def reset_counts(self):
        self.encoder_counts = 0


# TEST
if __name__ == "__main__":  # Test only the encoder part
    from utime import sleep

    # SETUP
    # em = EncodedMotor(
    #     driver_ids=(16, 18, 17),
    #     encoder_ids=(20, 19),
    # )  # left motor, encoder's green and yellow on GP19 and GP20
    em = EncodedMotor(
        driver_ids=(15, 13, 14),
        encoder_ids=(10, 11),
    )  # right motor, encoder's green and yellow on GP10 and GP11

    # LOOP
    # Forward ramp up and down
    for i in range(100):
        em.forward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {em.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        em.forward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {em.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down
    # Backward ramp up and down
    for i in range(100):
        em.backward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {em.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp up
    for i in reversed(range(100)):
        em.backward((i + 1) / 100)
        print(f"f, dc: {i}%, enc_cnt: {em.encoder_counts}")
        sleep(4 / 100)  # 4 seconds to ramp down

    # Terminate
    em.stop()
    sleep(0.5)
    print("motor stopped.")
