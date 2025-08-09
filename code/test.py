import shutil, os
import pytesseract

print("tesseract in PATH:", shutil.which("tesseract"))
try:
    print("pytesseract sees version:", pytesseract.get_tesseract_version())
except Exception as e:
    print("pytesseract error:", e)
