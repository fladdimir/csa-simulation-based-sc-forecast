import boto3
import os

if "AWS_DEFAULT_REGION" not in os.environ:
    os.environ["AWS_DEFAULT_REGION"] = "localhost"
if "AWS_ACCESS_KEY_ID" not in os.environ:
    os.environ["AWS_ACCESS_KEY_ID"] = "access_key_id"
if "AWS_SECRET_ACCESS_KEY" not in os.environ:
    os.environ["AWS_SECRET_ACCESS_KEY"] = "secret_access_key"

AWS_ENDPOINT = os.getenv("AWS_ENDPOINT", "http://localhost:4566")

dynamo = boto3.resource("dynamodb", endpoint_url=AWS_ENDPOINT)

TABLE_NAMES = ["state_table", "analytics_table"]


def truncate_table(tableName):
    # https://stackoverflow.com/questions/28521631/empty-a-dynamodb-table-with-boto
    table = dynamo.Table(tableName)
    tableKeyNames = [key.get("AttributeName") for key in table.key_schema]
    ProjectionExpression = ", ".join(tableKeyNames)
    response = table.scan(ProjectionExpression=ProjectionExpression)
    data = response.get("Items")
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ProjectionExpression=ProjectionExpression,
            ExclusiveStartKey=response["LastEvaluatedKey"],
        )
        data.extend(response["Items"])
    with table.batch_writer() as batch:
        for each in data:
            batch.delete_item(Key={key: each[key] for key in tableKeyNames})


for table in TABLE_NAMES:
    truncate_table(table)

print("done.")
