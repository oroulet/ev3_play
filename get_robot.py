import rpyc
import robot
from IPython import embed

if __name__ == "__main__":
    conn = rpyc.classic.connect("10.0.0.119")
    ev3 = conn.modules["ev3dev.ev3"]
    r = robot.Robot()
    embed()
