"""Converts image to text"""

import os
import pytesseract
from PIL import Image
from aol_db import AolDb


def main() -> None:
    """Main function"""
    folder = "./static/"
    aol_db = AolDb()
    aol_db.create_connection()

    for *_, files in os.walk(folder):
        for img in files:
            if not aol_db.is_converted_to_text(img):
                text = pytesseract.image_to_string(Image.open(folder + img), lang="tur")
                aol_db.update_question(img, text)

    aol_db.close_connection()


if __name__ == "__main__":
    main()
