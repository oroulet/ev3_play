import time

import rpyc

conn = rpyc.classic.connect("10.0.0.119")
ev3 = conn.modules["ev3dev.ev3"]


class Robot(object):
    def __init__(self):
        self.left = ev3.LargeMotor('outB')
        self.right = ev3.LargeMotor('outC')
        self.weapon = ev3.MediumMotor('outA')
        self.ir = ev3.InfraredSensor()
        self.touch = ev3.TouchSensor()
        #for light in (ev3.Leds.LEFT, ev3.Leds.RIGHT):
            #ev3.Leds.set_color(ev3.light, ev3.Leds.RED)

    def turn(self):
        self.left.run_forever(duty_cycle_sp=35)
        self.right.run_forever(duty_cycle_sp=-35)
        while self.ir.value() < 45:
            time.sleep(0.5)
        time.sleep(1)

    def run(self):
        while True:
            self.left.run_forever(duty_cycle_sp=75)
            self.right.run_forever(duty_cycle_sp=75)
            while True:
                if self.ir.value() < 45:
                    break
                if self.ir.value() < 70:
                    self.weapon.run_forever(duty_cycle_sp=100)
                if self.ir.value() > 70:
                    self.weapon.stop()
                if self.touch.value() == 1:
                    self.left.run_forever(duty_cycle_sp=-20)
                    self.right.run_forever(duty_cycle_sp=-20)
                    time.sleep(3)
                    break

                time.sleep(0.1)
            self.turn()

    def stop(self):
        self.left.stop()
        self.right.stop()


if __name__ == "__main__":
    conn = rpyc.classic.connect("10.0.0.119")
    ev3 = conn.modules["ev3dev.ev3"]
    r = Robot()
    try:
        r.run()
    finally:
        r.stop()


