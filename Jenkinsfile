pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'image-classification-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        HF_TOKEN = credentials('hf-token')
    }

    stages {
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

        stage('Test') {
            steps {
                script {
                    // Run any tests here if needed
                    echo 'Running tests...'
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
                            -p 5000:5000 \
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
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
