# this allows interacting with Python runtime
# here it is mainly useful for getting the exception
import sys
from src.logger import logging


def error_message_detail(error, error_detail:sys):
    '''
    this function takes in two arguments, error and error_detail from Exception class
    and then creates error_message
    error_message consists of file, line and error
    '''
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail = error_detail)

    def __str__(self):
        return self.error_message

## to test exception.py
## this will be commented otherwise


#if __name__ == "__main__":
#
#    try:
#        a = 1/0
#    except Exception as e:
#        logging.info("Divide by Zero")
#        raise CustomException(e, sys)
   