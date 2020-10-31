import sys

sys.path.append(".")
import logging

logging.getLogger().setLevel("INFO")

import lambda_function

lambda_function.handler(None, None)
