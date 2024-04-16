provider "aws" {
  region  = "us-east-2"
}

resource "aws_instance" "example_instance" {
  ami           = "ami-02ca28e7c7b8f8be1"
  instance_type = "t2.micro"

  tags = {
    Name = "Example-Instance-For-Project"
  }
}
