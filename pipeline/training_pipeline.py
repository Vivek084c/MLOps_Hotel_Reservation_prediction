from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataPreprocessor
from src.model_training import ModelTraining
from utils.common_functions import read_yaml
from config.path_config import *

if __name__=="__main__":
    ### data ingestion

    obj = DataIngestion(read_yaml(CONFIG_PATH))
    obj.run()

    ### data processing
    processor = DataPreprocessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()

    ### model training
    obj = ModelTraining(PROCESSED_TRAIN_DATA_PATH, PROCESSED_TEST_DATA_PATH, MODEL_OUTPUT_PATH)
    obj.run()