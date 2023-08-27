pipeline {
  agent any

  stages {
    stage('Clone Git Repository') {
      steps {
        sh 'rm -rf /home/vagrant/agent/ProjectB/'
        sh 'git -C /home/vagrant/agent/ clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git'
      }
    }

/*
    stage('Build Product Image') {
      steps {
        sh 'docker build -f /home/vagrant/agent/ProjectB/product/Dockerfile -t product_microservice:$(git rev-parse --short=7 HEAD) /home/vagrant/agent/ProjectB/product/'
      }
    }

    stage('Build Order Image') {
      steps {
        sh 'docker build -f /home/vagrant/agent/ProjectB/order/Dockerfile -t order_microservice:$(git rev-parse --short=7 HEAD) /home/vagrant/agent/ProjectB/order/'
      }
    }

*/

    stage('Remove Containers Running on Ports 8080 and 9090') {
      steps {
        script {
          sh 'docker rm -f product_container'
          sh 'docker rm -f order_container'
        }
      }
    }
/*
    stage('Deploy Product Microservice') {
      steps {
        sh 'rm -f product_microservice_container'
        sh 'docker run -d -p 8080:8080 --name product_microservice_container product_microservice:$(git rev-parse --short=7 HEAD)'
      }
    }


    stage('Deploy Order Microservice') {
      steps {
        sh 'rm -f order_microservice_container'
        sh 'docker run -d -p 9090:9090 --name order_microservice_container order_microservice:$(git rev-parse --short=7 HEAD)'
      }
    }
*/

    stage('Build') {
      steps {
        // Build your microservices using Docker-compose
        sh 'docker-compose -f microservices/docker-compose.yml build'
      }
    }
    
    stage('Deploy') {
      steps {
        // Deploy your microservices using Docker-compose
        sh 'docker-compose -f microservices/docker-compose.yml up -d'
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