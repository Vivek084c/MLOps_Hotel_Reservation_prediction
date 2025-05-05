pipeline{
    agent any

    stages{
        stage('Cloning Github Repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repo to Jenkins..'
                    checkout scmGit(branches: [[name: '*/master']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHub_token', url: 'https://github.com/Vivek084c/MLOps_Hotel_Reservation_prediction.git']])
                }
            }
        }
    }
}