locals {
  lambda_function_name = "lambda-${var.service.name}"
}

resource "aws_lambda_function" "this" {
  function_name = local.lambda_function_name
  role          = aws_iam_role.iam_for_lambda.arn
  runtime       = "python3.8"
  handler       = "lambda_function.lambda_handler"
  filename      = "index.zip"
  source_code_hash = filebase64sha256("index.zip")
  layers = [aws_lambda_layer_version.this.arn]
  environment {
    variables = {
      foo = "bar"
    }
  }

  lifecycle {
    ignore_changes = [source_code_hash]
  }
}

resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${local.lambda_function_name}"
  retention_in_days = 14
}