import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_output_path = model_output_path

        self.param_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS

    def load_and_split_data(self):
        """
        Loading the preprocessed data from the given directory
        """
        try:
            logger.info(f"Loading data from : {self.train_path}")
            train_df = load_data(self.train_path)

            logger.info(f"Loading data from : {self.test_path}")
            test_df = load_data(self.test_path)

            x_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            x_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data Spliting successfull for model traininng")

            return x_train,x_test, y_train, y_test
        except Exception as e:
            logger.info(f"Error in loading data for model {e}")
            raise CustomException("Error in loading data for model training", e)
        
    def train_lightgbm(self, xtrain, ytrain):
        try:
            logger.info("Initilising the Model")
            lgbm_model = 


    

