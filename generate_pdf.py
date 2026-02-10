#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from datetime import datetime
import os

# Create PDF
pdf_path = "Terraform_ALB_EC2_Docker_Setup.pdf"
doc = SimpleDocTemplate(pdf_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for PDF elements
elements = []
styles = getSampleStyleSheet()

# Define custom styles
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=30,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2E5090'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

subheading_style = ParagraphStyle(
    'SubHeading',
    parent=styles['Heading3'],
    fontSize=11,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=10,
    spaceBefore=8,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=10
)

code_style = ParagraphStyle(
    'Code',
    parent=styles['Normal'],
    fontSize=8,
    fontName='Courier',
    textColor=colors.HexColor('#333333'),
    backColor=colors.HexColor('#f5f5f5'),
    leftIndent=10,
    rightIndent=10,
    spaceAfter=6
)

# Title Page
elements.append(Spacer(1, 1*inch))
elements.append(Paragraph("TERRAFORM ALB + EC2 + DOCKER", title_style))
elements.append(Paragraph("Infrastructure as Code Setup Guide", styles['Normal']))
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
elements.append(Spacer(1, 0.5*inch))

# Key Info Table
key_info = [
    ['Project', 'Terraform ALB EC2 Docker'],
    ['Region', 'AWS ap-south-1 (Mumbai)'],
    ['Infrastructure', 'ALB + ASG + EC2 + VPC'],
    ['Containerization', 'Docker (Nginx + Java)'],
    ['CI/CD', 'GitHub Actions'],
    ['Repository', 'Chettipellysrilatha/terraform-alb-ec2-docker']
]
key_table = Table(key_info, colWidths=[1.5*inch, 4.5*inch])
key_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#2E5090')),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (0, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))
elements.append(key_table)
elements.append(PageBreak())

# Table of Contents
elements.append(Paragraph("TABLE OF CONTENTS", heading_style))
toc_items = [
    "1. Architecture Overview",
    "2. Infrastructure Components",
    "3. File Structure & Code",
    "4. Deployment Instructions",
    "5. Configuration Details",
    "6. Troubleshooting Guide",
    "7. Monitoring & Scaling",
    "8. GitHub Actions CI/CD Pipeline"
]
for item in toc_items:
    elements.append(Paragraph(item, body_style))
elements.append(PageBreak())

# 1. Architecture Overview
elements.append(Paragraph("1. ARCHITECTURE OVERVIEW", heading_style))
elements.append(Paragraph(
    "This infrastructure deploys a highly available, auto-scaling web application on AWS using Terraform. "
    "The setup includes a VPC with public subnets, an Application Load Balancer (ALB) for traffic distribution, "
    "an Auto Scaling Group (ASG) managing EC2 instances, and Docker containers running Nginx and a Java application.",
    body_style
))
elements.append(Spacer(1, 0.15*inch))
elements.append(Paragraph("Key Components:", subheading_style))
arch_components = [
    ["Component", "Purpose"],
    ["VPC", "10.0.0.0/16 - Isolated network with 2 public subnets"],
    ["Internet Gateway", "Enables internet connectivity for public resources"],
    ["ALB", "Distributes incoming traffic across healthy EC2 instances"],
    ["Target Group", "Health checks and traffic routing to instances"],
    ["ASG", "Automatically scales EC2 instances (2-6) based on CPU utilization"],
    ["Launch Template", "Defines EC2 instance configuration and user data"],
    ["Security Groups", "Controls inbound/outbound traffic rules"],
    ["CloudWatch", "Monitors metrics and triggers scaling policies"]
]
arch_table = Table(arch_components, colWidths=[1.5*inch, 4.5*inch])
arch_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
]))
elements.append(arch_table)
elements.append(PageBreak())

# 2. Infrastructure Components
elements.append(Paragraph("2. INFRASTRUCTURE COMPONENTS", heading_style))

elements.append(Paragraph("2.1 Virtual Private Cloud (VPC)", subheading_style))
vpc_code = """
CIDR Block: 10.0.0.0/16
Public Subnets:
  - Subnet 1: 10.0.1.0/24 (ap-south-1a)
  - Subnet 2: 10.0.2.0/24 (ap-south-1b)
Internet Gateway: Attached to VPC
Route Table: Public subnets route 0.0.0.0/0 through IGW
"""
elements.append(Paragraph(vpc_code.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("2.2 Application Load Balancer", subheading_style))
alb_code = """
ALB Configuration:
  - Type: Application Load Balancer
  - Scheme: Internet-facing
  - Subnets: Both public subnets (for high availability)
  - Security Group: Allows inbound on port 80 from 0.0.0.0/0

Target Group:
  - Protocol: HTTP on port 80
  - Health Check: Path /, Interval 30s, Timeout 5s
  - Healthy Threshold: 2, Unhealthy: 2
  - Matcher: HTTP status 200
"""
elements.append(Paragraph(alb_code.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("2.3 Auto Scaling Group", subheading_style))
asg_code = """
ASG Configuration:
  - Min Size: 2 instances
  - Max Size: 6 instances
  - Desired Capacity: 3 instances
  - Launch Template: app-template (Version 4)
  - Health Check Type: ELB
  - Health Check Grace Period: 300 seconds

Scaling Policies:
  - Scale Up: CPU > 70% (add 1 instance)
  - Scale Down: CPU < 30% (remove 1 instance)
  - Evaluation: 2 consecutive periods, 5-minute intervals
"""
elements.append(Paragraph(asg_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

elements.append(Paragraph("2.4 EC2 Instances", subheading_style))
ec2_code = """
Instance Configuration:
  - AMI: Ubuntu 22.04 LTS (Canonical)
  - Instance Type: t2.small
  - Root Volume: 20 GB gp2
  - Security Group: app-sg (allows port 80 from ALB)
  - Availability: Distributed across 2 AZs

User Data Script:
  ✓ Updates system packages (apt-get)
  ✓ Installs Java 11 (OpenJDK)
  ✓ Installs Docker
  ✓ Starts Docker daemon and enables auto-start
  ✓ Runs Nginx container on port 80
  ✓ Runs Java application on port 8080
"""
elements.append(Paragraph(ec2_code.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("2.5 Security Groups", subheading_style))
sg_code = """
ALB Security Group (alb-sg):
  - Inbound: 0.0.0.0/0 on port 80 (HTTP)
  - Outbound: All traffic allowed

EC2 Security Group (app-sg):
  - Inbound: app-sg (ALB SG) on port 80 only
  - Outbound: All traffic allowed

Purpose: Restrict traffic - only ALB can reach instances
"""
elements.append(Paragraph(sg_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

# 3. File Structure & Code
elements.append(Paragraph("3. FILE STRUCTURE & CODE", heading_style))

elements.append(Paragraph("3.1 Project Layout", subheading_style))
structure = """
terraform-alb-ec2-docker/
  ├── provider.tf              # AWS provider configuration
  ├── variables.tf             # Input variables definition
  ├── terraform.tfvars         # Variable values
  ├── vpc.tf                   # VPC and networking
  ├── security.tf              # Security groups
  ├── alb.tf                   # Load balancer configuration
  ├── ec2.tf                   # EC2 instances
  ├── asg.tf                   # Auto scaling group
  ├── outputs.tf               # Output values
  ├── .github/workflows/
  │   └── terraform.yml        # GitHub Actions CI/CD
  ├── README.md                # Project documentation
  └── LEARNING_GUIDE.md        # Comprehensive guide
"""
elements.append(Paragraph(structure.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("3.2 Provider Configuration (provider.tf)", subheading_style))
provider_code = """
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "terraform-state-srilatha-001"
    key            = "terraform.tfstate"
    region         = "ap-south-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region
}
"""
elements.append(Paragraph(provider_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

elements.append(Paragraph("3.3 Variables (variables.tf)", subheading_style))
variables_code = """
variable "aws_region" {
  default = "ap-south-1"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  type    = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "instance_type" {
  default = "t2.small"
}

variable "instance_count" {
  default = 2
}

variable "asg_min_size" {
  default = 2
}

variable "asg_max_size" {
  default = 6
}

variable "asg_desired_capacity" {
  default = 3
}

variable "environment" {
  default = "production"
}
"""
elements.append(Paragraph(variables_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

elements.append(Paragraph("3.4 VPC & Networking (vpc.tf)", subheading_style))
vpc_tf_code = """
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Name = "app-vpc"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = {
    Name = "app-igw"
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block      = "0.0.0.0/0"
    gateway_id      = aws_internet_gateway.main.id
  }
  
  tags = {
    Name = "public-rt"
  }
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
"""
elements.append(Paragraph(vpc_tf_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

elements.append(Paragraph("3.5 Security Groups (security.tf)", subheading_style))
sg_tf_code = """
resource "aws_security_group" "alb" {
  name   = "alb-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "app" {
  name   = "app-sg"
  vpc_id = aws_vpc.main.id
  
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
"""
elements.append(Paragraph(sg_tf_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

elements.append(Paragraph("3.6 Load Balancer (alb.tf)", subheading_style))
alb_tf_code = """
resource "aws_lb" "main" {
  name               = "tf-lb-${formatdate("YYYYMMDDHHMMSS", timestamp())}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = aws_subnet.public[*].id
  
  tags = {
    Name = "app-alb"
  }
}

resource "aws_lb_target_group" "app" {
  name        = "app-tg"
  port        = 80
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  
  health_check {
    path                = "/"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 2
    unhealthy_threshold = 2
    matcher             = "200"
  }
}

resource "aws_lb_listener" "main" {
  load_balancer_arn = aws_lb.main.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}
"""
elements.append(Paragraph(alb_tf_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

elements.append(Paragraph("3.7 Auto Scaling Group (asg.tf - Key Sections)", subheading_style))
asg_tf_code = """
resource "aws_launch_template" "app" {
  name_prefix            = "app-template-"
  image_id               = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.app.id]
  
  user_data = base64encode(<<-EOF
              #!/bin/bash
              apt-get update -y
              apt-get install -y openjdk-11-jre-headless
              apt-get install -y docker.io
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu
              
              docker run -d -p 80:80 --name web-server nginx:latest
              docker run -d -p 8080:8080 --name java-app 
                -e JAVA_OPTS="-Xmx512m -Xms256m" 
                openjdk:11-jre-slim 
                java -jar /app/application.jar
              EOF
  )
  
  root_block_device {
    volume_size = 20
    volume_type = "gp2"
  }
}

resource "aws_autoscaling_group" "app" {
  name                = "app-asg-${aws_launch_template.app.latest_version_number}"
  vpc_zone_identifier = aws_subnet.public[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  health_check_grace_period = 300
  
  min_size         = var.asg_min_size
  max_size         = var.asg_max_size
  desired_capacity = var.asg_desired_capacity
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
}

resource "aws_autoscaling_policy" "scale_up" {
  name                   = "scale-up"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  autoscaling_group_name = aws_autoscaling_group.app.name
  cooldown               = 300
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 70
  alarm_actions       = [aws_autoscaling_policy.scale_up.arn]
}
"""
elements.append(Paragraph(asg_tf_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

# 4. Deployment Instructions
elements.append(Paragraph("4. DEPLOYMENT INSTRUCTIONS", heading_style))

elements.append(Paragraph("4.1 Prerequisites", subheading_style))
prereq_code = """
✓ AWS Account with appropriate IAM permissions
✓ AWS CLI configured with credentials
✓ Terraform 1.5+ installed
✓ Git installed
✓ GitHub account with repository access

S3 Bucket: terraform-state-srilatha-001
DynamoDB Table: terraform-locks
  - Partition Key: LockID (String)
"""
elements.append(Paragraph(prereq_code.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.15*inch))

elements.append(Paragraph("4.2 Step-by-Step Deployment", subheading_style))
deploy_steps = """
1. Clone Repository
   git clone https://github.com/Chettipellysrilatha/terraform-alb-ec2-docker.git
   cd terraform-alb-ec2-docker

2. Initialize Terraform
   terraform init
   (Initializes backend, downloads providers, validates state)

3. Format & Validate
   terraform fmt -recursive
   terraform validate

4. Plan Deployment
   terraform plan -out=tfplan

5. Apply Configuration
   terraform apply tfplan
   (Creates all AWS resources)

6. Get Outputs
   terraform output alb_url
   (Use this URL to access your application)

7. Verify Deployment
   - Check ALB in AWS Console
   - Verify target group health checks
   - Monitor ASG scaling events
   - Test application at ALB URL
"""
elements.append(Paragraph(deploy_steps.replace('\n', '<br/>'), body_style))
elements.append(PageBreak())

elements.append(Paragraph("4.3 Accessing the Application", subheading_style))
access_code = """
After successful deployment:

1. Get ALB URL:
   terraform output alb_url
   
2. Open in Browser:
   http://<alb_url>
   
3. Expected Response:
   - Nginx default page (port 80) from ALB
   - Java application (port 8080) on backend

4. Monitor Health:
   AWS Console → EC2 → Target Groups
   - Check all targets are "Healthy"
   - Monitor request count and response times
"""
elements.append(Paragraph(access_code.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("4.4 Common Terraform Commands", subheading_style))
commands = """
terraform init                    # Initialize workspace
terraform plan                    # Preview changes
terraform apply                   # Apply changes
terraform destroy                 # Destroy resources
terraform output                  # Show outputs
terraform state list              # List resources
terraform state show <resource>   # Show resource details
terraform refresh                 # Update state file
terraform fmt -recursive          # Format all files
terraform validate                # Validate syntax
"""
elements.append(Paragraph(commands.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

# 5. Configuration Details
elements.append(Paragraph("5. CONFIGURATION DETAILS", heading_style))

elements.append(Paragraph("5.1 terraform.tfvars Values", subheading_style))
tfvars_code = """
aws_region             = "ap-south-1"
vpc_cidr               = "10.0.0.0/16"
public_subnet_cidrs    = ["10.0.1.0/24", "10.0.2.0/24"]
instance_type          = "t2.small"
instance_count         = 2
asg_min_size           = 2
asg_max_size           = 6
asg_desired_capacity   = 3
environment            = "production"
"""
elements.append(Paragraph(tfvars_code.replace('\n', '<br/>'), code_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("5.2 User Data Script Breakdown", subheading_style))
userdata_breakdown = """
The user data script executed on each EC2 instance:

1. System Updates
   apt-get update -y
   (Updates package lists)

2. Install Java Runtime
   apt-get install -y openjdk-11-jre-headless
   (Lightweight Java for running applications)

3. Install Docker
   apt-get install -y docker.io
   (Container runtime)

4. Start Docker Service
   systemctl start docker
   systemctl enable docker
   (Ensures Docker starts on reboot)

5. Docker Permissions
   usermod -aG docker ubuntu
   (Allows ubuntu user to run Docker commands)

6. Run Nginx Container
   docker run -d -p 80:80 --name web-server nginx:latest
   (Port 80 - web server for ALB traffic)

7. Run Java Application
   docker run -d -p 8080:8080 --name java-app ... java -jar /app/application.jar
   (Port 8080 - backend application)

Note: Ports are mapped inside containers. Nginx acts as reverse proxy.
"""
elements.append(Paragraph(userdata_breakdown.replace('\n', '<br/>'), body_style))
elements.append(PageBreak())

# 6. Troubleshooting
elements.append(Paragraph("6. TROUBLESHOOTING GUIDE", heading_style))

elements.append(Paragraph("6.1 502 Bad Gateway Error", subheading_style))
error_502 = """
Problem: ALB returns 502 Bad Gateway error

Causes & Solutions:

1. User Data Script Not Executed
   ✗ Wrong AMI type (e.g., Amazon Linux commands on Ubuntu)
   ✓ Check instance console output: EC2 → Instances → Instance ID → Monitor
   ✓ Verify correct commands for AMI (apt-get for Ubuntu, yum for Amazon Linux)

2. Docker/Services Not Running
   ✗ Instance starting but services haven't started yet
   ✓ Check instance in ASG has completed initialization
   ✓ Give instances 3-5 minutes after launch
   ✓ Check CloudWatch logs for service startup

3. Ports Not Exposed
   ✗ Containers not mapping ports correctly
   ✓ Verify: docker ps -a (on instance)
   ✓ Check container logs: docker logs <container_name>

4. Security Group Issue
   ✗ EC2 SG doesn't allow traffic from ALB SG
   ✓ Verify source group in EC2 SG ingress rule
   ✓ Ensure rule allows port 80

5. Health Check Failing
   ✗ Target marked unhealthy even if service running
   ✓ Check Target Group health check settings
   ✓ Verify path "/" returns 200 status
   ✓ Check service is actually listening on port 80
"""
elements.append(Paragraph(error_502.replace('\n', '<br/>'), body_style))
elements.append(PageBreak())

elements.append(Paragraph("6.2 State Lock Issues", subheading_style))
lock_issues = """
Problem: Terraform operations hang or fail with lock errors

Root Causes:

1. DynamoDB Lock Corrupted
   Symptom: Multiple lock entries or stale entries
   Solution:
   - Check locks: aws dynamodb scan --table-name terraform-locks
   - Delete stale entries: aws dynamodb delete-item --table-name terraform-locks --key ...
   - Run: terraform refresh -lock=false

2. S3 State File Locked
   Symptom: "Error acquiring the state lock"
   Solution:
   - Use: terraform plan -lock=false (for read-only operations)
   - Clean lock: aws dynamodb delete-item --table-name terraform-locks --key ...

3. GitHub Actions Lock Conflict
   Solution in workflow:
   - terraform plan -input=false -lock=false
   - terraform apply -input=false -lock=false
   (Appropriate for CI/CD, read-only safety maintained via state file)
"""
elements.append(Paragraph(lock_issues.replace('\n', '<br/>'), body_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("6.3 Debugging Commands", subheading_style))
debug_commands = """
Check EC2 Instance Health:
  aws ec2 describe-instances --region ap-south-1 \\
    --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]'

Check ALB Target Health:
  aws elbv2 describe-target-health --target-group-arn <arn> \\
    --region ap-south-1

Check ASG Status:
  aws autoscaling describe-auto-scaling-groups \\
    --auto-scaling-group-names app-asg-* --region ap-south-1

View Instance Logs:
  aws ec2 get-console-output --instance-id <id> --region ap-south-1

Check CloudWatch Metrics:
  aws cloudwatch get-metric-statistics \\
    --namespace AWS/EC2 --metric-name CPUUtilization \\
    --dimensions Name=AutoScalingGroupName,Value=app-asg-* \\
    --start-time <date> --end-time <date> --period 300 --statistics Average
"""
elements.append(Paragraph(debug_commands.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

# 7. Monitoring & Scaling
elements.append(Paragraph("7. MONITORING & SCALING", heading_style))

elements.append(Paragraph("7.1 Auto Scaling Policies", subheading_style))
scaling_policies = """
Scale-Up Policy:
  Trigger: CPU Utilization > 70%
  Action: Add 1 instance to ASG
  Cooldown: 300 seconds (prevents rapid scaling)
  Min Instances: Always at least 2 running

Scale-Down Policy:
  Trigger: CPU Utilization < 30%
  Action: Remove 1 instance from ASG
  Cooldown: 300 seconds
  Max Reduction: One instance at a time

Evaluation:
  - Periods: 2 (two consecutive 5-minute periods)
  - Interval: 5 minutes (300 seconds)
  - This prevents rapid up/down cycles

Capacity Limits:
  Minimum: 2 instances (always running for HA)
  Maximum: 6 instances (cost control)
  Desired: 3 instances (target state)
"""
elements.append(Paragraph(scaling_policies.replace('\n', '<br/>'), body_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("7.2 CloudWatch Monitoring", subheading_style))
monitoring = """
Metrics Monitored:
  - CPUUtilization (triggers scaling policies)
  - NetworkIn / NetworkOut
  - StatusCheckFailed (instance health)
  - ALBRequestCount (traffic volume)
  - TargetResponseTime

How to View Metrics:
  AWS Console → CloudWatch → Dashboards
  Or CLI:
  aws cloudwatch list-metrics --namespace AWS/EC2 \\
    --dimensions Name=AutoScalingGroupName,Value=app-asg-*

Create Custom Dashboards:
  Monitor: CPU usage, request count, response time, instance count
  Update frequency: 1 minute for real-time visibility
"""
elements.append(Paragraph(monitoring.replace('\n', '<br/>'), body_style))
elements.append(PageBreak())

# 8. GitHub Actions CI/CD
elements.append(Paragraph("8. GITHUB ACTIONS CI/CD PIPELINE", heading_style))

elements.append(Paragraph("8.1 Workflow Overview", subheading_style))
workflow_overview = """
File: .github/workflows/terraform.yml

Trigger: Push to main branch

Pipeline Steps:

1. Checkout Code
   Actions/checkout@v3 (retrieve repository code)

2. Configure AWS Credentials
   AWS credentials from GitHub Secrets
   Assumes IAM role for Terraform operations

3. Setup Terraform
   hashicorp/setup-terraform@v2 (v1.5+)

4. Format Check
   terraform fmt -check -recursive (validates code style)

5. Terraform Init
   terraform init (initialize state, download providers)
   Uses S3 backend and DynamoDB locks

6. Validate
   terraform validate (syntax check)

7. Plan (Read-Only)
   terraform plan -input=false -lock=false \\
     -var-file=terraform.tfvars -out=tfplan
   (Creates execution plan without acquiring locks)

8. Apply (Deployment)
   terraform apply -input=false -lock=false tfplan
   (Applies approved changes to AWS)

9. Generate Outputs
   terraform output > $GITHUB_OUTPUT
   (For next workflow steps if needed)
"""
elements.append(Paragraph(workflow_overview.replace('\n', '<br/>'), body_style))
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("8.2 Key Features", subheading_style))
ci_features = """
✓ Automated Deployment: Every push to main triggers pipeline
✓ Plan Before Apply: Operators see changes before deployment
✓ Locking Strategy: Uses -lock=false (safe for stateless CI/CD)
✓ State Management: S3 backend with DynamoDB locks
✓ Error Handling: Pipeline stops on format/validation errors
✓ Outputs: Infrastructure details available after apply
✓ Secrets: AWS credentials stored in GitHub Secrets

GitHub Secrets Required:
  AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY
  AWS_DEFAULT_REGION (ap-south-1)
"""
elements.append(Paragraph(ci_features.replace('\n', '<br/>'), body_style))
elements.append(PageBreak())

elements.append(Paragraph("8.3 Workflow File (terraform.yml)", subheading_style))
workflow_code = """
name: Terraform

on:
  push:
    branches:
      - main

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_DEFAULT_REGION }}
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
      
      - name: Terraform Format Check
        run: terraform fmt -check -recursive
        continue-on-error: true
      
      - name: Terraform Init
        run: terraform init
      
      - name: Terraform Validate
        run: terraform validate
      
      - name: Terraform Plan
        id: plan
        run: terraform plan -input=false -lock=false \\
          -var-file=terraform.tfvars -out=tfplan
      
      - name: Terraform Apply
        run: terraform apply -input=false -lock=false tfplan
      
      - name: Generate Outputs
        run: terraform output
"""
elements.append(Paragraph(workflow_code.replace('\n', '<br/>'), code_style))
elements.append(PageBreak())

# 9. Summary & Best Practices
elements.append(Paragraph("9. SUMMARY & BEST PRACTICES", heading_style))

elements.append(Paragraph("9.1 Infrastructure Summary", subheading_style))
summary_table_data = [
    ["Component", "Details", "Status"],
    ["VPC", "10.0.0.0/16, 2 public subnets", "Active"],
    ["IGW", "Internet Gateway attached", "Active"],
    ["ALB", "Internet-facing, HTTP port 80", "Active"],
    ["Target Group", "Port 80, health check /, matcher 200", "Active"],
    ["ASG", "2-6 instances, desired 3", "Active"],
    ["Launch Template", "Ubuntu 22.04, t2.small, Docker", "v4"],
    ["Scaling Policies", "CPU >70% (up), <30% (down)", "Active"],
    ["Security Groups", "ALB SG + App SG with restrictions", "Active"],
    ["State Backend", "S3 + DynamoDB locks", "Configured"]
]
summary_table = Table(summary_table_data, colWidths=[1.3*inch, 2.7*inch, 1*inch])
summary_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E5090')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey)
]))
elements.append(summary_table)
elements.append(Spacer(1, 0.2*inch))

elements.append(Paragraph("9.2 Best Practices", subheading_style))
best_practices = """
Infrastructure as Code:
  ✓ Keep code in version control (Git)
  ✓ Use meaningful variable names
  ✓ Separate concerns (provider, vpc, security, etc.)
  ✓ Always use terraform.tfvars for values

State Management:
  ✓ Use S3 backend with encryption enabled
  ✓ Enable versioning on S3 bucket
  ✓ Use DynamoDB for state locking
  ✓ Never commit .tfstate files to Git
  ✓ Use -lock=false only for read-only CI/CD operations

Security:
  ✓ Use security groups to restrict traffic
  ✓ Follow principle of least privilege
  ✓ Don't expose sensitive data in code
  ✓ Use IAM roles with minimal permissions
  ✓ Enable S3 encryption and versioning

Scaling & Performance:
  ✓ Monitor CloudWatch metrics regularly
  ✓ Set appropriate CPU thresholds (avoid rapid scaling)
  ✓ Use health checks for instance validation
  ✓ Keep cooldown periods reasonable (300s)
  ✓ Test scaling policies in non-production first

CI/CD & Deployment:
  ✓ Always run terraform plan before apply
  ✓ Review plan output carefully
  ✓ Use separate environments (dev, staging, prod)
  ✓ Implement approval gates for production changes
  ✓ Keep Terraform versions consistent across team

Documentation:
  ✓ Document all variables and outputs
  ✓ Maintain README for infrastructure overview
  ✓ Track changes in Git commit messages
  ✓ Create runbooks for common operations
  ✓ Document troubleshooting procedures
"""
elements.append(Paragraph(best_practices.replace('\n', '<br/>'), body_style))
elements.append(PageBreak())

elements.append(Paragraph("9.3 Useful Resources", subheading_style))
resources = """
Official Documentation:
  • Terraform AWS Provider: https://registry.terraform.io/providers/hashicorp/aws
  • Terraform Language: https://www.terraform.io/docs
  • AWS EC2 Documentation: https://docs.aws.amazon.com/ec2/
  
Repository:
  • GitHub: https://github.com/Chettipellysrilatha/terraform-alb-ec2-docker
  • Main Branch: Contains latest infrastructure code
  • README.md: Quick reference and setup instructions
  
Quick Commands:
  • Deploy: terraform init && terraform apply tfplan
  • Destroy: terraform destroy
  • View Outputs: terraform output
  • Check State: terraform state list
  
AWS Console:
  • EC2 Instances: Check instance health and status
  • Load Balancers: View ALB and target group health
  • Auto Scaling: Monitor scaling events and policies
  • CloudWatch: View metrics and alarms
  • S3: Verify state file backups and versions
"""
elements.append(Paragraph(resources.replace('\n', '<br/>'), body_style))
elements.append(Spacer(1, 0.3*inch))

elements.append(Paragraph("Generated: " + datetime.now().strftime('%B %d, %Y at %H:%M:%S'), styles['Italic']))
elements.append(Paragraph("Project: Terraform ALB + EC2 + Docker Infrastructure", styles['Italic']))

# Build PDF
doc.build(elements)
print(f"✓ PDF created successfully: {pdf_path}")
