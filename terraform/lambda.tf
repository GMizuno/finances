resource "aws_lambda_function" "lambda_stock_pricing" {
  function_name = "finance_stock"
  role          = aws_iam_role.lambda_execution_role.arn
  kms_key_arn   = "arn:aws:kms:us-east-2:605771322130:key/d35f7bb6-58f5-478a-97f3-b89f8dcb1435"
  timeout       = 300
  description   = "Lambda para realizar extração dos dados na Yahoo Finance"
  image_uri     = "${var.ecr_repo_url}:${var.image_tag}"
  package_type  = "Image"

  environment {
    variables = {
      WEBHOOK     = var.webhook_discord
      TICKETS     = var.tickets
      ENVIROMENTS = "PRD"
    }
  }

  tags = {
    Environment = "production"
    Application = "Finace"
  }
}

resource "aws_cloudwatch_event_rule" "ocr_schedule" {
  name        = "finance_stock_trigger"
  description = "Dispara a lambda de ${aws_lambda_function.lambda_stock_pricing.function_name} todo dia as 08:00 UTC"

  schedule_expression = "cron(45 22 ? * MON-FRI *)"

  tags = {
    Environment = "PRD"
    Application = "Finace"
  }
}

resource "aws_cloudwatch_event_target" "check_stock_every_day" {
  rule      = aws_cloudwatch_event_rule.ocr_schedule.name
  target_id = "finance_stock_lambda"
  arn       = aws_lambda_function.lambda_stock_pricing.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_ocr" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_stock_pricing.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.ocr_schedule.arn
}
