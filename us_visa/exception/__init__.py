import sys
from us_visa.logger import logging

def error_message_detail(error, error_detail):
    """
    Generates a detailed error message including the script name, line number, and error message.

    Args:
        error (Exception): The exception that occurred.
        error_detail (tuple): The traceback details from sys.exc_info().

    Returns:
        str: A formatted error message.
    """
    _, _, exc_tb = error_detail  # Extract the traceback object
    file_name = exc_tb.tb_frame.f_code.co_filename  # Get the file where the error occurred
    error_message = (
        f"Error occurred in python script name [{file_name}] "
        f"line number [{exc_tb.tb_lineno}] error message [{str(error)}]"
    )
    return error_message

class Custom_Exception(Exception):
    def __init__(self, error_message, error_detail):
        """
        Custom exception class for handling errors with detailed information.

        Args:
            error_message (str): A custom error message.
            error_detail (tuple): The traceback details from sys.exc_info().
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
    
    def __str__(self):
        return self.error_message
