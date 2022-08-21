import argparse 
from sys import exit


# python .\acchelper.py invoices -d 25
# python .\acchelper.py pdf2txt
# rerun 'python .\acchelp.py '


def main():
    args = get_args()
    coordinator( args )


def get_args():
    parser = argparse.ArgumentParser() 
    subparser = parser.add_subparsers(dest='command') 

    pdf2txt =    subparser.add_parser('pdf2txt') 
    # pdf2txt.add_argument('-d','--day', type=int, required=True) 
    # pdf2txt.add_argument('-f','--fake_email', type=str, required=True)
    # pdf2txt.add_argument('-c','--client-id', type=str, required=True) 
    # pdf2txt.add_argument('--all-deposits-made', type=str, choices=('yes','no'), required=True) 
    # pdf2txt.add_argument('-q', '--quarter', type=int, choices=(1,2,3,4), required=True) 
    # pdf2txt.add_argument('-y', '--tax-year', type=int, choices=(2021,2022,2023,2024,2025), required=True) 

    args = parser.parse_args() 
    return args


def coordinator( args ):
    # add_client(args)

    if args.command == 'pdf2txt':
        from utils.pdf.pdf2txt import pdf2txt
        pdf2txt()


def rm_pdf_page():
    from utils.pdf.rm_pdf_page import rm_pdf_page
    rm_pdf_page(args)
    exit(0)


# # TODO move to utils
# def pdf2txt(args):

#     import sys
#     import os
#     import time
#     from pathlib import Path
#     import pytesseract
#     from PIL import Image
#     from pdf2image import convert_from_path
#     from utils.clean_img import clean_img
#     from utils.improve_pdf import improve_pdf
#     from config import ( 
#         STATEMENT_DATA_FILE, STATEMENT_PDF,
#         PATH_TESSERACT_IMAGES_DIR, IMPROVED_STATEMENT_PDF,
#         client_name, client)
#     from rich.console import Console
#     red = Console(style="red")
#     yellow = Console(style="yellow")

#     if hasattr(client, 'rm_pdf_page'):
#         from utils.pdf.rm_pdf_page import rm_pdf_page
#         page = client.rm_pdf_page()
#         rm_pdf_page(page, str(STATEMENT_PDF), str(STATEMENT_PDF))
        
#     exit(0)
#     pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#     # So that it knows how to call teserract.
#     # In other machines might be: pytesseract.pytesseract.tesseract_cmd = r'C:\Users\<user>\AppData\Local\Tesseract-OCR\tesseract.exe'


#     improve_pdf( # scale, etc
#         input_path=str(STATEMENT_PDF),
#         output_path=str(IMPROVED_STATEMENT_PDF)
#     )


#     red.print('\nConverting PDF to txt ==> ');print( IMPROVED_STATEMENT_PDF );print()


#     output_file = STATEMENT_DATA_FILE
#     # DO NOT DELETE; clear the output file # needed bc below we are just appending
#     f = open(output_file, '+w')
#     f.close()


#     pdf_file_name = STATEMENT_PDF.name
#     images_dir = PATH_TESSERACT_IMAGES_DIR / pdf_file_name.replace('.pdf','')[0:20]
#     if not os.path.exists(images_dir):
#         os.makedirs(images_dir)
#     # TODO: wait! maybe can not avoid saving images bc we are also cleaning them. Maybe delete them after finish function. see below


#     img_pages = convert_from_path(IMPROVED_STATEMENT_PDF)
#     page_number = 1
#     for page in img_pages:
#         if page_number <= 20:
#             image_name = "pg_"+str(page_number)+'_'+ pdf_file_name.replace('.pdf','.jpg')
#             image_path = os.path.join(images_dir, image_name)

#             # TODO: check if posible clean page in memory & not have to write; old todo: maybe can not avoid saving images bc we are then cleaning them. Maybe delete after finish the convertion to text;  old todo; avoid having to save page. maybe f.write(pytesseract.image_to_string(page)) f.write("\n")

#             page.save(image_path) # write img to this path

#             clean_img(image_path, image_path) # clean some background shadows. Could be improved to clean in memory

#             with open(output_file, 'a+', encoding='utf8') as f:
#                 f.write("=============================== PAGE " + str(page_number) + " =========================================\n")
#                 f.write(pytesseract.image_to_string(image_path)+"\n")
#                 #f.write(unicode(pytesseract.image_to_string(image_path)+"\n")) # TODO why errors ?
#                 f.write("=============================== ========================= =========================================\n")
#             page_number = page_number + 1

#     red.print('\nOutput text file was saved to ==> ')
#     print(output_file, '\n')
#     print()


if __name__ == "__main__":
    main()