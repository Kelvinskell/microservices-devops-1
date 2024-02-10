# Create Security Group
resource "aws_security_group" "jenkins_rules" {
  name        = "Jenkins rules"
  description = "Allow inbound traffic"
  
dynamic "ingress" {
    for_each = local.ingress
    content {
    description      = ingress.value.description
    from_port        = ingress.value.port
    to_port          = ingress.value.port
    protocol         = ingress.value.protocol
    cidr_blocks      = ["0.0.0.0/0"]
    }
}

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = "allow_tls"
  }
}


# Create EC2 Instance
resource "aws_instance" "jenkins_server" {
  ami           = var.ami
  instance_type = var.instance_type
  vpc_security_group_ids = [aws_security_group.jenkins_rules.id]
  user_data = file("tools-install.sh")
  user_data_replace_on_change = true

  tags = {
    Name = "Jenkins Server"
  }
  lifecycle {
    replace_triggered_by = [ aws_security_group.jenkins_rules.id ]
  }
}


# Define output
output "public_ip" {
  value = aws_instance.jenkins_server.public_ip
}