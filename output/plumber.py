import pdfplumber
import re
from datetime import datetime

with pdfplumber.open("output.pdf") as pdf:
    first_page = pdf.pages[0]
    text = first_page.extract_text()
    print(text)

