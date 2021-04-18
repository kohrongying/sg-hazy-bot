resource "aws_lambda_permission" "apigw_lambda_dev" {
  statement_id  = "AllowExecutionFromAPIGatewayDevStage"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.this.function_name}:dev"
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_api_gateway_rest_api.this.execution_arn}/*/*/haze"
}

resource "aws_lambda_permission" "apigw_lambda_prod" {
  statement_id  = "AllowExecutionFromAPIGatewayProdStage"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.this.function_name}:prod"
  principal     = "apigateway.amazonaws.com"

  source_arn = "${data.aws_api_gateway_rest_api.this.execution_arn}/*/*/haze"
}