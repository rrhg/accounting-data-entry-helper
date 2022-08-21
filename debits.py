import time
# import typer
from utils.csv2.create_output_csv_file import create_debits_csv_file
from transactions.compare_sums_of_transactions import compare_sums_of_debits
from transactions.get_all import get_all_debits
from config import model, client, STATEMENT_PDF
# app = typer.Typer()

# @app.command()
# def debits(model_logs: str = False):
def debits():

    # from PIL import Image   
    # from utils.images import ResizeImage
    # img = r"C:\Users\r\OneDrive - H&J Accounting\Documents\Ricky\accounting-data-entry-helper\accounting_clients\hsdv\cks_images\imgs of payees\check_0.jpg"
    # img = Image.open(img)
    # print(img.size) # 370, 43
    # img.show()
    # # res = ResizeImage()
    # re_img = img.resize((600,100))
    # re_img.show()


    """
        YA HIZE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            LOOK FOR STATEMENT IN SAME FOLDER I PUT WHEN DOWNLOAD FROM GMAIL
            ----- FALTA ARREGLAR OTROS CLIENTES FUNCTIONS FILES ....
            SAVE EACH CHECK Image

        AHORA:
            QUE CUANDO PREGUNTE POR CK VENDOR ; HAGA CHECK.SHOW() !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """



    # cks = cks_images.get_from_statement_pdf(use_textract=False)
    # print()
    # for ck in cks:
    #     print(f"ck number: {ck.number}")
    #     print(f"payee_txt_hugginface: {ck.payee_txt_hugginface}")
    #     print(f"payee_txt_textract: {ck.payee_txt_textract}")
    #     print()
        
    # cks_images.delete_all()
    # print('deleting & waiting 15 secs')
    # time.sleep(15)


    all_debits = get_all_debits()

    # print(all_debits)

    compare_sums_of_debits( all_debits )

    create_debits_csv_file( all_debits )

    model.save_model()

if __name__ == '__main__':
    # app()
    debits()
