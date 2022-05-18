
#  Work in process !     

# Accounting Data Entry Helper 

Interactively convert bank statement to csv files  
* Create new vendors on the fly
* Create both csv files (vendors & debits/payments or customers & credits/deposits) 
* Customize csv rows for importing transactions to accounting software  
* TODO: explain use cases

## Warning for accountants: requires python knowledge.   
- You have to customize python functions to help the script find debit lines, amounts, files, etc.  
- If a subsequent accounting client have the same bank statement format, then when running new_client.py, you can choose to copy from prior client, to avoid rewriting most functions.   
- Some functions will still need to be customized, for example the bank statement file path.   
-Hopefully in the future, there could be example clients for many statement formats.


Input formats:
- pdf (need to install Tesseract OCR )
- text
- csv(not ready)



#    
# Install & use example with miniconda in Windows.  
1. Install Tesseract (for PDF)
    1. `https://tesseract-ocr.github.io/tessdoc/Installation.html`
1. `conda create --name venv1`
1. `conda activate venv1`
1. `git clone https://github.com/rrhg/accounting-data-entry-helper`
1. `cd accounting-data-entry-helper`
1. Go to `pdf2txt.py` & customize `pytesseract.pytesseract.tesseract_cmd = ...` to include the full path to Tesseract   
1. `pip install -r requirements.txt`
1. `conda install -c conda-forge poppler`
    1. Aparently poppler can't be installed via pip in conda 
1. `python new_client.py`
1. Customize all functions in `accounting_clients/ <client name> /functions/`
    1. The 1st time, u may have to customize all functions.
    1. TODO: link to guide
    1. Export customers & vendors as csv files from your accouting software, get the full path, & include the path in `accounting_clients/ <client name> /functions/files.py`
    1. Add bank statement pdf file full path to `accounting_clients/ <client name> /functions/files.py`
    1. TODO   
1. `python import_vendors.py`
1. `python import_customers.py`
1. Set up is finshed. The next steps are done every month(period)
1. `python pdf2txt.py`   
    1. `pdf2txt.py` will create a text file.  
1. `python debits.py`   
    1. `debits.py` reads data from text file created by `pdf2txt.py`
    1. Interact with the script via the command line to create vendors.csv & debit.csv files that u can import from your accounting software.
    1. TODO: link to guide
    1. Reminder:  
        - clients == our accounting clients  
        - partner(type == customers) == customers to our clients  
        - partner(type == vendors) == vendors to our clients
    1. Vendors & customers are saved
    1. When `debits.py` finds a vendor in a debit/payment line, automatically creates a transaction with vendor code, name, amount, accounts, date, etc. 
1. `python credits.py`
1. Import created csv files from your accounting software
1. TODO:

  
TODO :  
1. Remove \n \r from lines at decoding pdf
1. Tesseract is saving too much images. Find a way to not save images in disk (use only in memory) or delete them after use
1. Fix get one csv row from file & rm folder
1. Option to not add returned checks (credits)
1. Better explanations in example client functions
1. csv to txt
1. Tesseract OCR instructions
1. Clients git backup
1. Model(river library) for learning & predicting vendor/customer per line
   1. For now appears to be working  
   1. Only for vendors/debits. 
   1. Need to pass transaction type to model, so that it does not train on credits.
   1. For now, credits.py is not saving it, so the training from credits is been lost. That is the expected behavior for now.
1. Option to choose different account # than vendor default
1. Tests
1. Github Actions
1. A
1. A
1. A

