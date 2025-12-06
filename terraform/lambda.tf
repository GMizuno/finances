resource "aws_lambda_function" "lambda_stock_pricing" {
  function_name = "finance_stock"
  role          = aws_iam_role.lambda_execution_role.arn
  kms_key_arn   = "arn:aws:kms:us-east-2:605771322130:key/d35f7bb6-58f5-478a-97f3-b89f8dcb1435"
  timeout       = 300
  description   = "Lambda para realizar operações de OCR nas notas de corretagem "
  image_uri     = "${var.ecr_repo_url}:${var.image_tag}"
  package_type  = "Image"

  environment {
    variables = {
      WEBHOOK     = var.webhook_discord
      TICKETS     = var.tickets
    }
  }

  tags = {
    Environment = "production"
    Application = "Finace"
  }
}
