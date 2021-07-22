from aol_db import *
import os
import pytesseract

try:
    from PIL import Image
except ImportError:
    import Image

folder = "./static/"

db = aol_db()
db.create_connection()

for path, folders, files in os.walk(folder):
    for img in files:
        if not db.isConvertedToText(img):
            text = pytesseract.image_to_string(Image.open(folder + img), lang="tur")
            db.update_question(img, text)

db.close_connection()
