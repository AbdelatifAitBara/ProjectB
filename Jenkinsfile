pipeline {
  agent any
  
  environment {
    PROJECT_DIR = '/home/jenkins/ProjectB'
    PROJECT_FOLDER = 'ProjectB'
    DOCKER_COMPOSE_FILE = 'microservices/docker-compose.yml'
    DOCKER_IMAGE = 'python:3.8-slim-buster'
  }

  stages {
    stage('Clone Git Repository') {
      steps {
        sh "rm -rf ${PROJECT_DIR}"
        sh "mkdir -p ${PROJECT_DIR}"
        sh "git -C ${PROJECT_DIR} clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git"
      }
    }

    stage('Build Microservices Images') {
      steps {
          sh "docker-compose -f ${DOCKER_COMPOSE_FILE} build"
      }
    }

    stage('Leave Swarm') {
      steps {
        sh "docker swarm leave --force || true" // leave the swarm if already joined
      }
    }

    stage('Deploy Microservices Stack') {
      steps {
        input message: 'Approve deployment?', ok: 'Deploy'
        sh "docker swarm init --advertise-addr 10.0.2.15" // initialize the swarm
        sh "docker stack deploy -c ${DOCKER_COMPOSE_FILE} production-microservices" // deploy the stack to the swarm
      }
    }

    stage('Delete Unused Docker Images') {
      steps {
        sh 'docker system prune --all --force'
      }
    }
  }

  post {
    failure {
      echo "Build failed: ${currentBuild.result}"
    }
    success {
      echo "Build succeeded: ${currentBuild.result}"
    }
  }
}