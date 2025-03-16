print("Pi Started! Let's save the world!")

import rpi_gpio as GPIO  # Import the QNX Raspberry Pi GPIO module
import time  # Import the time module for delays

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

# Main loop
while True:
    button_c_pressed = GPIO.input(BTN_C) == GPIO.LOW
    button_b_pressed = GPIO.input(BTN_B) == GPIO.LOW
    button_a_pressed = GPIO.input(BTN_A) == GPIO.LOW

    # Control LEDs
    GPIO.output(LED_C, button_c_pressed)
    GPIO.output(LED_B, button_b_pressed)
    GPIO.output(LED_A, button_a_pressed)

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
