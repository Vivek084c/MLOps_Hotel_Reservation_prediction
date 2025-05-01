import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataPreprocessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir

        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(processed_dir)
        
    def preprocess_data(self, df):
        try:
            logger.info("Starting the data processing step")

            logger.info("Dropping the columns")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_col = self.config["data_processing"]["categorical_columns"]
            num_col = self.config["data_processing"]["numerical_columns"]

            logger.info("Applying lable encodign")
            lb = LabelEncoder()
            mapping = {}

            for col in cat_col:
                df[col]=lb.fit_transform(df[col])
                #storing the mappings i.e the label and thr corrospoinding mapping 
                mapping[col] = {label: code for label, code in zip(lb.classes_ , lb.transform(lb.classes_))}

            logger.info("Labels mapping are : ")
            for col, mapp in mapping.items():
                logger.info(f"{col} : {mapp}")

            logger.info("preforming skewness handling ")
            skewness_thresh = self.config["data_processing"]["skewness_threshol"]
            skewness = df[num_col].apply(lambda x : x.skew())

            for col in skewness[skewness>skewness_thresh].index:
                df[col] = np.log1p(df[col])

            return df
        except Exception as e:
            logger.error(f"Error during preprocess step {e}")
            raise CustomException("Error in data preprocessing", e)
    def balance_data(self, df):
        try:
            logger.info("Handling the imbalance data")
            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            #appying smot technique
            smt = SMOTE(random_state=42)
            X_res, y_res= smt.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_res, columns=X.columns)
            balanced_df["booking_status"] = y_res

            logger.info("Data balance successfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error during balancing step {e}")
            raise CustomException("Error in data balancing", e)
        
    def selecte_features(self, df):
        try:
            logger.info("Started feature selection")

            X = df.drop(columns=["booking_status"])
            y = df["booking_status"]

            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame(
                {
                    'features' : X.columns,
                    'importance' : feature_importance
                }
            )
            # feature_importance_df.sort_values(by="importance", ascending=False)
            top_features = feature_importance_df.sort_values(by="importance", ascending=False)
            num_features = self.config["data_processing"]["no_of_feaatures"]
            top_10 = top_features["features"].head(num_features).values
            logger.info(f"Features selected : {num_features}")
            top_10_df = df[top_10.tolist() + ["booking_status"]]

            logger.info("Feature selection completed ")
            return top_10_df

        except Exception as e:
            logger.error(f"Error during feature selection step {e}")
            raise CustomException("Error in feature selection", e)

    def save_data(self, df, path):
        try:
            logger.info(f"Saving the dataframe at {path}")
            df.to_csv(path, index=False)
            logger.info(f"Data saved successfully at : {path}")

        except Exception as e:
            logger.error(f"Error during data saving step{e}")
            raise CustomException("Error in data saving", e)            

    def process(self):
        try:
            logger.info("Loading data from RAW directory")
            
            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.selecte_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed")


        except Exception as e:
            logger.error(f"Error in processing pipeline completed{e}")
            raise CustomException("Error in processing pipeline completed", e)            

if __name__=="__main__":
    processor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()


