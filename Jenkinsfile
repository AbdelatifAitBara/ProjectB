pipeline {
  agent any

  stages {
    stage('Clone Git repository') {
      steps {
        sh 'rm -drf /home/vagrant/agent/ci-cd/'
        sh 'git -C /home/vagrant/agent/ clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t microservice .'
      }
    }

    stage('Deploy container') {
      steps {
        sh 'docker run -d -p 8080:8080 microservice'
      }
    }
  }
}