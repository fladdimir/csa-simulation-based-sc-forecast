import base64
import json
import logging
import os
from decimal import Decimal

import boto3

"""
environment variables:
    export AWS_ENDPOINT=http://localhost:4566
    export TABLE_NAME=table_xy
    # for direct local execution:
    export AWS_DEFAULT_REGION=localhost
    export AWS_ACCESS_KEY_ID=access_key_id
    export AWS_SECRET_ACCESS_KEY=secret_access_key
"""

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
TABLE_NAME = os.getenv("TABLE_NAME")

# localstack specific url processing
LOCALSTACK_HOSTNAME = "LOCALSTACK_HOSTNAME"
if LOCALSTACK_HOSTNAME in AWS_ENDPOINT:
    localstack_hostname = os.getenv(LOCALSTACK_HOSTNAME, "localstack_main")
    AWS_ENDPOINT = AWS_ENDPOINT.replace(LOCALSTACK_HOSTNAME, localstack_hostname)


dynamodb = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT)
table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    datas = [record["kinesis"]["data"] for record in event["Records"]]
    bodies = [base64.b64decode(data) for data in datas]
    deserialized_bodies = [json.loads(body) for body in bodies]
    for data in deserialized_bodies:
        update_item(data)


def update_item(item: dict):
    # e.g.: data = {"order_name": "entity_1", "attribute": "time_of_acceptance", "value": 0.0, "timestamp": 0.0}
    logging.info(f"updating item: {item}")
    table.update_item(
        Key={"order_name": item["order_name"]},
        UpdateExpression=f"SET {item['attribute']} = :value, last_update = :ts",
        ExpressionAttributeValues={
            ":value": Decimal(item["value"]),
            ":ts": Decimal(item["timestamp"]),
        },
    )
