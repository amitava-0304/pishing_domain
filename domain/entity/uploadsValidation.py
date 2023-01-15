import pandas as pd
import os

import json

class Validation:
    def __init__(self,file,location,jsonn = "NULL"):
        self.file = file
        self.name = location
        self.location = "./"+location+"/" + str(file.filename)
        self.jsonn = jsonn


    def save(self):
        try:
            self.file.save(os.path.join(self.name,self.file.filename))
        except Exception:
            raise Exception


    def checkFile(self):
        try:
            data = pd.read_csv(self.location)

            with open(self.jsonn,'r') as f:
                dic = json.load(f)
                f.close()
            numberofcols = dic['NumberofColumns']

            if(data.shape[1] != numberofcols):
                os.remove(self.location)
                return numberofcols,"Number of columns are not equal",True

                # raise ValueError("Number of Columns are not equal")
            col_name = dic['col_name']
            print("Checking passed")
            return numberofcols,col_name,False

        except UnicodeDecodeError:
            print("are we here??22")
            os.remove(self.location)
            raise UnicodeDecodeError

        except ValueError:
            raise ValueError('Number of Columns are not equal')

        # except Exception:
        #     raise Exception


