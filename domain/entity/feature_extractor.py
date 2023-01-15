from domain.utils import read_yaml_file
from domain.constants import *
from typing import List
import pandas as pd
import numpy as np
import datetime 
import whois
from domain.logger import logging
## This script is responsible for generating datframe out of some raw url

config  = read_yaml_file(CONFIG_FILE_PATH)
features = config[DATA_INGESTION_CONFIG_KEY][DATA_INGESTION_TOP_FEATURES_KEY]
features.pop()



class FeatureExtractor:
    def __init__(self, columns = features):
       self.columns = columns
    
    @staticmethod
    def __extract_domain(url):
        try:
            return url.split("//")[1].split("/")[0]
        except Exception as e:
            return ""
    
    @staticmethod
    def __extract_directory(url):
        try:
            return url.split("//")[1].split("/")[1]
        except Exception as e:
            return ""
        
    @staticmethod
    def __extract_file(url):
        try:
            return url.split("//")[1].split("/")[2]
        except Exception as e:
            return ""
    
    @staticmethod
    def __extract_parameters(url):
        try:
            return url.split("//")[1].split("/")[3]
        except Exception as e:
            return ""
    
    @staticmethod
    def __extract_directory_length(directory):
        if directory == "":
            return -1
        return len(directory)
    
    @staticmethod
    def __extract_time_domain_activation(url):
        try:
            res = whois.whois(url)
            day_created = res['creation_date'][0]
            days= (datetime.datetime.now()-day_created).days
            return days
        except:
            return -1
    
    
    @staticmethod
    def __extract_length_url(url):
        return len(url)
    
    @staticmethod
    def __extract_file_length(file):
        
        if file == "":
            return -1
        
        return len(file)
    
    @staticmethod
    def __extract_qty_slash_url(url):
        return url.count("/")
    
    @staticmethod
    def __extract_qty_plus_directory(directory):
        return directory.count("+")
    
    @staticmethod
    def __extract_qty_vowels_domain(domain):
        qty_vowels_domain = 0
        for i in domain:
            if i in {"a","e","i","o","u"}:
                qty_vowels_domain+=1
        
        return qty_vowels_domain
    
    @staticmethod
    def __extract_qty_asterik_directory(directory):
        if directory == "":
            return -1
        
        return directory.count("*")
    
    @staticmethod
    def __extract_qty_hyphen_directory(directory):
        if directory == "":
            return  -1
        return directory.count("-")
    
    @staticmethod
    def __extract_qty_underline_directory(directory):
        if directory == "":
            return -1
        
        return directory.count("_")
    
    
    @staticmethod
    def __extract_qty_percent_directory(directory):
        if directory == "":
            return -1
        return directory.count("%")
    
    
    @staticmethod
    def __extract_qty_hyphen_file(file):
        if file == "":  
            return -1
        return file.count("-")
    
    @staticmethod
    def __extract_params_length(parameters):
        if parameters == "":
            return -1
        return len(parameters)
    
    @staticmethod
    def __extract_qty_tld_url(domain):
        try:
            
            top_level_domain = domain.split(".")[-1]
            
            return len(top_level_domain)

        except Exception as e:
            return 1
    
    @staticmethod
    def __extract_qty_plus_params(parameters):
        if parameters == "":
            return -1
        
        return parameters.count("+")
    
    @staticmethod
    def __extract_qty_equal_params(parameters):
        if parameters == "":
            return -1
        
        return parameters.count("=")
    
    @staticmethod
    def __extract_qty_dot_params(parameters):
        if parameters == "":    
            return -1
        
        return parameters.count(".")
    
    
    @staticmethod
    def __extract_qty_percent_params(parameters):
        if parameters == "":
            return -1
        return parameters.count("%")
    
    @staticmethod
    def __extract_qty_underline_params(parameters):
        if parameters == "":
            return -1
        return parameters.count("_")
    
    def __generate_dataframe_from_url(self, url:str):
        
        domain = FeatureExtractor.__extract_domain(url)
        directory = FeatureExtractor.__extract_directory(url)
        file = FeatureExtractor.__extract_file(url)
        parameters = FeatureExtractor.__extract_parameters(url)
        
        
        directory_length = FeatureExtractor.__extract_directory_length(directory)
        time_domain_activation = FeatureExtractor.__extract_time_domain_activation(url)
        length_url = FeatureExtractor.__extract_length_url(url)
        file_length = FeatureExtractor.__extract_file_length(file)
        qty_slash_url = FeatureExtractor.__extract_qty_slash_url(url)
        qty_plus_directory = FeatureExtractor.__extract_qty_plus_directory(directory)
        
        domain_length = len(domain)
        qty_vowels_domain = FeatureExtractor.__extract_qty_vowels_domain(domain)
        qty_asterisk_directory = FeatureExtractor.__extract_qty_asterik_directory(directory)
        qty_hyphen_directory = FeatureExtractor.__extract_qty_hyphen_directory(directory)
        
        qty_dot_domain = domain.count(".")
        qty_underline_directory = FeatureExtractor.__extract_qty_underline_directory(directory)
        qty_percent_directory = FeatureExtractor.__extract_qty_percent_directory(directory)
        
        qty_dot_url = url.count(".")
        qty_hyphen_url = url.count("-")
        qty_hyphen_file = FeatureExtractor.__extract_qty_hyphen_file(file)
        
        
        qty_hyphen_domain = domain.count("-")
        qty_params_length = FeatureExtractor.__extract_params_length(parameters)
        
        qty_underline_url = url.count("_")
        qty_tld_url = FeatureExtractor.__extract_qty_tld_url(domain)
        
        qty_plus_params = FeatureExtractor.__extract_qty_plus_params(parameters)
        
        
        qty_percent_url = url.count("%")
        
        
        qty_equal_params = FeatureExtractor.__extract_qty_equal_params(parameters)
        qty_dot_params = FeatureExtractor.__extract_qty_dot_params(parameters)
        
        qty_percent_params = FeatureExtractor.__extract_qty_percent_params(parameters)
        qty_underline_params = FeatureExtractor.__extract_qty_underline_params(parameters)
        
        df_row_array = np.array([directory_length, time_domain_activation, length_url,
                  file_length, qty_slash_url, qty_plus_directory, 
                  domain_length, qty_vowels_domain, qty_asterisk_directory,qty_hyphen_directory,
                  qty_dot_domain, qty_underline_directory, qty_percent_directory,
                  qty_dot_url, qty_hyphen_url, qty_hyphen_file, qty_hyphen_domain, qty_params_length,
                  qty_underline_url,qty_tld_url, qty_plus_params,qty_percent_url,qty_equal_params, 
                  qty_dot_params, qty_percent_params, qty_underline_params])
        
        
        
        df_row = pd.DataFrame(df_row_array.reshape(1,-1), columns = self.columns)
        
        # print(df_row_array)
        return df_row
        
    
    def generate_dataframe_from_urls(self, url_list:List[str]):
        df = pd.DataFrame(columns=self.columns)
        for url in url_list:
            df_row = self.__generate_dataframe_from_url(url)
            df = pd.concat([df, df_row])
            logging.info("Feature Extraction Done.......")
        return df