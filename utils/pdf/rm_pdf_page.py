from PyPDF2 import PdfFileWriter, PdfFileReader
from rich.console import Console

red = Console(style="red")
# yellow = Console(style="yellow")

def get_numb_of_pages(input_pdf):
    long_pdf = PdfFileReader(input_pdf, strict=False)
    return long_pdf.getNumPages()


def rm_pdf_page(
            page_to_remove = None,
            rm_last_pdf_pages = None,
            in_file_path = '',
            out_file_path = '',
):
    long_pdf = PdfFileReader(in_file_path, strict=False)
    num_of_pages = long_pdf.getNumPages() # 0 indexed
    # pages_to_rm =[]

    if page_to_remove:
        red.print(f"\nRemoving page {page_to_remove} from statement pdf")
        page_to_remove -= 1 # pdf reader use 0 index
        # pages_to_rm.append( page_to_remove )

    if rm_last_pdf_pages:
        red.print(f"\nRemoving last {rm_last_pdf_pages} pages from statement pdf")
        num_of_pages = num_of_pages - rm_last_pdf_pages
        # num_of_pages = num_of_pages[:last_item]
    
    output = PdfFileWriter()

    for num in range(0, num_of_pages): # num_of_pages is not included
        if num != page_to_remove:
            output.addPage(long_pdf.getPage(num))

    with open( out_file_path, "w+b") as f:
        output.write(f)

