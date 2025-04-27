pipeline {
    agent any

    environment {
        VENV = "venv" // Virtual Environment Name
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Clone your GitHub or Git repo
                git credentialsId: 'your-credential-id', url: 'https://github.com/your-username/your-repo.git', branch: 'main'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV}
                source ${VENV}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source ${VENV}/bin/activate
                pytest tests/
                '''
            }
        }

        stage('Validate Model') {
            steps {
                sh '''
                source ${VENV}/bin/activate
                python validate_model.py
                '''
            }
        }

        stage('Deploy (Dummy Step)') {
            steps {
                echo "Deployment would happen here!"
                // You can later replace this with real commands like docker push, aws s3 cp, etc.
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
