provider "aws" {
  access_key                  = "mock_access_key"
  region                      = "us-east-1"
  s3_force_path_style         = true
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  endpoints {
    apigateway     = "http://localhost:4566"
    cloudformation = "http://localhost:4566"
    cloudwatch     = "http://localhost:4566"
    dynamodb       = "http://localhost:4566"
    ec2            = "http://localhost:4566"
    es             = "http://localhost:4566"
    firehose       = "http://localhost:4566"
    iam            = "http://localhost:4566"
    kinesis        = "http://localhost:4566"
    lambda         = "http://localhost:4566"
    route53        = "http://localhost:4566"
    redshift       = "http://localhost:4566"
    s3             = "http://localhost:4566"
    secretsmanager = "http://localhost:4566"
    ses            = "http://localhost:4566"
    sns            = "http://localhost:4566"
    sqs            = "http://localhost:4566"
    ssm            = "http://localhost:4566"
    stepfunctions  = "http://localhost:4566"
    sts            = "http://localhost:4566"
  }
}

# locals

locals {
  lambda_ingest_zip_path    = "../ingest_to_dynamodb/function.zip"
  lambda_analytics_zip_path = "../simulation/function.zip"
}

# ----------------------------------------
# capture state

# dynamodb
resource "aws_dynamodb_table" "state_table" {
  name           = "state_table"
  read_capacity  = 50
  write_capacity = 50
  hash_key       = "order_name"
  attribute {
    name = "order_name"
    type = "S"
  }
  stream_enabled   = true
  stream_view_type = "KEYS_ONLY"
}

# kinesis stream
resource "aws_kinesis_stream" "order_event_stream" {
  name        = "order_event_stream"
  shard_count = 5
}

# iam role
resource "aws_iam_role" "iam_role_for_lambda" {
  name               = "iam_role_for_lambda"
  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
      ]
    }
EOF
}

# dynamodb iam access policy for role
resource "aws_iam_role_policy" "dynamodb-lambda-policy" {
  name   = "dynamodb_lambda_policy"
  role   = aws_iam_role.iam_role_for_lambda.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "${aws_dynamodb_table.state_table.arn}"
    }
  ]
}
EOF
  # (additional restrictions possible)
}

# lambda function
resource "aws_lambda_function" "lambda_ingest" {
  filename         = local.lambda_ingest_zip_path
  function_name    = "lambda_ingest"
  role             = aws_iam_role.iam_role_for_lambda.arn
  handler          = "lambda_function.handler" # python module_name.function_name
  source_code_hash = filebase64sha256(local.lambda_ingest_zip_path)
  runtime          = "python3.8"
  timeout          = 30
  environment {
    variables = {
      TABLE_NAME   = "state_table",
      AWS_ENDPOINT = "http://LOCALSTACK_HOSTNAME:4566" # will be replaced by LOCALSTACK_HOSTNAME environment variable in lambda script
    }
  }
}

# lambda event mapping
resource "aws_lambda_event_source_mapping" "order_update_event" {
  event_source_arn  = aws_kinesis_stream.order_event_stream.arn
  function_name     = aws_lambda_function.lambda_ingest.arn
  starting_position = "LATEST"
  batch_size        = 1
}

# ---------------------------------------------------------------------------------------------------------------
# create forecast

# dynamodb table
resource "aws_dynamodb_table" "analytics_table" {
  name           = "analytics_table"
  read_capacity  = 50
  write_capacity = 50
  hash_key       = "result_name"
  attribute {
    name = "result_name"
    type = "S"
  }
}

# iam role
resource "aws_iam_role" "iam_role_for_lambda_analytics" {
  name               = "iam_role_for_lambda_analytics"
  assume_role_policy = <<EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Effect": "Allow",
          "Sid": ""
        }
      ]
    }
EOF
}

# dynamodb iam access policy for role
resource "aws_iam_role_policy" "dynamodb_lambda_policy_analytics" {
  name   = "dynamodb_lambda_policy_analytics"
  role   = aws_iam_role.iam_role_for_lambda_analytics.id
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "${aws_dynamodb_table.analytics_table.arn}"
    }
  ]
}
  EOF
}

# lambda function
resource "aws_lambda_function" "lambda_analytics" {
  filename         = local.lambda_analytics_zip_path
  function_name    = "lambda_analytics"
  role             = aws_iam_role.iam_role_for_lambda_analytics.arn
  handler          = "lambda_function.handler" # python module_name.function_name
  source_code_hash = filebase64sha256(local.lambda_analytics_zip_path)
  runtime          = "python3.8"
  timeout          = 600
  environment {
    variables = {
      TABLE_NAME   = "analytics_table",
      AWS_ENDPOINT = "http://LOCALSTACK_HOSTNAME:4566" # will be replaced by LOCALSTACK_HOSTNAME environment variable in lambda script
    }
  }
}

# lambda event mapping
resource "aws_lambda_event_source_mapping" "state_table_stream_event" {
  event_source_arn  = aws_dynamodb_table.state_table.stream_arn
  function_name     = aws_lambda_function.lambda_analytics.arn
  starting_position = "LATEST"
  batch_size        = 1
}
