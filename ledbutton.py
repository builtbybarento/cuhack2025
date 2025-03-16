import rpi_gpio as GPIO  # Import the QNX Raspberry Pi GPIO module
import time  # Import the time module for delays
import json
import asyncio
import websockets

# GPIO pin assignments
LED_C = 26
LED_B = 19
LED_A = 6
BTN_C = 16
BTN_B = 20
BTN_A = 21
BUZZER_PIN = 13

# WebSocket server configuration
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 8765

# Global variables to track button states for WebSocket transmission
button_states = {
    'A': False,
    'B': False,
    'C': False
}

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

# Track connected WebSocket clients
connected_clients = set()

async def handle_websocket(websocket, path):
    """Handle WebSocket connections and communication."""
    # Add the client to our set of connected clients
    connected_clients.add(websocket)
    try:
        # Send the initial button states to the new client
        await websocket.send(json.dumps(button_states))
        
        # Keep the connection open and handle incoming messages
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message: {data}")
                # Handle any commands from the client if needed
            except json.JSONDecodeError:
                print(f"Received invalid JSON: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # Remove the client when they disconnect
        connected_clients.remove(websocket)

async def broadcast_button_states():
    """Broadcast button states to all connected clients."""
    if connected_clients:
        message = json.dumps(button_states)
        await asyncio.gather(
            *[client.send(message) for client in connected_clients]
        )

async def read_buttons():
    """Read button states and update LEDs/buzzer."""
    global last_button_a_state, last_button_b_state, last_button_c_state
    global a_processed, b_processed, c_processed
    global last_a_press_time, last_b_press_time, last_c_press_time
    global button_states
    
    while True:
        current_time = int(time.time() * 1000)  # Current time in milliseconds
        
        button_c_pressed = GPIO.input(BTN_C) == GPIO.LOW
        button_b_pressed = GPIO.input(BTN_B) == GPIO.LOW
        button_a_pressed = GPIO.input(BTN_A) == GPIO.LOW
        
        # Control LEDs
        GPIO.output(LED_C, button_c_pressed)
        GPIO.output(LED_B, button_b_pressed)
        GPIO.output(LED_A, button_a_pressed)
        
        # Track state changes for WebSocket broadcasting
        states_changed = False
        
        # Debounce handling for button C
        if button_c_pressed and last_button_c_state == GPIO.HIGH:
            if (current_time - last_c_press_time) > debounce_delay and not c_processed:
                print('C pressed')
                last_c_press_time = current_time
                c_processed = True  # Mark as processed to prevent repeat while held
                button_states['C'] = True
                states_changed = True
        elif not button_c_pressed and button_states['C']:
            c_processed = False  # Reset the processed flag when button is released
            button_states['C'] = False
            states_changed = True
        
        # Debounce handling for button B
        if button_b_pressed and last_button_b_state == GPIO.HIGH:
            if (current_time - last_b_press_time) > debounce_delay and not b_processed:
                print('B pressed')
                last_b_press_time = current_time
                b_processed = True  # Mark as processed to prevent repeat while held
                button_states['B'] = True
                states_changed = True
        elif not button_b_pressed and button_states['B']:
            b_processed = False  # Reset the processed flag when button is released
            button_states['B'] = False
            states_changed = True
        
        # Debounce handling for button A
        if button_a_pressed and last_button_a_state == GPIO.HIGH:
            if (current_time - last_a_press_time) > debounce_delay and not a_processed:
                print('A pressed')
                last_a_press_time = current_time
                a_processed = True  # Mark as processed to prevent repeat while held
                button_states['A'] = True
                states_changed = True
        elif not button_a_pressed and button_states['A']:
            a_processed = False  # Reset the processed flag when button is released
            button_states['A'] = False
            states_changed = True
        
        # Update the last button states
        last_button_c_state = button_c_pressed
        last_button_b_state = button_b_pressed
        last_button_a_state = button_a_pressed
        
        # Turn buzzer ON if any button is pressed, OFF otherwise
        if button_c_pressed or button_b_pressed or button_a_pressed:
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
        else:
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        
        # Broadcast button states if they've changed
        if states_changed:
            await broadcast_button_states()
        
        # Short delay to reduce CPU usage
        await asyncio.sleep(0.01)

async def main():
    """Main function to start the WebSocket server and button reading."""
    # Start the WebSocket server
    server = await websockets.serve(handle_websocket, HOST, PORT)
    print(f"WebSocket server started on ws://{HOST}:{PORT}")
    
    # Start reading buttons
    button_task = asyncio.create_task(read_buttons())
    
    # Keep the server running
    await server.wait_closed()

# Run the main function
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program stopped by user")
    finally:
        # Clean up GPIO
        GPIO.cleanup()