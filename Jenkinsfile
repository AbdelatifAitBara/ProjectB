pipeline {
  agent any

  stages {
    stage('Clone Git Repository') {
      steps {
        sh 'rm -rf /home/vagrant/agent/ProjectB/'
        sh 'git -C /home/vagrant/agent/ clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git'
      }
    }

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

    stage('Remove Containers Running on Ports 8080 and 9090') {
      steps {
        script {
          def containers = sh(
            script: 'docker ps --filter "publish=80" --filter "publish=90" -q',
            returnStdout: true
          ).trim()
          if (containers) {
            sh "docker rm -f ${containers}"
          } else {
            echo "No containers running on ports 8080 and 9090"
          }
        }
      }
    }
    
    stage('Deploy Product Microservice') {
      steps {
        sh 'docker run -d -p 8080:80 --name product_microservice_container product_microservice:$(git rev-parse --short=7 HEAD)'
      }
    }

    stage('Deploy Order Microservice') {
      steps {
        sh 'docker run -d -p 9090:80 --name order_microservice_container order_microservice:$(git rev-parse --short=7 HEAD)'
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