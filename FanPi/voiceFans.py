import RPi.GPIO as GPIO
import sys


def fans(mode):
    # Set up GPIO mode and pin number
    GPIO.setmode(GPIO.BOARD)

    ch1 = 37
    ch2 = 38
    ch3 = 40

    # Set up GPIO pin as output
    GPIO.setup(ch1, GPIO.OUT)
    GPIO.setup(ch2, GPIO.OUT)
    GPIO.setup(ch3, GPIO.OUT)

    try:
        GPIO.output(ch3, GPIO.HIGH)
        mode = mode.lower()
        if mode == "l" or mode == "low":
            GPIO.output(ch1, GPIO.LOW)
            GPIO.output(ch2, GPIO.HIGH)
        elif mode == "h" or mode == "high":
            GPIO.output(ch1, GPIO.LOW)
            GPIO.output(ch2, GPIO.LOW)
        else:
            GPIO.output(ch1, GPIO.HIGH)
            GPIO.output(ch2, GPIO.HIGH)
    except KeyboardInterrupt:
        print("Ctrl+C pressed. Exiting...")
        GPIO.cleanup()


if len(sys.argv) > 1:
    fans(sys.argv[1])
