import os
from domain.entity.feature_extractor import FeatureExtractor

from domain.logger import logging
from domain.exception import PishingException

from domain.utils import load_object

import os,sys
from typing import List


class PhishingEstimator:
    """class responsible formaking final predictions
    """
    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise PishingException(e, sys)
        
    def get_latest_model_path(self):
        try:
            folder_names = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_names)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise PishingException(e, sys)
        
    def predict(self,url_list:List[str]):
        try:
            model_in_production_path = self.get_latest_model_path() ## The latest model is the model in production
            extractor = FeatureExtractor()
            features_from_url_df = extractor.generate_dataframe_from_urls(url_list)
            model = load_object(model_in_production_path)
            
            return model.predict(features_from_url_df)
            
        except Exception as e:
            raise PishingException(e, sys)
        
    def predict_proba(self,url_list:List[str]):
        try:
            model_in_production_path = self.get_latest_model_path() ## The latest model is the model in production
            extractor = FeatureExtractor()
            features_from_url_df = extractor.generate_dataframe_from_urls(url_list)
            model = load_object(model_in_production_path)
            
            return model.predict_proba(features_from_url_df)
            
        except Exception as e:
            raise PishingException(e, sys)
        