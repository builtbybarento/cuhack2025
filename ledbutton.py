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

# Button state tracking variables
last_button_a_state = GPIO.HIGH
last_button_b_state = GPIO.HIGH
last_button_c_state = GPIO.HIGH

# Flags to track if button has been processed (to prevent repeated inputs when held)
a_processed = False
b_processed = False
c_processed = False

# Time variables for debouncing
last_a_press_time = 0
last_b_press_time = 0
last_c_press_time = 0
debounce_delay = 50  # Debounce time in milliseconds

# Main loop
while True:
    current_time = int(time.time() * 1000)  # Current time in milliseconds
    
    button_c_pressed = GPIO.input(BTN_C) == GPIO.LOW
    button_b_pressed = GPIO.input(BTN_B) == GPIO.LOW
    button_a_pressed = GPIO.input(BTN_A) == GPIO.LOW
    
    # Control LEDs
    GPIO.output(LED_C, button_c_pressed)
    GPIO.output(LED_B, button_b_pressed)
    GPIO.output(LED_A, button_a_pressed)
    
    # Debounce handling for button C
    if button_c_pressed and last_button_c_state == GPIO.HIGH:
        if (current_time - last_c_press_time) > debounce_delay and not c_processed:
            print('C pressed')
            last_c_press_time = current_time
            c_processed = True  # Mark as processed to prevent repeat while held
    elif not button_c_pressed:
        c_processed = False  # Reset the processed flag when button is released
    
    # Debounce handling for button B
    if button_b_pressed and last_button_b_state == GPIO.HIGH:
        if (current_time - last_b_press_time) > debounce_delay and not b_processed:
            print('B pressed')
            last_b_press_time = current_time
            b_processed = True  # Mark as processed to prevent repeat while held
    elif not button_b_pressed:
        b_processed = False  # Reset the processed flag when button is released
    
    # Debounce handling for button A
    if button_a_pressed and last_button_a_state == GPIO.HIGH:
        if (current_time - last_a_press_time) > debounce_delay and not a_processed:
            print('A pressed')
            last_a_press_time = current_time
            a_processed = True  # Mark as processed to prevent repeat while held
    elif not button_a_pressed:
        a_processed = False  # Reset the processed flag when button is released
    
    # Update the last button states
    last_button_c_state = button_c_pressed
    last_button_b_state = button_b_pressed
    last_button_a_state = button_a_pressed
    
    # Turn buzzer ON if any button is pressed, OFF otherwise
    if button_c_pressed or button_b_pressed or button_a_pressed:
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
    else:
        GPIO.output(BUZZER_PIN, GPIO.LOW)
    
    time.sleep(0.01)  # Short delay to reduce CPU usage