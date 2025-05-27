from PIL import Image

# Originalbild laden
img = Image.open("img.png")

# Koordinaten des „Ihr seid gestorben“-Textes _--_ 500. 450. 1550. 670
crop_box = (500, 450, 1550, 670)  # (left, top, right, bottom)

# Zuschneiden
cropped = img.crop(crop_box)
cropped.save("death_template.png")

print("Vorlage gespeichert als 'death_template.png'")
