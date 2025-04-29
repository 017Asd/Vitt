pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        DOCKER_IMAGE = 'image-classification-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        HF_TOKEN = credentials('hf-token')
        PORT = '5000'
    }

    stages {
        stage('Test GitHub Connection') {
            steps {
                echo "Testing GitHub connection..."
                sh 'git --version'
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    // Stop and remove existing container if running
                    sh 'docker stop ${DOCKER_IMAGE} || true'
                    sh 'docker rm ${DOCKER_IMAGE} || true'
                    
                    // Run new container
                    sh """
                        docker run -d \
                            --name ${DOCKER_IMAGE} \
                            -p ${PORT}:${PORT} \
                            -e HF_TOKEN=${HF_TOKEN} \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    // Remove old images to save space
                    sh 'docker image prune -f'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
            echo 'Application is running at http://localhost:5000'
        }
        failure {
            echo 'Pipeline failed!'
            echo 'Error details:'
            echo "${currentBuild.description}"
        }
        always {
            echo "Build URL: ${env.BUILD_URL}"
        }
    }
}
