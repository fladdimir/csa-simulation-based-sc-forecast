import json
import logging
import os
from typing import Union

from model.blocks.order import Order


class LoggingQueue:
    def send_message(
        self,
        MessageBody="",
        MessageAttributes={},
        MessageGroupId="MessageGroupId",
    ):
        logging.info(
            f"sent message to log_queue - body: {MessageBody}, attributes: {json.dumps(MessageAttributes)}, groupId: {MessageGroupId}"
        )


class KinesisQueue:
    def __init__(self, client, stream_name):
        self.client = client
        self.stream_name = stream_name

    def send_message(
        self,
        MessageBody="",
        MessageAttributes={},
        MessageGroupId="MessageGroupId",
    ):
        self.client.put_record(
            StreamName=self.stream_name, Data=MessageBody, PartitionKey=MessageGroupId
        )


queue = LoggingQueue()


def connect():
    import boto3

    if "AWS_DEFAULT_REGION" not in os.environ:
        os.environ["AWS_DEFAULT_REGION"] = "localhost"
    if "AWS_ACCESS_KEY_ID" not in os.environ:
        os.environ["AWS_ACCESS_KEY_ID"] = "access_key_id"
    if "AWS_SECRET_ACCESS_KEY" not in os.environ:
        os.environ["AWS_SECRET_ACCESS_KEY"] = "secret_access_key"

    endpoint = os.getenv("AWS_ENDPOINT", "http://localhost:4566")
    stream_name = os.getenv("ORDER_EVENT_STREAM_NAME", "order_event_stream")

    client = boto3.client("kinesis", endpoint_url=endpoint)
    global queue
    queue = KinesisQueue(client, stream_name)


def update(
    order_name: str,
    attribute: str,
    value: Union[float, int, str],
    t: float,
    order: Order,
):
    data = {
        "order_name": order_name,
        "attribute": attribute,
        "value": value,
        "timestamp": t,
    }
    serialized = json.dumps(data)
    logging.info(f"sending update: {serialized}")
    queue.send_message(
        MessageBody=serialized,
        MessageAttributes={},
        MessageGroupId=order.name,  # id
    )
