pipeline {
  agent any

  stages {
    stage('Clone Git Repository') {
      steps {
        sh 'rm -rf /home/vagrant/agent/ProjectB/'
        sh 'git -C /home/vagrant/agent/ clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git'
      }
    }

    stage('Remove Containers Running on Ports 8080 and 9090') {
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
        sh 'docker-compose -f microservices/docker-compose.yml up -d'
      }
    }

/*    
    stage('Product Microservice Test') {
      steps {
        sh 'sleep 6'
        sh 'python3 -m unittest test_product.py'
      }
    }
*/    
  }
}