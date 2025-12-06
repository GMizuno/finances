variable "region" {
  type        = string                     # The type of the variable, in this case a string
  default     = "us-east-2"                # Default value for the variable
}

variable "webhook_discord" {
  type        = string
  description = "A URL do webhook recebida via GitHub Secrets"
}

variable "tickets" {
  type = string
}

variable "ecr_repo_url" {
  type    = string
  default = "605771322130.dkr.ecr.us-east-2.amazonaws.com/teste_mizuno"
}

variable "image_tag" {
  type = string
}
