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
        withSonarQubeEnv('Sonarqube Server') {
          sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=newsread-microservice-application"
        }
      }
    }

        stage('Build Docker Images') {
            steps {
                script{
                    sh 'docker build -t kelvinskell/newsread-customize customize-service/'
                    sh 'docker build -t kelvinskell/newsread-news news-service/'
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
        stage('Push Images To Dockerhub') {
            steps {
                    script{
                        withCredentials([string(credentialsId: 'DockerHubPass', variable: 'DockerHubPass')]) {
                        sh 'docker login -u kelvinskell --password ${DockerHubPass}' }
                        sh 'docker push kelvinskell/newsread-news && docker push kelvinskell/newsread-customize'
               }
            }
                 
            }

        //stage('Trivy scan on Docker images'){
          //  steps{
            //     sh 'TMPDIR=/home/jenkins'
              //   sh 'trivy image kelvinskell/newsread-news:latest'
                // sh 'trivy image kelvinskell/newsread-customize:latest'
        //}
       
   // }
        }    

        post {
        always {
            // Always executed
                sh 'docker rm news-service'
                sh 'docker rm customize-service'
        }
        success {
            // on sucessful execution
            sh 'docker logout'   
        }
    }
}