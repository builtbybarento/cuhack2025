import rpi_gpio as GPIO  # Import the QNX Raspberry Pi GPIO module
import time  # Import the time module for delays
from rainbowhat import RainbowHat  # Import the Rainbow HAT library

print("Pi Started! Let's save the world!")

# GPIO pin assignments
LED_C = 26
LED_B = 19
LED_A = 6
BTN_C = 16
BTN_B = 20
BTN_A = 21
BUZZER_PIN = 13

# Setup GPIO
GPIO.setup(LED_C, GPIO.OUT)
GPIO.setup(LED_B, GPIO.OUT)
GPIO.setup(LED_A, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

GPIO.setup(BTN_C, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BTN_B, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(BTN_A, GPIO.IN, GPIO.PUD_UP)

# Ensure all outputs are off initially
GPIO.output(LED_C, GPIO.LOW)
GPIO.output(LED_B, GPIO.LOW)
GPIO.output(LED_A, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# Initialize Rainbow HAT LED strip
ledstrip = RainbowHat.openLedStrip()
ledstrip.setBrightness(31)  # Set brightness to max

# Function to create rainbow effect
def flash_rainbow():
    rainbow = [0] * RainbowHat.LEDSTRIP_LENGTH
    for i in range(len(rainbow)):
        # Generate rainbow colors
        rainbow[i] = RainbowHat.Color.HSVToColor(255, [i * 360.0 / RainbowHat.LEDSTRIP_LENGTH, 1.0, 1.0])
    ledstrip.write(rainbow)

def clear_rainbow():
    ledstrip.clear()

# Main loop
while True:
    button_c_pressed = GPIO.input(BTN_C) == GPIO.LOW
    button_b_pressed = GPIO.input(BTN_B) == GPIO.LOW
    button_a_pressed = GPIO.input(BTN_A) == GPIO.LOW

    # Control LEDs for button presses
    GPIO.output(LED_C, button_c_pressed)
    GPIO.output(LED_B, button_b_pressed)
    GPIO.output(LED_A, button_a_pressed)

    # Flash Rainbow Lights when a button is pressed
    if button_c_pressed or button_b_pressed or button_a_pressed:
        flash_rainbow()  # Create the rainbow effect on button press
        time.sleep(0.5)  # Keep rainbow effect for half a second
        clear_rainbow()  # Clear rainbow effect
        time.sleep(0.5)  # Keep lights off for half a second

    # Print button presses
    if button_c_pressed:
        print('C pressed')
    if button_b_pressed:
        print('B pressed')
    if button_a_pressed:
        print('A pressed')

    # Turn buzzer ON if any button is pressed, OFF otherwise
    if button_c_pressed or button_b_pressed or button_a_pressed:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    time.sleep(0.05)  # Short delay to reduce CPU usage
