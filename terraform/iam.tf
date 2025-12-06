resource "aws_iam_role" "lambda_execution_role" {
  name               = "lambda_ecr_stock"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Policy: Permissão para escrever no S3 na pasta Results
resource "aws_iam_policy" "s3_write_policy" {
  name        = "s3_write_results_policy"
  description = "Permite escrita no bucket nfinance-605771322130 na pasta Results"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["s3:PutObject", "s3:GetObject"]
        Effect   = "Allow"
        Resource = "arn:aws:s3:::finance-605771322130/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}

resource "aws_iam_policy" "kms_decrypt_policy" {
  name        = "kms_decrypt_policy"
  description = "Permite desencriptação com uma KMS Key específica"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = ["kms:Decrypt"]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "kms_policy_attachment" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.kms_decrypt_policy.arn
}
