data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "lambda_iceberg_policy_statement" {
  statement {
    sid    = "S3Access"
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:GetObject",
      "s3:DeleteObject",
      "s3:ListBucket",
      "s3:GetBucketLocation"
    ]
    resources = [
      "arn:aws:s3:::finance-605771322130",
      "arn:aws:s3:::finance-605771322130/*"
    ]
  }

  statement {
    sid    = "GlueCatalogAccess"
    effect = "Allow"
    actions = [
      "glue:GetDatabase",
      "glue:GetTable",
      "glue:CreateTable",
      "glue:UpdateTable",
      "glue:DeleteTable"
    ]
    resources = [
      "arn:aws:glue:*:605771322130:catalog",
      "arn:aws:glue:*:605771322130:database/corretagem",
      "arn:aws:glue:*:605771322130:table/corretagem/*"
    ]
  }

  statement {
    sid    = "AthenaAccess"
    effect = "Allow"
    actions = [
      "athena:StartQueryExecution",
      "athena:GetQueryExecution",
      "athena:GetQueryResults",
      "athena:GetWorkGroup"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "SecretAccess"
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue"
    ]
    resources = ["*"]
  }

  statement {
    sid    = "S3AthenaResults"
    effect = "Allow"
    actions = [
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:ListMultipartUploadParts",
      "s3:AbortMultipartUpload",
      "s3:CreateBucket",
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::aws-athena-query-results-605771322130-us-east-2",
      "arn:aws:s3:::aws-athena-query-results-605771322130-us-east-2/*"
    ]
  }
}

data "aws_iam_policy_document" "kms_decrypt_policy_statement" {
  statement {
    effect    = "Allow"
    actions   = ["kms:Decrypt"]
    resources = ["*"]
  }
}
