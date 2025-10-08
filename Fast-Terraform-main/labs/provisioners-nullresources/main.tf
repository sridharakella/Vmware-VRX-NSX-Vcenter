terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
	region = "eu-central-1"
}

resource "aws_vpc" "my_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = {
    Name = "My VPC"
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = "eu-central-1c"
  tags = {
    Name = "Public Subnet"
  }
}

resource "aws_internet_gateway" "my_vpc_igw" {
  vpc_id = aws_vpc.my_vpc.id
  tags = {
    Name = "My VPC - Internet Gateway"
  }
}

resource "aws_route_table" "my_vpc_eu_central_1c_public" {
    vpc_id = aws_vpc.my_vpc.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.my_vpc_igw.id
    }
    tags = {
        Name = "Public Subnet Route Table"
    }
}
resource "aws_route_table_association" "my_vpc_eu_central_1c_public" {
    subnet_id      = aws_subnet.public.id
    route_table_id = aws_route_table.my_vpc_eu_central_1c_public.id
}

resource "aws_security_group" "allow_ssh" {
  name        = "allow_ssh_sg"
  description = "Allow SSH inbound connections"
  vpc_id      = aws_vpc.my_vpc.id
  # for SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["0.0.0.0/0"]
  }
  tags = {
    Name = "allow_ssh_sg"
  }
}

resource "aws_instance" "ubuntu2204" {

  ami                         = "ami-0d1ddd83282187d18" # Ubuntu 22.04 eu-central-1 Frankfurt
  instance_type               = "t2.nano" 
  key_name                    = "testkey"
  vpc_security_group_ids      = [aws_security_group.allow_ssh.id]
  subnet_id                   = aws_subnet.public.id
  associate_public_ip_address = true

  tags = {
    Name = "Ubuntu 22.04"
  }

  provisioner "file" {
    source      = "test-file.txt" 
    destination = "/home/ubuntu/test-file.txt"
  }

  provisioner "file" {
    content     = "I want to copy this string to the destination file => server.txt (using provisioner file content)"
    destination = "/home/ubuntu/server.txt"
  }
  
  provisioner "remote-exec" {
    inline = [
      "touch hello.txt",
      "echo helloworld remote-exec provisioner >> hello.txt",
    ]
  }

  connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ubuntu"
      private_key = file("testkey.pem")
      timeout     = "4m"
   }
}

resource "null_resource" "example" {
  provisioner "local-exec" {
    command = "'This is test file for null resource local-exec' >>  nullresource-generated.txt"
    interpreter = ["PowerShell", "-Command"]
  }
}

