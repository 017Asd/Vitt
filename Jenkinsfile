pipeline {
    agent any

    environment {
        IMAGE_NAME = "image"          // Name of your Docker image
        CONTAINER_NAME = "vit-container" // Name of your Docker container
    }

    stages {
        stage('Checkout Code') {
            steps {
                git credentialsId: 'github-credentials', url: 'https://github.com/011111111111111/Projectdev.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                powershell """
                    echo 🛠️ Building Docker image...
                    docker build -t ${env.IMAGE_NAME}:latest .
                """
            }
        }

        stage('Deploy Container') {
            steps {
                powershell """
                    echo 🚀 Deploying Docker container...

                    docker stop ${env.CONTAINER_NAME} || exit 0
                    docker rm ${env.CONTAINER_NAME} || exit 0

                    docker run -d -p 5000:5000 --name ${env.CONTAINER_NAME} ${env.IMAGE_NAME}:latest
                """
            }
        }
    }

    post {
        success {
            echo '✅ Deployment completed successfully!'
        }
        failure {
            echo '❌ Deployment failed.'
        }
    }
}
