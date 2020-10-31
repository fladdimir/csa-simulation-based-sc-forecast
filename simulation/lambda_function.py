import os

import boto3

from simulation_forecast.forecasting import forecast

"""
environment variables:
    export AWS_ENDPOINT=http://localhost:4566
    export TABLE_NAME=Books
    # for direct local execution:
    export AWS_DEFAULT_REGION=localhost
    export AWS_ACCESS_KEY_ID=access_key_id
    export AWS_SECRET_ACCESS_KEY=secret_access_key
"""

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
if "AWS_DEFAULT_REGION" not in os.environ:
    os.environ["AWS_DEFAULT_REGION"] = "localhost"
if "AWS_ACCESS_KEY_ID" not in os.environ:
    os.environ["AWS_ACCESS_KEY_ID"] = "access_key_id"
if "AWS_SECRET_ACCESS_KEY" not in os.environ:
    os.environ["AWS_SECRET_ACCESS_KEY"] = "secret_access_key"


# localstack specific url processing
LOCALSTACK_HOSTNAME = "LOCALSTACK_HOSTNAME"
if LOCALSTACK_HOSTNAME in AWS_ENDPOINT:
    AWS_ENDPOINT = AWS_ENDPOINT.replace(
        LOCALSTACK_HOSTNAME, os.getenv(LOCALSTACK_HOSTNAME)
    )

ANALYTICS_TABLE_NAME = os.getenv("ANALYTICS_TABLE_NAME", "analytics_table")
STATE_TABLE_NAME = os.getenv("STATE_TABLE_NAME", "state_table")

dynamodb = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT)

analytics_table = dynamodb.Table(ANALYTICS_TABLE_NAME)
state_table = dynamodb.Table(STATE_TABLE_NAME)


def handler(event, context):
    forecast(state_table, analytics_table)
