pipeline {
  agent any

  stages {
    stage('Clone Git repository') {
      steps {
        git 'https://github.com/username/repo.git'
      }
    }

    stage('Build Docker image') {
      steps {
        sh 'docker build -t myimage .'
      }
    }

    stage('Push Docker image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
          sh 'docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD'
          sh 'docker push myimage'
        }
      }
    }

    stage('Deploy container') {
      steps {
        sh 'docker run -d -p 8080:80 myimage'
      }
    }
  }
}