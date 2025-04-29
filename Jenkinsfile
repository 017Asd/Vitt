pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'image-classification-app'
        PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    bat "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Starting deployment..."
                    
                    // Stop and remove existing container if running
                    bat """
                        docker ps -q --filter "name=${DOCKER_IMAGE}" && docker stop ${DOCKER_IMAGE} || exit 0
                        docker ps -aq --filter "name=${DOCKER_IMAGE}" && docker rm ${DOCKER_IMAGE} || exit 0
                    """
                    
                    // Run new container
                    bat """
                        docker run -d ^
                            --name ${DOCKER_IMAGE} ^
                            -p ${PORT}:${PORT} ^
                            ${DOCKER_IMAGE}
                    """
                }
            }
        }

        stage('Verify') {
            steps {
                script {
                    echo "Verifying deployment..."
                    bat "docker ps | findstr ${DOCKER_IMAGE}"
                    echo "Container is running on port ${PORT}"
                }
            }
        }

        stage('Pipeline Name') {
            steps {
                echo 'Image Classification Pipeline'
            }
        }
    }

    post {
        success {
            echo """
            =========================================
            Pipeline completed successfully!
            Application is running at http://localhost:${PORT}
            =========================================
            """
        }
        failure {
            echo """
            =========================================
            Pipeline failed!
            Error details: ${currentBuild.description}
            Build URL: ${env.BUILD_URL}
            =========================================
            """
        }
    }
}
