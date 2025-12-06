variable "region" {
  type        = string                     # The type of the variable, in this case a string
  default     = "us-east-2"                # Default value for the variable
  description = "The type of EC2 instance" # Description of what this variable represents
}

variable "bucket_id" {
  type    = string
  default = "notas-corretagem-605771322130"
}

variable "bucket_arn" {
  type    = string
  default = "arn:aws:s3:::notas-corretagem-605771322130"
}

variable "webhook_discord" {
  type = string
}

variable "tickets" {
  type = string
}

variable "ecr_repo_url" {
  type = string
  default = "605771322130.dkr.ecr.us-east-2.amazonaws.com/teste_mizuno"
}

variable "image_tag" {
  type = string
}
