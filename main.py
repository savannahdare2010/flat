"""
The Python code you will write for this module should read
acceleration data from the IMU. When a reading comes in that surpasses
an acceleration threshold (indicating a shake), your Pi should pause,
trigger the camera to take a picture, then save the image with a
descriptive filename. You may use GitHub to upload your images automatically,
but for this activity it is not required.

The provided functions are only for reference, you do not need to use them.
You will need to complete the take_photo() function and configure the VARIABLES section
"""

# AUTHORS: Savannah Dare, Felix Quezada-York, Qi Cheng Feng, Helen Montero, Anna Keh
# DATE: 12/25/2025

# import libraries
import time                      # so everything doesn't happen too fast
import board                     # access physical pins by name
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
from git import Repo             # interact with GitHub
from picamera2 import Picamera2  # camera control
import os                        # interact with operating system

# =========================
# VARIABLES
# =========================
THRESHOLD = 1.11154
REPO_PATH = "/home/savannahdare/flat"
FOLDER_PATH = "images"

# =========================
# IMU & CAMERA INITIALIZATION
# =========================
i2c = board.I2C()
accel_gyro = LSM6DS(i2c)
mag = LIS3MDL(i2c)
picam2 = Picamera2()

# =========================
# GIT PUSH FUNCTION
# =========================
def git_push():
    """
    Stages, commits, and pushes new images to the GitHub repository.
    """
    try:
        repo = Repo(REPO_PATH)
        origin = repo.remote('origin')
        origin.pull()
        repo.git.add(os.path.join(REPO_PATH, FOLDER_PATH))
        repo.index.commit('New Photo')
        origin.push()
        print("Image uploaded to GitHub.")
    except Exception as e:
        print("Git upload failed:", e)

# =========================
# IMAGE NAME GENERATOR
# =========================
def img_gen(name):
    """
    Generates a timestamped image filename.

    Parameters:
        name (str): name prefix for image
    """
    t = time.strftime("_%H%M%S")
    return os.path.join(REPO_PATH, FOLDER_PATH, f"{name}{t}.jpg")

# =========================
# PHOTO CAPTURE LOGIC
# =========================
def take_photo():
    """
    Takes a photo when acceleration magnitude exceeds THRESHOLD.
    """

    # Camera setup (run once)
    capture_config = picam2.create_still_configuration()
    picam2.configure(capture_config)
    picam2.start()
    time.sleep(2)  # camera warm-up

    while True:
        accelx, accely, accelz = accel_gyro.acceleration
        mag_accel = (accelx**2 + accely**2 + accelz**2) ** 0.5
        dynamic_accel = abs(9.81 - mag_accel)

        if dynamic_accel > THRESHOLD:
            time.sleep(0.5)  # debounce
            name = "SavannahD"
            image_name = img_gen(name)
            picam2.capture_file(image_name)
            git_push()
            time.sleep(2)  # prevent rapid retriggering

        time.sleep(0.1)

# =========================
# MAIN
# =========================
def main():
    take_photo()

if __name__ == "__main__":
    main()
