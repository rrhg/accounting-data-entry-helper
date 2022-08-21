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
    PATH_TESSERACT_IMAGES_DIR, IMPROVED_STATEMENT_PDF,
    client_name, client)
from rich.console import Console
from settings import tesseract_path
from tempfile import TemporaryDirectory


def pdf2jpg_images(pdf):

    img_pages = convert_from_path(improved_pdf)

    page_number = 1
    for page in img_pages:
        if page_number <= 20:
            image_name = "pg_"+str(page_number)+'_'+ pdf_file_name.replace('.pdf','.jpg')
            image_path = os.path.join(images_dir, image_name)

            # TODO: check if posible clean page in memory & not have to write; old todo: maybe can not avoid saving images bc we are then cleaning them. Maybe delete after finish the convertion to text;  old todo; avoid having to save page. maybe f.write(pytesseract.image_to_string(page)) f.write("\n")

            page.save(image_path) # write img to this path

            clean_img(image_path, image_path) # clean some background shadows. Could be improved to clean in memory

            with open(output_file, 'a+', encoding='utf8') as f:
                text = "=========== PAGE " + str(page_number) + " ======\n"
                f.write(text)
                # long_string += text

                tesse_conf = (
                    #   r'--load_system_dawg 0' # nothing printed to txt file
                    # + r' --load_freq_dawg 0' # nothing printed to txt file
                    r'--psm 6' # Assume a single uniform block of text
                )

                text = pytesseract.image_to_string(image_path, config=tesse_conf)+"\n"
                #f.write(unicode(pytesseract.image_to_string(image_path)+"\n")) # TODO why errors ?

                f.write(text)
                # long_string += text

                # f.write("======= ========================= ==============\n")
            page_number = page_number + 1


    red.print('\nOutput text file was saved to ==> ')
    print(output_file, '\n')
    print()
    # list_of_strings = long_string.split('\n')
    # return list_of_strings # maybe not needed bc we always want to be able to see the text file for debuging


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

