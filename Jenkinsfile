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
                        // Force stop and remove the container
                        bat 'docker stop vit-container || true'
                        bat 'docker rm -f vit-container || true'
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
                            bat "docker run -d -p ${PORT}:${PORT} --name vit-container -e \"HF_TOKEN=${HF_TOKEN}\" ${DOCKER_IMAGE}:latest"
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
                        // Wait for container to start
                        sleep 10
                        
                        // Check if container exists and is running
                        def containerId = bat(script: 'docker ps -q -f name=vit-container', returnStdout: true).trim()
                        if (containerId) {
                            echo "Container is running with ID: ${containerId}"
                            
                            // Check container logs for any startup issues
                            def logs = bat(script: 'docker logs vit-container', returnStdout: true).trim()
                            echo "Container logs: ${logs}"
                            
                            // Check if port is bound
                            def portCheck = bat(script: 'docker port vit-container 5000', returnStdout: true).trim()
                            if (portCheck) {
                                echo "Port mapping: ${portCheck}"
                                currentBuild.result = 'SUCCESS'
                            } else {
                                echo "Port 5000 is not bound"
                                currentBuild.result = 'FAILURE'
                                error "Port verification failed"
                            }
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
