terraform {
  backend "s3" {
    bucket  = "terraform-state-mizuno"
    key     = "terraform-finance.tfstate"
    region  = "us-east-2"
    encrypt = true
  }
}
