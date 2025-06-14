#!/usr/bin/env python3
"""
screenshot_death_area.py

Nimmt einen Screenshot auf und zeichnet ein Rechteck um die vorgegebene DEATH_AREA.
"""

import pyautogui
from PIL import ImageDraw

# Bereich, der markiert werden soll (x1, y1, x2, y2)
DEATH_AREA = (425, 500, 1150, 650)


def main():
    # Screenshot aufnehmen
    img = pyautogui.screenshot(region=(425, 500, 725, 150))



    # Bild speichern
    output_path = "screenshot_with_death_area.png"
    img.save(output_path)
    print(f"Screenshot mit markierter DEATH_AREA gespeichert als: {output_path}")


if __name__ == "__main__":
    main()
