locals {
    ingress = [{
        port = 22
        description = "SH"
        protocol = "tcp"
    },
    {
        port = 8080
        description = "Jenkins Port"
        protocol = "tcp"
    },
    {
        port = 9000
        description = "Sonarqube Port"
        protocol = "tcp"
    }
    ]
}

