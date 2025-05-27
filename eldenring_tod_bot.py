import socket
import time
import cv2
import numpy as np
from PIL import ImageGrab
from credentials import TWITCH_NICK, TWITCH_TOKEN, TWITCH_CHANNEL

DEATH_TEMPLATE_PATH = 'death_template.png'
template = cv2.imread(DEATH_TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)

# === Twitch IRC-Verbindung ===
server = 'irc.chat.twitch.tv'
port = 6667

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {TWITCH_TOKEN}\r\n".encode('utf-8'))
sock.send(f"NICK {TWITCH_NICK}\r\n".encode('utf-8'))
sock.send(f"JOIN {TWITCH_CHANNEL}\r\n".encode('utf-8'))

print("✅ Erfolgreich mit Twitch-Chat verbunden.")

# === Funktion zum Tod erkennen ===
def detect_death_screen(threshold=0.85):
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return len(loc[0]) > 0

def send_message(message):
    sock.send(f"PRIVMSG {TWITCH_CHANNEL} :{message}\r\n".encode('utf-8'))

# === Hauptfunktion mit Debug- und Testausgaben ===
def main():
    print("🤖 Bot läuft...")

    # 💬 Test: Sende sofort eine Nachricht in den Chat
    print("📤 Sende Testnachricht...")
    send_message("Test: EldenRingBot ist online")

    last_trigger_time = 0
    cooldown = 10  # Sekunden

    while True:
        try:
            print("🖼️ Screenshot analysieren...")

            if detect_death_screen():
                print("‼️ Schriftzug erkannt!")
                if time.time() - last_trigger_time > cooldown:
                    print("✅ Sende !tod")
                    send_message("!tod")
                    last_trigger_time = time.time()
                else:
                    print("⏳ Noch im Cooldown...")
            else:
                print("❌ Kein Tod erkannt.")

            time.sleep(1)

        except KeyboardInterrupt:
            print("⛔ Bot manuell gestoppt.")
            break

if __name__ == '__main__':
    main()
