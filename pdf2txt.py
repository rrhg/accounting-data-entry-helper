# Tesseract OCR
import sys
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from config import STATEMENT_DATA_FILE, STATEMENT_PDF


# If you need to assign tesseract to path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\<user>\AppData\Local\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_file = STATEMENT_PDF
print();print('Converting ==> ');print( pdf_file );print()
pdf_file_name = os.path.split(pdf_file)[-1]

output_file = STATEMENT_DATA_FILE
page_number = 1

sub_dir = os.path.join("tesseract_images", pdf_file_name.replace('.pdf','')[0:20] )
# TODO avoid sub_dir by not saving images. see below
if not os.path.exists(sub_dir):
    os.makedirs(sub_dir)

pages = convert_from_path(pdf_file)
for page in pages:
    if page_number <= 20:
        image_name = "pg_"+str(page_number)+'_'+ pdf_file_name.replace('.pdf','.jpg')
        image_path = os.path.join(sub_dir, image_name)
        # TODO avoid having to save page. maybe f.write(pytesseract.image_to_string(page)) f.write("\n")
        page.save(image_path)

        with open(output_file, 'a+', encoding='utf8') as f:
            f.write("=============================== PAGE " + str(page_number) + " =========================================\n")
            f.write(pytesseract.image_to_string(image_path)+"\n")
            #f.write(unicode(pytesseract.image_to_string(image_path)+"\n")) # TODO why errors ?
            f.write("=============================== ========================= =========================================\n")
        page_number = page_number + 1

print();print('Output text file was saved to ==> ');print( output_file );print()