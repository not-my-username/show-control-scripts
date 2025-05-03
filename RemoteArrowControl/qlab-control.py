from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.osc_server import BlockingOSCUDPServer
import multiprocessing
from Foundation import NSAppleScript


SEND_PORT = 53000
RECV_PORT = 53001
QLAB_IP = "127.0.0.1"  # or replace with QLab's IP if remote


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

    apple_process = multiprocessing.Process(target=run_applescript, args=(ascript,))
    apple_process.start()
    apple_process.join()


def handle_go_message(address, *args):
    if len(args) < 2:
        print("⚠️ OSC message missing cue name")
        return

    cue_name = args[1]
    print(f"🎬 Cue name received: {cue_name}")

    if "forward" in cue_name.lower():
        print("➡️ Moving right")
        press_arrow("right")
    elif "back" in cue_name.lower():
        print("⬅️ Moving left")
        press_arrow("left")
    else:
        print("ℹ️ Cue name did not match any action")


def main():
    # Set up OSC client and send /listen/go to QLab
    client = SimpleUDPClient(QLAB_IP, SEND_PORT)
    client.send_message("/listen/go", True)
    print(f"📡 Subscribed to /go messages from QLab on {QLAB_IP}:{SEND_PORT}")

    # Set up dispatcher to route messages
    dispatcher = Dispatcher()
    dispatcher.map("/go", handle_go_message)

    # Start OSC server to listen for messages from QLab
    server = BlockingOSCUDPServer(("0.0.0.0", RECV_PORT), dispatcher)
    print(f"🎧 Listening for OSC on UDP {RECV_PORT}...")
    server.serve_forever()


if __name__ == "__main__":
    main()

