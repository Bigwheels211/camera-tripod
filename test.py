import board
import busio
from adafruit_pca9685 import PCA9685
import time

#i2c = busio.I2C(board.SCL, board.SDA)
#pca = PCA9685(i2c)
#pca.reset()  # Clears all channels

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

kit = ServoKit(channels=16)

# ~90 = stop, <90 = one direction, >90 = other direction
kit.continuous_servo[12].throttle = 1.0   # Full speed forward
time.sleep(2)
kit.continuous_servo[12].throttle = -1.0  # Full speed backward
time.sleep(2)
kit.continuous_servo[12].throttle = 0.1     # Stop