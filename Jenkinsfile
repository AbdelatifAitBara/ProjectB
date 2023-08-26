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
        sh 'docker build -f /home/vagrant/agent/ProjectB/DockerfileProducts -t product_microservice:$(git rev-parse --short=7 HEAD) /home/vagrant/agent/ProjectB/'
      }
    }

    stage('Remove Container Running on port 8080') {
      steps {
        script {
          def containers = sh(
            script: 'docker ps --filter "publish=8080" -q',
            returnStdout: true
          ).trim()
          if (containers) {
            sh "docker rm -f ${containers}"
          } else {
            echo "No containers running on port 8080"
          }
        }
      }
    }
    
    stage('Deploy container') {
      steps {
        sh 'docker rm -f product_microservice_container'
        sh 'docker run -d -p 8080:8080 --name product_microservice_container product_microservice:$(git rev-parse --short=7 HEAD)'
      }
    }

    stage('Product Microservice Test') {
      steps {
        sh 'sleep 6'
        sh 'python3 -m unittest test_product.py'
      }
    }

  }
}