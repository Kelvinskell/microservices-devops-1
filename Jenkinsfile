pipeline {
    agent any
    
    stages{
        stage('SCA with OWASP Dependency Check') {
        steps {
            dependencyCheck additionalArguments: '''--format HTML
            ''', odcInstallation: 'DP-Check'
            }
    }

        stage('SonarQube Analysis') {
      steps {
        script {
          // requires SonarQube Scanner 2.8+
          scannerHome = tool 'SonarScanner'
        }
        withSonarQubeEnv('SonarQube Server') {
          sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=newsread-microservice-application"
        }
      }
    }

        stage('Build Docker Image') {
            steps {
                script{
                    sh 'cd customize-service'
                    sh 'docker build -t kelvinskell/newsread-customize .'
                    sh 'cd ../news-service'
                    sh 'docker build -t kelvinskell/newsread-news'
                    sh 'cd ..'
            }
        }
    }
        stage('Containerize And Test') {
            steps {
                script{
                    sh 'docker run -d  --name customize-service -e FLASK_APP=run.py kelvinskell/newsread-customize && sleep 10 && docker logs customize-service && docker stop customize-service'
                    sh 'docker run -d  --name news-service -e FLASK_APP=run.py kelvinskell/newsread-news && sleep 10 && docker logs news-service && docker stop news-service'
                }
            }
        }
        stage('Push Image To Dockerhub') {
            steps {
                    script{
            withDockerRegistry(credentialsId: 'DockerHub-Creds'
                sh 'docker push kelvinskell/newsread-customize && docker push kelvinskell/newsread-news'}
            }
                 // script{
                 //   withCredentials([string(credentialsId: 'DockerHubPass', variable: 'DockerHubpass')]) {
                 //   sh 'docker login -u kelvinskell --password ${DockerHubpass}' }
                  //  sh 'docker push kelvinskell/newsread-news && docker push kelvinskell/newsread-customize'
               // }
            }

        stage('Trivy scan on Docker image'){
            steps{
                 sh 'trivy image kelvinskell/newsread-news/new:latest'
                 sh 'trivy image kelvinskell/newsread-customize/new:latest'
        }
       
    }
        }    
}
        post {
        always {
            // Always executed
                sh 'docker rm newsread-customize'
                sh 'docker rm newsread-news'
        }
        success {
            // on sucessful execution
            sh 'docker logout'   
        }
    }
}