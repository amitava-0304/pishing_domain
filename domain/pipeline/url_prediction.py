import pandas as pd
import pickle
import numpy as np
from domain.entity.feature_extractor import FeatureExtractor
from domain.predictor import ModelResolver
from domain.utils import load_object
import os,sys
from domain.exception import PishingException
from domain.logger import logging
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import PowerTransformer
from sklearn import preprocessing
from sklearn.preprocessing import MaxAbsScaler
class Prediction_from_link:
    def get_data_transformer_object()->Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='median')
            robust_scaler =  MaxAbsScaler()
            pipeline = Pipeline(steps=[
                    ('Imputer',simple_imputer),
                    ('Normalizer',robust_scaler)


                ])
            return pipeline
        except Exception as e:
            raise PishingException(e, sys)

    def predict(self,link):
        try:
            print("Prediction from link started")
            model_resolver = ModelResolver(model_registry="saved_models")
            transformer = load_object(file_path=model_resolver.get_latest_transformer_path())
            model = load_object(file_path=model_resolver.get_latest_model_path())

            link=link.rstrip(link[-1])
            urls = link.split("\r\n")
            urls = [url.strip() for url in urls]
            print(urls)
            extractor = FeatureExtractor()
            features_from_url_df = extractor.generate_dataframe_from_urls(urls)
            print(features_from_url_df)
            input_feature_names =  features_from_url_df.columns
            input_arr = transformer.transform(features_from_url_df[input_feature_names])
            #transformation_pipleine = Prediction_from_link.get_data_transformer_object()
            #features_from_url_df=features_from_url_df.to_numpy()
            print(features_from_url_df)
            #input_arr=transformation_pipleine.fit_transform(np.array(features_from_url_df).reshape(1, -1))
            #input_arr = preprocessing.normalize(features_from_url_df, axis=0)
            #transforming input features
            
            #input_arr = transformation_pipleine.transform(features_from_url_df[input_feature_names])
            print(input_arr)
            prediction = model.predict(input_arr)
            print(prediction)
            y_pro_phishing = model.predict_proba(input_arr)[0,0]
            y_pro_non_phishing = model.predict_proba(input_arr)[0,1]
            print(y_pro_phishing,y_pro_non_phishing)
            predict=round(y_pro_phishing*100,2)
            predict1=round(y_pro_non_phishing*100,2) 
            logging.info("Prediction Done......")
            logging.info('{}:{}:{}'.format(prediction,predict,predict1))
            return prediction,predict,predict1
        except Exception as e:
            raise PishingException(e, sys)    

'''predict_obj = Prediction_from_link()
urls='https://github.com/'
phishing,pre,pre1 = predict_obj.predict(urls)
print(phishing,pre,pre1)'''