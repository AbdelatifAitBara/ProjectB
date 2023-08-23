pipeline {
  agent any

  stages {
    stage('Clone Git Repository') {
      steps {
        sh 'rm -rf /home/vagrant/agent/ProjectB/'
        sh 'git -C /home/vagrant/agent/ clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker rmi -f microservice'
        sh 'docker build -t microservice .'
      }
    }

        
    stage('Tag Docker Image') {
      steps {
        script {
          sh 'docker tag microservice:$(git rev-parse --short=7 HEAD) microservice_image:latest'
        }
      }
    }
    stage('Deploy container') {
      steps {
        sh 'docker rm -f microservice_container'
        sh 'docker run -d -p 8080:8080 --name microservice_container microservice_image:latest'
      }
    }
  }
}