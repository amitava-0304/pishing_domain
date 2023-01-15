import json
import os,sys
ROOT_DIR = os.getcwd()
model_directory = "domain"
pipeline_folder = "entity"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, model_directory,pipeline_folder ,"cols_details.json")
class Json_values:

    def __init__(self,file):
        self.file_name = file
    def data(self):

        try:
            with open(self.file_name,'r') as f:
                dic = json.load(f)
                f.close()

            keys,values,description = [],[],[]
            for items in dic['col_name'].keys():
                keys.append(items)
            for items in dic['col_name'].values():
                values.append(items)

            with open(MODEL_CONFIG_FILE_PATH,'r') as f:
                dic = json.load(f)
                f.close()
            for items in dic.values():
                description.append(items)

            return keys,values,description

        except Exception as e:
            raise Exception