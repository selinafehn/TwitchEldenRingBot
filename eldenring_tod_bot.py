import socket
import time
import numpy as np
from PIL import ImageGrab
import pyautogui
import cv2
import pytesseract
from credentials import TWITCH_NICK, TWITCH_TOKEN, TWITCH_CHANNEL

DEATH_AREA = (850, 1000, 2300, 1300)
server = 'irc.chat.twitch.tv'
port = 6667

def connect_to_twitch():
    while True:
        try:
            sock = socket.socket()
            sock.connect((server, port))
            sock.send(f"PASS {TWITCH_TOKEN}\r\n".encode('utf-8'))
            sock.send(f"NICK {TWITCH_NICK}\r\n".encode('utf-8'))
            sock.send(f"JOIN {TWITCH_CHANNEL}\r\n".encode('utf-8'))
            print(" Erfolgreich mit Twitch-Chat verbunden.")
            return sock
        except Exception as e:
            print(f"Fehler bei der Verbindung: {e}, versuche erneut in 5 Sekunden...")
            time.sleep(5)

def send_message(sock, message):
    try:
        sock.send(f"PRIVMSG {TWITCH_CHANNEL} :{message}\r\n".encode('utf-8'))
    except Exception as e:
        print(f"Fehler beim Senden: {e}")

def detect_death_screen():
    screenshot = pyautogui.screenshot(region=(425, 500, 775, 155))
    screenshot_np = np.array(screenshot)
    gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh_img = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("debug_ocr.png", thresh_img)  # Für Debugging
    config = '--psm 7 -l deu+eng'
    text = pytesseract.image_to_string(thresh_img, config=config)
    print("Erkannter Text:", text.strip())
    # Death-shit-text
    trigger_phrases = [
        "ihr seid gestorben",
        "IHR SEID GESTORBEN",
        "seid gestorben",
        "R SEID GES TORB",
        "gestorben",
        "R SEID GESTORB",
        "IHR SEID"
    ]
    for phrase in trigger_phrases:
        if phrase in text.lower():
            print("‼️ Todesscreen erkannt!")
            return True
    return False

def main():
    sock = connect_to_twitch()
    print("Bot läuft... (Strg+C zum Beenden)")
    death_detected = False
    send_message(sock, "!tod")
    while True:
        try:
            is_dead = detect_death_screen()
            if is_dead and not death_detected:
                print("Todesscreen erkannt! Sende !tod")
                send_message(sock, "!tod")
                death_detected = True
            elif not is_dead and death_detected:
                print("Schriftzug verschwunden, bereit für nächsten Tod")
                death_detected = False
            time.sleep(0.4)
        except KeyboardInterrupt:
            print("Bot manuell gestoppt.")
            break
        except Exception as e:
            print(f"Fehler: {e}")
            time.sleep(2)

if __name__ == '__main__':
    main()
