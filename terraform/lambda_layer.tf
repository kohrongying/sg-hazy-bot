resource "aws_lambda_layer_version" "this" {
  filename   = "requests.zip"
  layer_name = "lambda-layer-python38-requests"
  source_code_hash = filebase64sha256("requests.zip")

  compatible_runtimes = ["python3.6", "python3.7yes", "python3.8"]

  lifecycle {
    ignore_changes = [source_code_hash]
  }
}