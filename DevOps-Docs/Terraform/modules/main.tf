provider "aws" {
  
         access_key = "AKIAXEFUNJMJJKSUL363"
                       secret_key = ""
}

resource "aws_instance" "test" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name = var.key_name

  tags = {
    Name = "test"
  }
}