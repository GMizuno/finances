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

resource "aws_iam_policy" "lambda_iceberg_policy" {
  name        = "lambda-iceberg-writer-policy"
  description = "Permissoes para escrever tabelas Iceberg via AWS Wrangler"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "S3Access"
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:DeleteObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          "arn:aws:s3:::finance-605771322130",  # O Bucket em si
          "arn:aws:s3:::finance-605771322130/*" # Local Temporário/Staging
        ]
      },
      {
        Sid    = "GlueCatalogAccess"
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetTable",
          "glue:CreateTable",
          "glue:UpdateTable",
          "glue:DeleteTable"
        ]
        Resource = [
          "arn:aws:glue:*:605771322130:catalog",
          "arn:aws:glue:*:605771322130:database/corretagem",
          "arn:aws:glue:*:605771322130:table/corretagem/*"
        ]
      },
      {
        "Sid" : "AthenaAccess",
        "Effect" : "Allow",
        "Action" : [
          "athena:StartQueryExecution",
          "athena:GetQueryExecution",
          "athena:GetQueryResults",
          "athena:GetWorkGroup"
        ],
        "Resource" : "*"
      },
      {
        "Sid" : "S3AthenaResults",
        "Effect" : "Allow",
        "Action" : [
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:ListMultipartUploadParts",
          "s3:AbortMultipartUpload",
          "s3:CreateBucket",
          "s3:PutObject"
        ],
        "Resource" : [
          "arn:aws:s3:::finance-605771322130",
          "arn:aws:s3:::finance-605771322130/athena-results/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_iceberg_policy" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_iceberg_policy.arn
}
