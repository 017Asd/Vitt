pipeline {
    agent any

    environment {
        VENV = "venv"  // Virtual Environment Name
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Clone your GitHub or Git repo
                git credentialsId: 'github-credentials', url: 'https://github.com/011111111111111/Projectdev.git', branch: 'main'
            }
        }

        // stage('Set Up Python Environment') {
        //     steps {
        //         script {
        //             // Create the virtual environment
        //             powershell 'python3 -m venv ${VENV}'
                    
        //             // Set platform-specific activation commands
        //             def activateEnv = ''
        //             if (isUnix()) {
        //                 activateEnv = 'source ${VENV}/bin/activate'
        //             } else {
        //                 activateEnv = '${VENV}\\Scripts\\activate'
        //             }

        //             // Install dependencies
        //             powershell """
        //                 ${activateEnv}
        //                 pip install --upgrade pip
        //                 pip install -r requirements.txt
        //             """
        //         }
        //     }
        // }

        stage('Run Tests') {
            steps {
                script {
                    // Set platform-specific activation commands
                    def activateEnv = ''
                    if (isUnix()) {
                        activateEnv = 'source ${VENV}/bin/activate'
                    } else {
                        activateEnv = '${VENV}\\Scripts\\activate'
                    }

                    // Run tests using pytest
                    sh """
                        ${activateEnv}
                        pytest tests/
                    """
                }
            }
        }

        // stage('Validate Model') {
        //     steps {
        //         script {
        //             // Set platform-specific activation commands
        //             def activateEnv = ''
        //             if (isUnix()) {
        //                 activateEnv = 'source ${VENV}/bin/activate'
        //             } else {
        //                 activateEnv = '${VENV}\\Scripts\\activate'
        //             }

        //             // Run model inference script
        //             sh """
        //                 ${activateEnv}
        //                 python model_infer.py
        //             """
        //         }
        //     }
        // }

        stage('Deploy (Dummy Step)') {
            steps {
                echo "Deployment would happen here!"
                // Replace with real commands later like docker push, aws s3 cp, etc.
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
