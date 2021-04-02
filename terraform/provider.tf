provider "aws" {
  version = "~> 3.35.0"
  region  = "ap-southeast-1"
}

terraform {
  backend "s3" {
    bucket = "ry-terraform-state"
    key    = "sg-hazy-bot/terraform.tfstate"
    region = "ap-southeast-1"
  }
}