variable "service" {
  type = object({
    name = string
  })
  default = {
    name = "sg-hazy-bot"
  }
}