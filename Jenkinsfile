pipeline {
  agent any

  stages {
    stage('Clone Git Repository') {
      steps {
        sh 'rm -rf /home/jenkins/ProjectB/'
        sh 'git -C /home/jenkins clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git'
      }
    }

    stage('Remove The Old Containers') {
      steps {
        script {
          sh 'docker rm -f product_container'
          sh 'docker rm -f order_container'
        }
      }
    }

    stage('Build Microservices Images') {
      steps {
        // Build your microservices using Docker-compose
        sh 'docker-compose -f microservices/docker-compose.yml build'
      }
    }
    
    stage('Deploy Microservices Containers') { 
      steps {
        // Deploy your microservices using Docker-compose
        input message: 'Approve deployment?', ok: 'Deploy'
        sh 'docker-compose -f microservices/docker-compose.yml up -d'
      }
    }

    stage('Delete Unused Docker Images') {
      steps {
        sh 'docker system prune --all --force'
      }
    }
  }
}