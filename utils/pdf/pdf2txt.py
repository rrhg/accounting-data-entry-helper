import sys
import os
import time
from pathlib import Path
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
from utils.clean_img import clean_img
from utils.pdf.improve_pdf import improve_pdf
from config import ( 
    STATEMENT_DATA_FILE, STATEMENT_PDF,
    # PATH_TESSERACT_IMAGES_DIR, IMPROVED_STATEMENT_PDF,# not using improved pdf anymore, now we use the same pdf but only the images are cropped, resized & cleaned
    PATH_TESSERACT_IMAGES_DIR,
    client_name, client)
from settings import tesseract_path
from tempfile import TemporaryDirectory

from rich.console import Console
red = Console(style="red")
yellow = Console(style="yellow")

pytesseract.pytesseract.tesseract_cmd = tesseract_path


def pdf2txt( use_temp_dir_for_imgs=False):
    # DO NOT USE TEMP DIR BC WE STILL HAVE TO LOOK AT IMAGES TO CHECK IF CROP & RESIZE ARE OK FOR EACH CLIENT

    red.print('\nConverting PDF to txt ==> ');print( STATEMENT_PDF );print()

    if use_temp_dir_for_imgs:
        with TemporaryDirectory() as images_dir:
            _pdf2txt(STATEMENT_PDF, images_dir)
    else:
        pdf_file_name = STATEMENT_PDF.name
        images_dir = PATH_TESSERACT_IMAGES_DIR / pdf_file_name.replace('.pdf','')[0:20]
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)

        _pdf2txt(STATEMENT_PDF, images_dir)


def _pdf2txt(pdf_path, images_dir):
    pdf_file_name = STATEMENT_PDF.name
    output_file = STATEMENT_DATA_FILE

    # DO NOT DELETE; clear the output file # needed bc below we are just appending
    f = open(output_file, '+w')
    f.close()

    img_pages = convert_from_path(pdf_path)

    page_number = 1
    for page in img_pages:
        if page_number <= 20:
            image_name = "pg_"+str(page_number)+'_'+ pdf_file_name.replace('.pdf','.jpg')
            image_path = os.path.join(images_dir, image_name)

            page = crop_pil_img_n_resize(page)

            page.save(image_path) # write img to this path
            clean_img(image_path, image_path) # clean some background shadows. Could be improved to clean in memory

            with open(output_file, 'a+', encoding='utf8') as f:
                text = "=========== PAGE " + str(page_number) + " ======\n"
                f.write(text)

                tesse_conf = (
                    #   r'--load_system_dawg 0' # nothing printed to txt file
                    # + r' --load_freq_dawg 0' # nothing printed to txt file
                    r'--psm 6' # Assume a single uniform block of text
                )
                text = pytesseract.image_to_string(image_path, config=tesse_conf)+"\n"

                f.write(text)

            page_number = page_number + 1

    red.print('\nOutput text file was saved to ==> ')
    print(output_file, '\n')


def crop_pil_img_n_resize(img):
    scale,left,right,upper,bottom = client.scale_bank_pdf_to()
    w, h = img.size
    left = round(w * left ) # 
    right = round(w * right) # 
    upper = round(h * upper) # 
    bottom = round(h * bottom) # 
    area = (left, upper,  right,  bottom)
    new = img.crop(area)
    new = new.resize(( 
        round(w*scale), 
        round(h*scale)
        ))
    return new


def extract_lines_of_txt_from_searchable_pdf(pdf_path):

    # brake lines
    # from pdfminer.high_level import extract_text
    # text = extract_text(str(pdf_path))
    # print(text)


    import sys
    sys.exit()

    # ism issing some lines atthe bottom of page. like 3 or 4 lines
    import pdfplumber
    with pdfplumber.open(str(pdf_path)) as pdf:
        # first_page = pdf.pages[0]
        for p in pdf.pages:
            # print(p.extract_text()  )
            for l in p.lines:
                print(l)
        # print(first_page.extract_text())


    # text = []
    # tables = camelot.read_pdf(str(pdf_path), strip_text='\n') #address of file location
    # df = tables[0].df
    # for r in df.index:
    #     print(df[:][r])
    # for t in tables:
    #     print(t.df)

    # tables.export('foo.csv', f='csv', compress=True) # json, excel, html, markdown, sqlite
    # tables[0]
    # <Table shape=(7, 7)>
    # print(tables[0].parsing_report)

    # PyPDF2 is giving too much errors
    # from PyPDF2 import PdfReader
    # with open(pdf_path, 'rb') as pdfFileObj:
    #     reader = PdfReader(pdfFileObj)
    #     # reader = PdfReader(pdf_path)
    #     if reader.isEncrypted:
    #         reader.decrypt('')
    #     # number_of_pages = len(reader.pages)
    #     # page = reader.pages[0]
    #     page = reader.getPage(0)
    #     # pdfFileObj.close()
    #     # for p in reader.pages:
    #     #     text.extend = p.extract_text().split('\n')
    #     text = page.extract_text()
    #     return text

