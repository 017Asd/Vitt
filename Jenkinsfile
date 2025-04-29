pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')  // Poll every 5 minutes
    }

    environment {
        DOCKER_IMAGE = 'vit-app'
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
                    try {
                        // Build with cache for faster builds
                        bat "docker build -t ${DOCKER_IMAGE}:latest --cache-from ${DOCKER_IMAGE}:latest ."
                    } catch (Exception e) {
                        echo "Build failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error "Build failed"
                    }
                }
            }
        }

        stage('Stop Existing Container') {
            steps {
                script {
                    try {
                        bat 'docker stop vit-container || exit 0'
                        bat 'docker rm vit-container || exit 0'
                    } catch (Exception e) {
                        echo "Cleanup failed: ${e.message}"
                        // Continue even if cleanup fails
                    }
                }
            }
        }

        stage('Run New Container') {
            steps {
                script {
                    try {
                        bat "docker run -d -p ${PORT}:${PORT} --name vit-container ${DOCKER_IMAGE}:latest"
                    } catch (Exception e) {
                        echo "Deployment failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error "Deployment failed"
                    }
                }
            }
        }

        stage('Verify') {
            steps {
                script {
                    try {
                        // Wait for container to be healthy
                        timeout(time: 1, unit: 'MINUTES') {
                            waitUntil {
                                def status = bat(script: 'docker inspect -f {{.State.Running}} vit-container', returnStdout: true).trim()
                                return status == 'true'
                            }
                        }
                        echo "Container is running successfully"
                    } catch (Exception e) {
                        echo "Verification failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        error "Verification failed"
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline completed with status: ${currentBuild.currentResult}"
        }
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
            Check the logs for details
            =========================================
            """
        }
    }
}
