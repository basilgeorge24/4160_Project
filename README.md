# Multi-Cloud Deployment with Terraform 
*By Basil George. Ryan Ostrowski, Christian Aziz*

> [!NOTE] 
> To view this README.md, download the 'Markdown All in One' extension on VS Code, open the README.md file, press Ctrl+Shift+V   

We have used Terraform to solve the problem of managing multiple cloud deployments. For the  project, we are focused on AWS and GCP. Terraform transforms what would be a tedious and error-prone process into a streamlined and efficient one, making infrastructure management more reliable and scalable. 

## Pre-requesites 
1. Download Terraform from https://developer.hashicorp.com/terraform/install

2. Create an AWS and a GCP account.

3. Download AWS Cli and configure it with the Secret key and Access Key for your root / IAM user.
   
4. Add the **AdministratorAccess** and **AmazonRDSFullAccess** policies to your root / IAM user.
   
5. Create a project on GCP (optional) and enable the **Compute Engine API** and the **Cloud SQL Admin API**.
   
6. Create a service account on GCP after which you will receive a key. Download this key file onto your computer. 
   
7. Install Flask 
   
## Procedure
1. Under **main.tf** of **aws_ec2**
   - You need to provide the region where you want to deploy your EC2 instance.
   You also need to provide your desired Amazon Machine Image in ami, which can be found on the AWS website. 
   - Choose your instance type depending on the number of CPUs, memory, storage and budget you have. Repace *example_instance* with whatever name you want your instance to have. 
  
 ```
 provider "aws" {
  region  = "us-####-#"
}

resource "aws_instance" "example_instance" {
  ami           = "ami-#####" 
  instance_type = "t2.micro" 

  tags = {
    Name = "Tag for your instance"
  }
}
```

2. Under **main.tf** of **aws_rds**, you can replace the name of your RDS by replacing the *identifier* value. You can also edit the *engine*, *instance_class*, and *allocated storage* according to your needs. Enter a desired *username* and *password* to access your database once created.

```
resource "aws_db_subnet_group" "database_subnet_group" {
  name        = "database-subnets"
  subnet_ids  = [aws_default_subnet.subnet_az1.id, aws_default_subnet.subnet_az2.id]
  description = "subnets for database instance"

  tags = {
    Name = "database-subnets"
  }
}

resource "aws_db_instance" "db_instance" {
  engine                = "mysql"
  engine_version        = "8.0.31"
  multi_az              = false
  identifier            = "trial-rds-instance"
  username              = "#####" 
  password              = "#####" 
  instance_class        = "db.t2.micro"
  allocated_storage     = 200
  db_subnet_group_name  = aws_db_subnet_group.database_subnet_group.name
  availability_zone     = data.aws_availability_zones.available_zones.names[0]
  db_name               = "applicationdbz"
  skip_final_snapshot   = true
}
```
3. For **main.tf** under **gcp_compute**, 
   -  Add the path of the GCP JSON key which was downloaded earlier under *credentials* 
   - Enter the project ID under *project*
   - Enter the region you want your VM instance to be deployed under *region*.
   - Change the *name*, *machine_type*, *zone*, *image* however you please 

```
provider "google" { 
  credentials = file("#########")
  project     = "#####" 
  region      = "us-####-#"
}

resource "google_compute_instance" "example_instance" {
  name         = "example-instance"
  machine_type = "n1-standard-1"
  zone         = "us-#####-#"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }
  network_interface {
    network = "default"
  }
}
```
4. Make the necessary changes in **main.tf** of **gcp_sql** like we did in aws_rds

## Execution
1. Go into the **aws_ec2, aws_rds, gcp_compute,** and **gcp_sql folders** individually and run *terraform init*. This should create additional dependencies in your folder.
   
2. Run the **app.py** and click on the link in the terminal which will take you to the webpage. 

3. On the webpage, select the desired deployment from the list. It will take time depending on which deployment you chose and the configurations you when creating your Terraform scripts.
   
4. You will get a **Deployment Successful** page once the deployment has been succesful. Check AWS or GCP for the results. 

> [!TIP]
> It is good practice to destroy the resources you created once you are happy with your results. To do this, just select the option to delete whatever resource you created on the webpage.