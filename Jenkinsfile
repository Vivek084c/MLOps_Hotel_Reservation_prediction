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

        stage('Building and pushing Docker image to GCR') {
            steps {
                withCredentials([file(credentialsId : 'gcp-key', variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and pushing Docker image to GCR.........'
                        sh '''
                        export PATH=$PATH:$(GCLOUD_PATH)

                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t grc.io/${GCP_PROJECT}/ml-project:latest .

                        docker push grc.io/${GCP_PROJECT}/ml-project:latest 
                        '''
                    }
                }
            }
        }

        
    }
}