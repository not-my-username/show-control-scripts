import socket
from Foundation import NSAppleScript, NSError

HOST = '0.0.0.0'
PORT = 5005

def run_applescript(ascript):
    """
    Run the given AppleScript using NSAppleScript.
    """
    apple_script = NSAppleScript.alloc().initWithSource_(ascript)
    result, error = apple_script.executeAndReturnError_(None)

    if error is not None:
        error_message = error.get("NSAppleScriptErrorMessage", "Unknown error")
        raise RuntimeError(f"AppleScript error: {error_message}")
    return result.stringValue() if result else None

def press_arrow(direction):
    if direction == "left":
        ascript = '''
        tell application "System Events"
            tell application process "Preview"
                key code 123 -- left arrow
            end tell
        end tell
        '''
    elif direction == "right":
        ascript = '''
        tell application "System Events"
            tell application process "Preview"
                key code 124 -- right arrow
            end tell
        end tell
        '''
    else:
        raise ValueError("Invalid direction. Must be 'left' or 'right'.")
    
    run_applescript(ascript)

def handle_connection(conn, addr):
    print(f"🔌 Connected by {addr}")
    try:
        with conn:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data:
                    print("📴 Connection closed by", addr)
                    break

                # Concatenate new data to the buffer
                buffer += data.decode().strip()

                # If buffer contains a full message, process it
                while 'left' in buffer or 'right' in buffer:
                    if 'left' in buffer:
                        print(f"⬅️ Received: left")
                        buffer = buffer.replace('left', '', 1)  # Remove the processed command
                        press_arrow("left")  # Move left (AppleScript keypress)
                    if 'right' in buffer:
                        print(f"➡️ Received: right")
                        buffer = buffer.replace('right', '', 1)  # Remove the processed command
                        press_arrow("right")  # Move right (AppleScript keypress)

    except Exception as e:
        print(f"⚠️ Error: {e}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        print(f"🚪 Listening on {HOST}:{PORT}...")

        while True:
            conn, addr = s.accept()
            handle_connection(conn, addr)

if __name__ == "__main__":
    main()

