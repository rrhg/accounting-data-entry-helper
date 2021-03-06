# Tesseract OCR
import sys
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from config import STATEMENT_DATA_FILE, STATEMENT_PDF, PATH_TESSERACT_IMAGES_DIR


# If you need to assign tesseract to path
# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\<user>\AppData\Local\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pdf_file = STATEMENT_PDF
print();print('Converting ==> ');print( pdf_file );print()
pdf_file_name = os.path.split(pdf_file)[-1]

output_file = STATEMENT_DATA_FILE

# DO NOT DELETE
# clear the output file # needed bc below we are just appending
f = open(output_file, '+w')
f.close()

page_number = 1

images_dir = PATH_TESSERACT_IMAGES_DIR / pdf_file_name.replace('.pdf','')[0:20]
# TODO avoid images_dir by not saving images. see below
if not os.path.exists(images_dir):
    os.makedirs(images_dir)


pages = convert_from_path(pdf_file)
for page in pages:
    if page_number <= 20:
        image_name = "pg_"+str(page_number)+'_'+ pdf_file_name.replace('.pdf','.jpg')
        image_path = os.path.join(images_dir, image_name)
        # TODO avoid having to save page. maybe f.write(pytesseract.image_to_string(page)) f.write("\n")
        page.save(image_path)

        with open(output_file, 'a+', encoding='utf8') as f:
            f.write("=============================== PAGE " + str(page_number) + " =========================================\n")
            f.write(pytesseract.image_to_string(image_path)+"\n")
            #f.write(unicode(pytesseract.image_to_string(image_path)+"\n")) # TODO why errors ?
            f.write("=============================== ========================= =========================================\n")
        page_number = page_number + 1

print('\n', 'Output text file was saved to ==> ', '\n', output_file, '\n')