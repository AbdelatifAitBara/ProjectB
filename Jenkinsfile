pipeline {
    agent { label 'Production_Machine' }
  
    environment {
        PROJECT_DIR = '/home/jenkins/ProjectB'
        PROJECT_FOLDER = 'ProjectB'
        DOCKER_COMPOSE_FILE = 'microservices/docker-compose.yml'
    }

    stages {
        stage('Clone Git Repository') {
            steps {
                sh "rm -rf ${PROJECT_DIR}"
                sh "mkdir -p ${PROJECT_DIR}"
                sh "git -C ${PROJECT_DIR} clone --recursive git@github.com:Tigran69LYON/ProjectB.git"
            }
        }

        stage('Build Microservices Images') {
            steps {
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} build"
            }
        }
    
        stage('Test WebGui') {
            steps {
                                
                script {
                                
                // Run the tests using the test.sh script and capture the output
                def testOutput = sh(script: "docker run --rm=false test_image:${GIT_COMMIT} /bin/sh test.sh", returnStdout: true).trim()
                
                // Get the timestamp
                def timestamp = sh(script: 'date +%Y%m%d%H%M', returnStdout: true).trim()

                // Define the destination path on the VM with the timestamp
                //def destination = "/home/jenkins/test_results_${timestamp}.txt"

                // Coping file with result for records on VM
                //sh(script: 'docker cp $(docker ps -lq):/tests/test_results.txt /home/jenkins/test_results_$(timestamp).txt')
                sh(script: "docker cp \$(docker ps -lq):/tests/test_results.txt /home/jenkins/test_results_${timestamp}.txt")

                // Print the test output for reference
                sh(script: "echo ${testOutput}")
                                
                // Check the result of the tests
                if (testOutput.contains("SUCCESS")) {
                    // Tests passed
                    currentBuild.result = 'SUCCESS'
                } else {
                    //Tests failed
                    currentBuild.result = 'FAILED'
                    }
                }
            }
        }

        stage('Deploy Microservices Containers') {
            when {
                expression { currentBuild.resultIsBetterOrEqualTo('SUCCESS') }
            }
            steps {
                input message: 'Approve deployment?', ok: 'Deploy'
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} down"
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d"
            }
            post {
                failure {
                    echo "Deployment skipped due to earlier test failures"
                }
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
