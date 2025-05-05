pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'utility-cumulus-458217-t9'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {
        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub Repository...'
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

        stage('Setup Virtual Environment & Install Dependencies') {
            steps {
                echo 'Setting up virtual environment and installing dependencies...'
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate

                    pip install --upgrade pip
                    pip install -e .
                '''
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo 'Authenticating with GCP and pushing Docker image...'
                    sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    '''
                }
            }
        }
    }
}