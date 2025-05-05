pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'utility-cumulus-458217-t9'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Cloning Github Repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github Repo to Jenkins...'
                    checkout scmGit(
                        branches: [[name: '*/master']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'GitHub_token',
                            url: 'https://github.com/Vivek084c/MLOps_Hotel_Reservation_prediction.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up venv and installing dependencies') {
            steps {
                script {
                    echo 'Setting up venv and installing dependencies'
                    sh '''
                    python -m venv $VENV_DIR
                    . ${VENV_DIR}/bin/activate

                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }

        
    }
}