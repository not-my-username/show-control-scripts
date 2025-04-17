import socket
import subprocess

HOST = '0.0.0.0'
PORT = 5005

def press_arrow(direction):
    key_code = 123 if direction == "left" else 124  # 123 = left, 124 = right
    script = f'''
    tell application "Preview" to activate
    delay 0.2 -- small delay to ensure it's active
    tell application "System Events"
        tell application process "Preview"
            key code {key_code}
        end tell
    end tell
    '''
    subprocess.run(["osascript", "-e", script])

def handle_connection(conn, addr):
    print(f"🔌 Connected by {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    print("📴 Connection closed by", addr)
                    break
                direction = data.decode().strip()
                print(f"⬅️➡️ Received: {direction}")
                if direction in ("left", "right"):
                    press_arrow(direction)
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

