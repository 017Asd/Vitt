pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'image-classification-app'
        PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code from repository...'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                echo 'Would run: docker build -t ${DOCKER_IMAGE} .'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Starting deployment...'
                echo 'Would run: docker run -d --name ${DOCKER_IMAGE} -p ${PORT}:${PORT} ${DOCKER_IMAGE}'
            }
        }

        stage('Verify') {
            steps {
                echo 'Verifying deployment...'
                echo 'Would check if container is running on port ${PORT}'
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
            Application would be running at http://localhost:${PORT}
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

