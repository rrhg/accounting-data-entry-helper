import shutil
import json
from datetime import datetime


# TODO : fix. This way of adding to Path is old code not used anymore. The comment was ==> this includes parent directory, otherwise can not import config
from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from config import VENDORS_JSON_BACKUP_FILE


def make_bakup(file):
 
    dst = VENDORS_JSON_BACKUP_FILE + '_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '.bak'
    
    try:
        shutil.copyfile(file, dst)
    except IOError:
        print(" Could not copy file: " + file + " to ===>> " + dst)

backup_vendor = make_bakup