pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'image-classification-app'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        HF_TOKEN = credentials('hf-token')
        PORT = '5000'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clean workspace before build
                cleanWs()
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/master']],
                    userRemoteConfigs: [[url: 'https://github.com/017Asd/Vit.git']]
                ])
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Starting Docker build..."
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                    echo "Docker build completed"
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Starting deployment..."
                    
                    // Stop and remove existing container if running
                    sh '''
                        docker ps -q --filter "name=${DOCKER_IMAGE}" | grep -q . && docker stop ${DOCKER_IMAGE} || true
                        docker ps -aq --filter "name=${DOCKER_IMAGE}" | grep -q . && docker rm ${DOCKER_IMAGE} || true
                    '''
                    
                    // Run new container
                    sh """
                        docker run -d \
                            --name ${DOCKER_IMAGE} \
                            -p ${PORT}:${PORT} \
                            -e HF_TOKEN=${HF_TOKEN} \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                    echo "Deployment completed"
                }
            }
        }

        stage('Verify') {
            steps {
                script {
                    echo "Verifying deployment..."
                    sh 'docker ps | grep ${DOCKER_IMAGE}'
                    echo "Container is running on port ${PORT}"
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    echo "Cleaning up old images..."
                    sh 'docker image prune -f'
                    echo "Cleanup completed"
                }
            }
        }
    }

    post {
        success {
            echo """
            =========================================
            Pipeline completed successfully!
            Application is running at http://localhost:${PORT}
            Container: ${DOCKER_IMAGE}:${DOCKER_TAG}
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
