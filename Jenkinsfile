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

    stage('Deploy Microservices Containers') {
      steps {
        input message: 'Approve deployment?', ok: 'Deploy'
        sh "docker-compose -f ${DOCKER_COMPOSE_FILE_MICROSERVICES} down"
        sh "docker-compose -f ${DOCKER_COMPOSE_FILE_MICROSERVICES} up -d"
        
      }
    }

    stage('Delete Unused Docker Images') {
      steps {
        sh 'docker system prune --all --force'
      }
    }

    stage('Clone Git Repository (Observability)') {
      agent {
        label 'Observability'
      }
      steps {
        sh "rm -rf ${PROJECT_DIR}"
        sh "mkdir -p ${PROJECT_DIR}"
        sh "git clone --recursive git@github.com:AbdelatifAitBara/ProjectB.git ${PROJECT_DIR}"
      }
    }


    stage('Start Swarm Cluster') {
      agent {
        label 'Observability'
      }
      steps {
        script {
            def isSwarm = sh(returnStdout: true, script: 'docker info --format "{{.Swarm.LocalNodeState}}"').trim()
            
            if (isSwarm == "inactive") {
                sh "docker swarm init --advertise-addr 10.0.2.15"
                sh "docker network create --driver overlay --attachable monitoring"
                sh "cd promgrafnode && docker stack deploy -c docker-compose.yml observability-stack"
            } else {
                echo "The swarm is already active."
                echo "Do you want to leave it and deploy a new observability-stack with an improvement function?"
                sh "cd promgrafnode && docker stack deploy -c docker-compose.yml observability-stack"
            }
        }
      }
    }

  }

  post {
    failure {
      echo "Build failed: \${currentBuild.result}"
    }
    success {
      echo "Build succeeded: \${currentBuild.result}"
    }
  }
}
