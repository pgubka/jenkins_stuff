pipeline {
    agent any
    stages {
        stage('install') {
            steps {
                sh 'apt install virtualenv'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}
