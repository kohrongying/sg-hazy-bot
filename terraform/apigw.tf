data "aws_api_gateway_rest_api" "this" {
  name = "main"
}

resource "aws_api_gateway_resource" "this" {
  rest_api_id = data.aws_api_gateway_rest_api.this.id
  parent_id   = data.aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "haze"
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = data.aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_resource.this.id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "any" {
  rest_api_id   = data.aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
  rest_api_id             = data.aws_api_gateway_rest_api.this.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.any.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.this.invoke_arn
}

resource "aws_api_gateway_deployment" "this" {
  rest_api_id = data.aws_api_gateway_rest_api.this.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id = data.aws_api_gateway_rest_api.this.id
  stage_name    = "dev"
}