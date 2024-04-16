resource "aws_default_vpc" "default_vpc" {
  tags = {
    Name = "default vpc for Project"
  }
}

data "aws_availability_zones" "available_zones" {}

resource "aws_default_subnet" "subnet_az1" {
  availability_zone = data.aws_availability_zones.available_zones.names[0]
}

resource "aws_default_subnet" "subnet_az2" {
  availability_zone = data.aws_availability_zones.available_zones.names[1]
}

resource "aws_db_subnet_group" "database_subnet_group" {
  name        = "database-subnets-for-project"
  subnet_ids  = [aws_default_subnet.subnet_az1.id, aws_default_subnet.subnet_az2.id]
  description = "subnets for database instance"

  tags = {
    Name = "database-subnets for project"
  }
}

resource "aws_db_instance" "db_instance" {
  engine                = "mysql"
  engine_version        = "8.0.31"
  multi_az              = false
  identifier            = "rds-instance-for-project"
  username              = "basgeo"
  password              = "password"
  instance_class        = "db.t3.micro"
  allocated_storage     = 200
  db_subnet_group_name  = aws_db_subnet_group.database_subnet_group.name
  availability_zone     = data.aws_availability_zones.available_zones.names[0]
  db_name               = "applicationdbz"
  skip_final_snapshot   = true
}

