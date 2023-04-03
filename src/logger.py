import logging
import os
from datetime import datetime



# creating a variable with name of the log file name using current date time
# using f string and datetime format
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# create a variable with a name for the path for where the log file needs to be saved
# start the name of the file with 'logs'
logs_path = os.path.join(os.getcwd(), 'logs',LOG_FILE)

# create a directory with path even if intermediate structures
# don't exist; exist_ok = True will ensure that it gets added
os.makedirs(logs_path, exist_ok=True)


# creating a variable with the name of 
# this will be used in logging basic config
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# setting up the basic config that sets where file is,
# logging info needs to stored

logging.basicConfig(
    filename = LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,

)


## this is to test if logger module is working
## will be commented otherwise

#if __name__ == "__main__":
#    logging.info("Logging has started")

# it will be important to see if there can be just one log file
