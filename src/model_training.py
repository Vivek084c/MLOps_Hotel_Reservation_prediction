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

import mlflow
import mlflow.sklearn

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
            
            lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params["random_state"])
            logger.info("Starting the hyper parameter tunning")

            random_serach = RandomizedSearchCV(
                estimator= lgbm_model,
                param_distributions= self.param_dist,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                verbose = self.random_search_params["verbose"],
                random_state= self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )   

            logger.info("Strating out model tranining ")

            random_serach.fit(xtrain, ytrain)

            logger.info("Hyper parameter tunning completed")
            best_params = random_serach.best_params_
            best_lbgm_model  = random_serach.best_estimator_

            logger.info(f"Best parameters are : {best_params}")

            return best_lbgm_model
        except Exception as e:
            logger.error("Error while training the model : {e}")
            raise CustomException("Error while training the model ", e)
    def evaluate_model(self, model, Xtest, ytest):
        try:
            logger.info("Evaluating the model")

            ypred = model.predict(Xtest)

            accuracy = accuracy_score(ytest, ypred)
            precision = precision_score(ytest, ypred)
            recall = recall_score(ytest, ypred)
            f1 = f1_score(ytest, ypred)

            logger.info(f"accuracy : {accuracy} ")
            logger.info(f"precision : {precision} ")
            logger.info(f"recall : {recall}")
            logger.info(f"f1 : {f1}")

            return {
                "accuracy" : accuracy,
                "precision" : precision,
                "recall" : recall,
                "f1" : f1
            }
        
        except Exception as e:
            logger.error("Error while evaluating the model : {e}")
            raise CustomException("Error while evaluating the model ", e)

    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving the model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
        except Exception as e:
            logger.error("Error while saving the model : {e}")
            raise CustomException("Error while saving the model ", e)
    
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting the model traning pipline")

                logger.info("Starting the logging with mlflow")

                logger.info("logging the training and testing dataset in MLFLOW")
                mlflow.log_artifact(self.train_path, artifact_path = "dataset")
                


                
                x_train,x_test, y_train, y_test = self.load_and_split_data()
                logger.info("loading and spliting done")
                best_lgbm_modle = self.train_lightgbm(x_train, y_train)
                metrices = self.evaluate_model(best_lgbm_modle, x_test, y_test)
                self.save_model(best_lgbm_modle)

                logger.info("Model training successfully complted")
        except Exception as e:
            logger.error("Error while model training pipeline : {e}")
            raise CustomException("Error while model training pipeline", e)
if __name__=="__main__":
    obj = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    obj.run()