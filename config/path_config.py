import os


################################## DATA_INGESTION ##################################

RAW_DIR = "artifacts/raw"
RAW_FILEPATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH =  "config/config.yaml"