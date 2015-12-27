import time

import rpyc


class Robot(object):
    def __init__(self):
        self.left = ev3.LargeMotor('outB')
        self.right = ev3.LargeMotor('outC')
        self.ir = ev3.InfraredSensor()

    def find_way(self):
        self.left.run_forever(duty_cycle_sp=45)
        self.right.stop()
        while self.ir.value() < 45:
            time.sleep(0.5)
        time.sleep(1)

    def run(self):
        while True:
            self.left.run_forever(duty_cycle_sp=75)
            self.right.run_forever(duty_cycle_sp=75)
            while self.ir.value() > 45:
                time.sleep(0.5)
            self.find_way()

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


