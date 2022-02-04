import pickle
import river
from pathlib import Path
import shutil
from datetime import datetime
from utils.strings import clean_line_for_training


class Model:
    def __init__(self, file_path):
        self.MODEL_FILE = file_path
        self.backup_model_file()
        self.model = self.load_model()
        """
        # This helps make sure the model is loading only once & that it includes last period added labels(vendors/customers)
        print('==>  model was loaded (hopefully only once) <==================================================================================================================================================================================================================================================================================================================================================================')    
        print()
        self.print_partners_prob('no line available at module creation')
        """


    def predict_partner(self, line):
        line = clean_line_for_training(line)
        return self.model.predict_one( line ) # river API


    def train_model(self, line, partner_code):
        """ 
        # this helps see how cleaning lines is working
        self.print_cleaned_line(line)
        """
        line = clean_line_for_training(line)
        """ Train 100 times to increase accuracy. Previously it was not enough. This script runs only once for period(month)"""
        for _ in range(100):
            self.model = self.model.learn_one(line, partner_code) # river API
        """
        # this helps see how the model is doing
        self.print_training_info(line, partner_code)
        """


    def load_model(self):
        with open(self.MODEL_FILE, 'rb') as f:
            return pickle.load(f)


    def backup_model_file(self):
        parent_dir = self.MODEL_FILE.parent
        name = self.MODEL_FILE.name
        date = datetime.today().strftime('%Y-%m-%d')
        backup_name = name + '-' + date + '.bak'
        backup_file = parent_dir /  backup_name
        shutil.copy( self.MODEL_FILE, backup_file )


    def print_training_info(self, line, partner_code):
        print()
        print('Trained model with line :')
        print(line)
        print('Trained model with label(partner code) :')
        print(partner_code)
        print()
        self.print_partners_prob(line)


    def save_model(self):
        """ Only once, when script finish- should we ask to save? """        
        a = input('Do you want to save the model trained with the new transactions ?  (y/n)')
        while True:
            if a == 'n' or a == 'N':
                return
            if a == 'y' or a == 'Y':
                with open(self.MODEL_FILE, 'wb') as f:
                    pickle.dump(self.model, f)
                print()
                print('    ==>   model was saved')
                print()
                return


    def print_partners_prob(self, line):
        print('==========================')
        print('Line :')
        print(line)
        print()
        print('Prediction :')
        print(self.predict_partner(line))
        print()
        print('Model Labels, Probabilities & lenght :')
        partners_prob = self.model.predict_proba_one(line) # river API
        print(partners_prob)
        print('len == ', len(partners_prob))
        print()
        print('==========================')


    def print_cleaned_line(line):
        print()
        print('line bf clean :')
        print(line)
        line = clean_line_for_training(line)
        print('line after clean :')
        print(line)
        print()


"""
 this may or may not be used. 
# As of now, we are just instanciating once in config.py, so the same instance is available to all, plus confing has the model file path for current accounting client
# Instantiate the Singleton
# model = _Model()
# https://realpython.com/python-import/#example-singletons-as-modules
"""