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

red = Console(style="red")
yellow = Console(style="yellow")

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# So that it knows how to call teserract.
# In other machines might be: pytesseract.pytesseract.tesseract_cmd = r'C:\Users\<user>\AppData\Local\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# def pdf2txt( use_temp_dir_for_imgs=True):
def pdf2txt( use_temp_dir_for_imgs=False):
    improve_pdf( # scale, etc
        input_path=str(STATEMENT_PDF),
        output_path=str(IMPROVED_STATEMENT_PDF)
    )
    red.print('\nConverting PDF to txt ==> ');print( IMPROVED_STATEMENT_PDF );print()

    if use_temp_dir_for_imgs:
        with TemporaryDirectory() as images_dir:
            _pdf2txt(IMPROVED_STATEMENT_PDF, images_dir)
    else:
        pdf_file_name = STATEMENT_PDF.name
        images_dir = PATH_TESSERACT_IMAGES_DIR / pdf_file_name.replace('.pdf','')[0:20]
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        # TODO: wait! maybe can not avoid saving images bc we are also cleaning them. Maybe delete them after finish function. see below
        _pdf2txt(IMPROVED_STATEMENT_PDF, images_dir)



def _pdf2txt(improved_pdf, images_dir):
    # list_of_strings = []
    # long_string = ''
    pdf_file_name = STATEMENT_PDF.name
    output_file = STATEMENT_DATA_FILE
    # DO NOT DELETE; clear the output file # needed bc below we are just appending
    f = open(output_file, '+w')
    f.close()

    img_pages = convert_from_path(improved_pdf)
    page_number = 1
    for page in img_pages:
        if page_number <= 20:
            image_name = "pg_"+str(page_number)+'_'+ pdf_file_name.replace('.pdf','.jpg')
            image_path = os.path.join(images_dir, image_name)

            # TODO: check if posible clean page in memory & not have to write; old todo: maybe can not avoid saving images bc we are then cleaning them. Maybe delete after finish the convertion to text;  old todo; avoid having to save page. maybe f.write(pytesseract.image_to_string(page)) f.write("\n")
            # page = crop_pil_img_n_resize(page, .10, .80, .10, .90)
            page = crop_pil_img_n_resize(page, .01, .65, .10, .90)
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


crop_payee_areas_map = [
    {"name":"vida","l":.17,"u":.30,"r":.70, "b":.44},
]

def crop_pil_img_n_resize(              img, left, right, upper, bottom):
    """example: i=crop_pil_img_n_resize(img,  .01,   .65,   .10,    .97)"""
    w, h = img.size
    left = round(w * left ) # 
    right = round(w * right) # 
    upper = round(h * upper) # 
    bottom = round(h * bottom) # 
    area = (left, upper,  right,  bottom)
    new = img.crop(area)
    resize = 1.20
    new = new.resize(( 
        round(w*resize), 
        round(h*resize)
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

