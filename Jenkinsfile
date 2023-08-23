pipeline {
  agent any

  stages {
    stage('Clone Git repository') {
      steps {
        sh 'git clone https://github.com/AbdelatifAitBara/ProjectB /home/vagrant'
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