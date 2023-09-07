pipeline {
  agent { label 'Production_Machine' }
  
  environment {
    PROJECT_DIR = '/home/jenkins/ProjectB'
    PROJECT_FOLDER = 'ProjectB'
    DOCKER_COMPOSE_FILE_MICROSERVICES = 'microservices/docker-compose.yml'
  }

  stages {
    stage('Clone Git Repository') {
      steps {
        sh "rm -rf ${PROJECT_DIR}"
        sh "mkdir -p ${PROJECT_DIR}"
        sh "git clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git ${PROJECT_DIR}"
      }
    }

    stage('Build Microservices Images') {
      steps {
        sh "docker-compose -f ${DOCKER_COMPOSE_FILE_MICROSERVICES} build"
      }
    }

    stage('Deploy Microservices Container') {
      steps {
        input message: 'Approve deployment?', ok: 'Deploy'
        sh "docker-compose -c ${DOCKER_COMPOSE_FILE_MICROSERVICES} down" 
        sh "docker-compose -c ${DOCKER_COMPOSE_FILE_MICROSERVICES} up -d"
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