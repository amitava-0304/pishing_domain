import pandas as pd
from pymongo import MongoClient
from domain.config import mongo_client

if __name__=="__main__":
    # Load csv dataset
    data = pd.read_csv('dataset_full.csv')
    top_features= ['directory_length', 'time_domain_activation', 'length_url',
       'file_length', 'qty_slash_url', 'qty_plus_directory', 'domain_length',
       'qty_vowels_domain', 'qty_asterisk_directory', 'qty_hyphen_directory',
       'qty_dot_domain', 'qty_underline_directory', 'qty_percent_directory',
       'qty_dot_url', 'qty_hyphen_url', 'qty_hyphen_file', 'qty_hyphen_domain',
       'params_length', 'qty_underline_url', 'qty_tld_url', 'qty_plus_params',
       'qty_percent_url', 'qty_equal_params', 'qty_dot_params',
       'qty_percent_params', 'qty_underline_params','phishing']
    data = data[top_features]
    # Connect to MongoDB
    client =  mongo_client

    db = client['pishing_domain']
    collection = db['pishing_detection']
    data.reset_index(inplace=True)
    data_dict = data.to_dict("records")
    # Insert collection
    collection.insert_many(data_dict)
    print("Data Insertion Done....")








