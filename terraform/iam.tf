resource "aws_iam_role" "lambda_execution_role" {
  name               = "lambda_ecr_stock"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "kms_decrypt_policy" {
  name        = "kms_decrypt_policy_lambda_stock"
  description = "Permite desencriptação com uma KMS Key específica"
  policy      = data.aws_iam_policy_document.kms_decrypt_policy_statement.json
}

resource "aws_iam_role_policy_attachment" "kms_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.kms_decrypt_policy.arn
}

resource "aws_iam_policy" "lambda_iceberg_policy" {
  name        = "lambda-iceberg-writer-policy"
  description = "Permissoes para escrever tabelas Iceberg via AWS Wrangler"

  policy = data.aws_iam_policy_document.lambda_iceberg_policy_statement.json
}

resource "aws_iam_role_policy_attachment" "attach_iceberg_policy" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_iceberg_policy.arn
}
