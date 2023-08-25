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
        sh 'docker build -f /home/vagrant/agent/ProjectB/DockerfileProducts  -t microservice:$(git rev-parse --short=7 HEAD)'
      }
    }

    stage('Deploy container') {
      steps {
        sh 'docker rm -f microservice_container'
        sh 'docker run -d -p 8080:8080 --name microservice_container microservice:$(git rev-parse --short=7 HEAD)'
      }
    }
  }
}