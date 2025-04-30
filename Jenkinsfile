pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')  // Poll every 5 minutes
    }

    environment {
        DOCKER_IMAGE = 'vit-app'
        PORT = '5000'
        HF_TOKEN = credentials('hf-token')
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
                        withCredentials([string(credentialsId: 'hf-token', variable: 'HF_TOKEN')]) {
                            // Create .env file
                            writeFile file: '.env', text: "HF_TOKEN=${HF_TOKEN}"
                            // Run container with environment file
                            bat "docker run -d -p ${PORT}:${PORT} --name vit-container --env-file .env ${DOCKER_IMAGE}:latest"
                        }
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
                        // Simple check if container exists and is running
                        def containerId = bat(script: 'docker ps -q -f name=vit-container', returnStdout: true).trim()
                        if (containerId) {
                            echo "Container is running with ID: ${containerId}"
                            // Check if port is bound
                            def portCheck = bat(script: 'docker port vit-container 5000', returnStdout: true).trim()
                            echo "Port mapping: ${portCheck}"
                            currentBuild.result = 'SUCCESS'
                        } else {
                            echo "Container is not running"
                            currentBuild.result = 'FAILURE'
                            error "Container verification failed"
                        }
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
