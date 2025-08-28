import numpy as np
from PIL import Image


class Map:
    def __init__(self, path):
        self.path = path

    # Funktion zum Umwandeln des Bildes in ein Array (Transparente Pixel als Weiß behandeln)
    def imageToArray(self):
        # Bild öffnen (mit Transparenz)
        img = Image.open(self.path).convert(
            "RGBA"
        )  # RGBA, um auch Transparenz zu erhalten

        # Bild in ein NumPy Array umwandeln
        img_array = np.array(img)

        # Neuer Array für das Ergebnis
        result_array = np.zeros((img_array.shape[0], img_array.shape[1]), dtype=int)

        # Pixel durchlaufen und Umwandeln
        for y in range(img_array.shape[0]):
            for x in range(img_array.shape[1]):
                r, g, b, a = img_array[y, x]  # RGBA-Werte extrahieren

                # Wenn der Pixel transparent ist (Alpha-Wert 0), wird er als Weiß behandelt
                if a == 0:
                    result_array[y, x] = 0  # Transparent als Weiß behandeln (0)
                else:
                    # ADD NEW TEXTURES TO THE BOTTOM (WRITE INTO INFO.TXT FILE FOR DOCUMENTATION)
                    if r == 0 and g == 0 and b == 0:
                        result_array[y, x] = 1  # Schwarz wird zu 1
                    elif r == 255 and g == 255 and b == 255:
                        result_array[y, x] = 0  # Weiß bleibt 0
                    elif r == 0 and g == 200 and b == 0:
                        result_array[y, x] = 2
                    elif r == 0 and g == 255 and b == 0:
                        result_array[y, x] = 3

        return result_array
