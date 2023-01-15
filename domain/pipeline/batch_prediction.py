from domain.exception import PishingException
from domain.logger import logging
from domain.predictor import ModelResolver
import pandas as pd
from domain.utils import load_object
import os,sys
from datetime import datetime
PREDICTION_DIR="prediction"

import numpy as np
def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info(f"Creating model resolver object")
        model_resolver = ModelResolver(model_registry="saved_models")
        logging.info(f"Reading file :{input_file_path}")
        df = pd.read_csv(input_file_path)
        top_features= ['directory_length', 'time_domain_activation', 'length_url',
            'file_length', 'qty_slash_url', 'qty_plus_directory', 'domain_length',
            'qty_vowels_domain', 'qty_asterisk_directory', 'qty_hyphen_directory',
            'qty_dot_domain', 'qty_underline_directory', 'qty_percent_directory',
            'qty_dot_url', 'qty_hyphen_url', 'qty_hyphen_file', 'qty_hyphen_domain',
            'params_length', 'qty_underline_url', 'qty_tld_url', 'qty_plus_params',
            'qty_percent_url', 'qty_equal_params', 'qty_dot_params',
            'qty_percent_params', 'qty_underline_params','phishing']
        df = df[top_features]
        #df.replace({"na":np.NAN},inplace=True)
        #validation
        
        logging.info(f"Loading transformer to transform dataset")
        transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
        
        input_feature_names =  list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_feature_names])

        logging.info(f"Loading model to make prediction")
        model = load_object(file_path=model_resolver.get_latest_model_path())
        prediction = model.predict(input_arr)
        
        logging.info(f"Target encoder to convert predicted column into categorical")
        #target_encoder = load_object(file_path=model_resolver.get_latest_target_encoder_path())

        cat_prediction = prediction

        df["prediction"]=prediction
        df["cat_pred"]=cat_prediction


        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise PishingException(e, sys)
